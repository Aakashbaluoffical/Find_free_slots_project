OpenSlot API
============

This API calculates the common availability of multiple users within a specified date range, taking into account their time zones, weekly availability, and scheduled booked slots. The API is built using FastAPI and SQLAlchemy, with a PostgreSQL database for persistence.

Features
==========

* Fetch common availability across multiple users.
* Considers user-defined weekly availability.
* Adjusts for scheduled booked slots.
* Supports timezone-based adjustments.
* Implements conflict resolution for overlapping bookings.



Installation
===============

Unzip above mentioned file

Install Dependencies:
========================
        pip install -r .\requirement.txt

Run the Application:
======================
        uvicorn main:app --reload --port=8000 --host=0.0.0.0

This will start the server at http://localhost:8000/docs.


Database Initialization:
============================
The PostgreSQL database is automatically created when the application runs for the first time.


API Endpoint
====================
Endpoint:
        
        /api/v1/add_slots

Method: POST

Request Body:

        {
                "user_ids": [1, 2,3],
                "date_range": {"start_date": "2024-10-11", "end_date": "2024-10-15"},
                "timezone": "Asia/Kolkata"
        }

user_ids: A list of user IDs to calculate common availability for.

start_date: Start date for the availability range (YYYY-MM-DD).

end_date: End date for the availability range (YYYY-MM-DD).

timezone: Timezone to adjust slots accordingly.

Response:
=========
{
    "11-10-2024": [
        "09:00AM-05:00PM",
        "08:00AM-10:00AM",
        "02:00PM-06:00PM",
        "09:00AM-05:00PM"
    ],
    "14-10-2024": [
        "08:00AM-10:00AM"
    ],
    "15-10-2024": [
        "09:00AM-05:00PM",
        "08:00AM-10:00AM",
        "02:00PM-06:00PM",
        "08:00AM-10:00AM",
        "02:00PM-06:00PM"
    ]
}

Keys are dates in the requested range.

Values are lists of time slots (in HH:MM-HH:MM format) where all users are available.


Database Models
=================

Users
=====
Table name:user_tbl

Fields:

id: User ID.

username: Username of the user.

timezone: User's timezone.


Create Table:

        create TABLE user_tbl (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            timezone VARCHAR(50) NOT NULL
        );


sample data:

        insert INTO user_tbl (username, timezone) VALUES
        ('user_1', 'America/New_York'),
        ('user_2', 'Europe/London'),
        ('user_3', 'Asia/Kolkata');


AvailableSlots
=============
Table name:available_slots_tbl

Fields:

id: Slot ID.

start_datetime: Start time of availability.

end_datetime: End time of availability.

day_of_week: Day of the week for the slot (e.g., "monday").

user_id: Foreign key referencing Users.

Create Table:

        create TABLE available_slots_tbl (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            day_of_week VARCHAR(20) NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user_tbl(id)
        );	

Sample Data:

        INSERT INTO available_slots_tbl (user_id, day_of_week, start_time, end_time) VALUES
        (1, 'Monday', '09:00', '17:00'),
        (1, 'Tuesday', '09:00', '17:00'),
        (1, 'Wednesday', '09:00', '17:00'),
        (1, 'Thursday', '09:00', '17:00'),
        (1, 'Friday', '09:00', '17:00'),
        (2, 'Monday', '08:00', '10:00'),
        (2, 'Monday', '14:00', '18:00'),
        (2, 'Tuesday', '08:00', '10:00'),
        (2, 'Tuesday', '14:00', '18:00'),
        (2, 'Wednesday', '08:00', '10:00'),
        (2, 'Wednesday', '14:00', '18:00'),
        (2, 'Thursday', '08:00', '10:00'),
        (2, 'Thursday', '14:00', '18:00'),
        (2, 'Friday', '08:00', '10:00'),
        (2, 'Friday', '14:00', '18:00'),
        (3, 'Monday', '09:00', '17:00'),
        (3, 'Tuesday', '08:00', '10:00'),
        (3, 'Tuesday', '14:00', '18:00'),
        (3, 'Wednesday', '09:00', '17:00'),
        (3, 'Thursday', '09:00', '17:00'),
        (3, 'Friday', '09:00', '17:00');

BookedSlots
===========
Table name:booked_slots_tbl,

Fields:

id: Slot ID.

start_datetime: Start time of the booked slot.

end_datetime: End time of the booked slot.

user_id: Foreign key referencing Users.

Create Table:

        create TABLE booked_slots_tbl (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    start_datetime TIMESTAMP NOT NULL,
                    end_datetime TIMESTAMP NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                    );

Sample Data:

        INSERT INTO booked_slots_tbl(user_id, start_datetime, end_datetime) VALUES

        -- user 1 schedule
        (1, '2024-10-13 10:00:00', '2024-10-13 11:00:00'),
        (1, '2024-10-14 14:00:00', '2024-10-14 15:00:00'),
        
        -- user 2 schedule
        (2, '2024-10-12 09:00:00', '2024-10-12 10:00:00'),
        (2, '2024-10-13 16:00:00', '2024-10-13 17:00:00'),

        -- user 3 schedule
        (3, '2024-10-12 15:00:00', '2024-10-12 16:00:00'),
        (3, '2024-10-13 11:00:00', '2024-10-13 12:00:00');


License
========
This project is licensed under the MIT License.
