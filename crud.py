from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date

def create_venue(db: Session, venue: schemas.VenueCreate):
    db_venue = models.Venue(**venue.model_dump())
    db.add(db_venue); db.commit(); db.refresh(db_venue)
    return db_venue

def get_venue(db: Session, venue_id: int):
    return db.query(models.Venue).filter(models.Venue.id == venue_id).first()

def get_venues(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Venue).offset(skip).limit(limit).all()

def update_venue(db: Session, venue_id: int, venue: schemas.VenueCreate):
    db_venue = db.query(models.Venue).filter(models.Venue.id == venue_id).first()
    if not db_venue:
        return None
    for key, value in venue.model_dump().items():
        setattr(db_venue, key, value)
    db.commit(); db.refresh(db_venue)
    return db_venue

def delete_venue(db: Session, venue_id: int):
    db_venue = db.query(models.Venue).filter(models.Venue.id == venue_id).first()
    if not db_venue:
        return False
    db.delete(db_venue); db.commit()
    return True

def get_attendee(db: Session, attendee_id: int):
    return db.query(models.Attendee).filter(models.Attendee.id == attendee_id).first()

def get_attendee_by_email(db: Session, email: str):
    return db.query(models.Attendee).filter(models.Attendee.email == email).first()

def create_attendee(db: Session, attendee: schemas.AttendeeCreate):
    db_attendee = models.Attendee(**attendee.model_dump())
    db.add(db_attendee); db.commit(); db.refresh(db_attendee)
    return db_attendee

def get_attendees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Attendee).offset(skip).limit(limit).all()

def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.model_dump())
    db.add(db_event); db.commit(); db.refresh(db_event)
    return db_event

def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()

def update_event(db: Session, event_id: int, event: schemas.EventCreate):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        return None
    for key, value in event.model_dump().items():
        setattr(db_event, key, value)
    db.commit(); db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        return False
    db.delete(db_event); db.commit()
    return True

def create_registration(db: Session, registration: schemas.RegistrationBase):
    db_registration = models.Registration(**registration.model_dump())
    db.add(db_registration); db.commit(); db.refresh(db_registration)
    return db_registration

def get_registration(db: Session, event_id: int, attendee_id: int):
    return db.query(models.Registration).filter(
        models.Registration.event_id == event_id,
        models.Registration.attendee_id == attendee_id
    ).first()

def get_registrations_by_event(db: Session, event_id: int):
    return db.query(models.Registration).filter(models.Registration.event_id == event_id).all()

def get_upcoming_events(db: Session, skip: int = 0, limit: int = 100):
    today = date.today()
    return (db.query(models.Event)
            .join(models.Venue)
            .filter(models.Event.date >= today)
            .order_by(models.Event.date)
            .offset(skip).limit(limit).all())