from sqlalchemy import Boolean, Column, ForeignKey, Integer, String , Float ,DateTime
from sqlalchemy.orm import relationship

from storage.database import Base


class Users(Base):
    __tablename__ = "user_tbl"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    timezone = Column(String, index=True)

    free_slots = relationship("AvailableSlots", back_populates="user")
    booked_slots = relationship("BookedSlots", back_populates="user")

class AvailableSlots(Base):
    __tablename__ = "available_slots_tbl"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(String, index=True)
    end_time = Column(String, index=True)
    day_of_week = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("user_tbl.id"), index=True)
    user = relationship("Users", back_populates="free_slots")

class BookedSlots(Base):
    __tablename__ = "booked_slots_tbl"

    id = Column(Integer, primary_key=True, index=True)
    start_datetime = Column(DateTime, index=True)
    end_datetime = Column(DateTime, index=True)
    user_id = Column(Integer, ForeignKey("user_tbl.id"), index=True)
    user = relationship("Users", back_populates="booked_slots")