from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime,timedelta
from storage.database import get_db , engine
from models.model import Users,AvailableSlots,BookedSlots
from schemas.schema import AvailabilityRequest
from models import model
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware


#automatically creates table and columns
model.Base.metadata.create_all(bind=engine) 

app = FastAPI()




# CORS functionality 
origins = [
    "http://localhost:4200",
    "http://localhost:8000",
    "http://localhost:8001"    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def group_availability_by_day(availability, start_date, end_date):
    grouped = {}
    print()
    for day_offset in range((end_date - start_date).days + 1):
        current_date = start_date + timedelta(days=day_offset)
        print("current_date",current_date)
        current_day = current_date.strftime("%A")
        print("current_day",current_day)
        grouped[current_date] = [
            {"start": a.start_time, "end": a.end_time}
            for a in availability if a.day_of_week == current_day
        ]
    return grouped


async def filter_conflicts(availability_by_day, booked_slots):
    for bookings in booked_slots:
        event_date = bookings.start_datetime.date()
        if event_date in availability_by_day:
            availability_by_day[event_date] = [
                slot for slot in availability_by_day[event_date]
                if not (
                    bookings.start_datetime.time() < slot["end"] and
                    bookings.end_datetime.time() > slot["start"]
                )
            ]
    return availability_by_day

# this below function is to find the common time slots
async def find_common_slots(availability_by_day):
    common_availability = {}
    for date, slots in availability_by_day.items():
        if slots:
            formatted_slots = [
                f"{slot['start'].strftime('%I:%M%p')}-{slot['end'].strftime('%I:%M%p')}"
                for slot in slots
            ]
            common_availability[date.strftime("%d-%m-%Y")] = formatted_slots
    return common_availability


# Dependency injection
db_dependency = Annotated[Session,Depends(get_db)]


# api for data
@app.post("/api/v1/add_slots")
async def post_add_slots(request: AvailabilityRequest, db: db_dependency):
    user_ids = request.user_ids
    start_date = datetime.strptime(request.date_range["start_date"], "%Y-%m-%d").date()
    end_date = datetime.strptime(request.date_range["end_date"], "%Y-%m-%d").date()
    
    
    
    availability = db.query(
        AvailableSlots.start_time,
        AvailableSlots.end_time,
        AvailableSlots.day_of_week,
        AvailableSlots.user_id
    ).filter(
        AvailableSlots.user_id.in_(user_ids)
    ).all()

    booked_slots = db.query(
        BookedSlots.start_datetime,
        BookedSlots.end_datetime,
        BookedSlots.user_id
    ).filter(
        and_(
            BookedSlots.user_id.in_(user_ids),
            BookedSlots.start_datetime >= start_date,
            BookedSlots.end_datetime <= end_date,
        )
    ).all()

    availability_by_day = await group_availability_by_day(availability, start_date, end_date)

    filtered_availability = await filter_conflicts(availability_by_day, booked_slots)

    return await find_common_slots(filtered_availability)



@app.get('/')
async def about():
    return {'data':{'name': "System API for Enterprise app.","version":"1.1" }}



if __name__ == "__name__":
    pass 
    #uvicorn.run(app,host="127.0.0.1", port=5200)