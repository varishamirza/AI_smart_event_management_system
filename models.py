try:
    from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Text
    from sqlalchemy.orm import relationship
    from .database import Base
    from datetime import date
except Exception as e:
    raise ImportError(f"Failed to import models dependencies: {e}")

class Venue(Base):
    __tablename__ = "venues"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    capacity = Column(Integer)
    description = Column(Text)
    events = relationship("Event", back_populates="venue")

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    date = Column(Date, index=True)
    start_time = Column(Time)
    end_time = Column(Time)
    venue_id = Column(Integer, ForeignKey("venues.id"))
    venue = relationship("Venue", back_populates="events")
    registrations = relationship("Registration", back_populates="event")

class Attendee(Base):
    __tablename__ = "attendees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    interests = Column(Text)  # e.g. "AI, machine learning, networking"
    registrations = relationship("Registration", back_populates="attendee")

class Registration(Base):
    __tablename__ = "registrations"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    attendee_id = Column(Integer, ForeignKey("attendees.id"))
    registration_date = Column(Date, default=date.today)
    event = relationship("Event", back_populates="registrations")
    attendee = relationship("Attendee", back_populates="registrations")