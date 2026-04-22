try:
    from pydantic import BaseModel, EmailStr
    from datetime import date, time
    from typing import Optional, List
except Exception as e:
    raise ImportError(f"Failed to import schemas dependencies: {e}")

class VenueBase(BaseModel):
    name: str
    location: str
    capacity: int
    description: Optional[str] = None

class VenueCreate(VenueBase):
    model_config = {"from_attributes": True}

class Venue(VenueBase):
    id: int
    model_config = {"from_attributes": True}

class EventBase(BaseModel):
    title: str
    description: str
    date: date
    start_time: time
    end_time: time
    venue_id: int

class EventCreate(EventBase):
    model_config = {"from_attributes": True}

class Event(EventBase):
    id: int
    venue: Optional[Venue] = None
    model_config = {"from_attributes": True}

class AttendeeBase(BaseModel):
    name: str
    email: EmailStr
    interests: str

class AttendeeCreate(AttendeeBase):
    model_config = {"from_attributes": True}

class Attendee(AttendeeBase):
    id: int
    model_config = {"from_attributes": True}

class RegistrationBase(BaseModel):
    event_id: int
    attendee_id: int

class Registration(RegistrationBase):
    id: int
    registration_date: date
    model_config = {"from_attributes": True}