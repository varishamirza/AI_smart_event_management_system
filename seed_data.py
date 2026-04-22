# seed_data.py
import sys
from .database import SessionLocal, engine
from . import models, crud, schemas
from datetime import date, time

models.Base.metadata.create_all(bind=engine)

db = None
try:
    db = SessionLocal()
    
    # Venues
    v1 = crud.create_venue(db, schemas.VenueCreate(
        name="Tech Hub Auditorium", location="Lucknow", capacity=250,
        description="Modern venue with AV setup"
    ))
    db.flush()  # Ensure ID is generated
    v1_id = v1.id
    print(f"Created Venue 1: {v1.name} (ID: {v1_id})")
    
    v2 = crud.create_venue(db, schemas.VenueCreate(
        name="Innovation Center", location="Gomti Nagar", capacity=120,
        description="Co-working style space"
    ))
    db.flush()  # Ensure ID is generated
    v2_id = v2.id
    print(f"Created Venue 2: {v2.name} (ID: {v2_id})")
    
    if v1_id is None or v2_id is None:
        raise ValueError(f"Failed to create venues. v1_id: {v1_id}, v2_id: {v2_id}")

    # Events
    e1 = crud.create_event(db, schemas.EventCreate(
        title="AI & Machine Learning Summit 2026",
        description="Latest trends in GenAI, LLMs, and responsible AI",
        date=date(2026, 3, 15), start_time=time(10, 0), end_time=time(17, 0),
        venue_id=v1_id
    ))
    db.flush()
    e1_id = e1.id
    print(f"Created Event 1: {e1.title} (ID: {e1_id}, Venue ID: {v1_id})")
    
    e2 = crud.create_event(db, schemas.EventCreate(
        title="Python Developers Meetup",
        description="Talks on FastAPI, async Python, and best practices",
        date=date(2026, 2, 28), start_time=time(14, 0), end_time=time(18, 0),
        venue_id=v2_id
    ))
    db.flush()
    e2_id = e2.id
    print(f"Created Event 2: {e2.title} (ID: {e2_id}, Venue ID: {v2_id})")
    
    e3 = crud.create_event(db, schemas.EventCreate(
        title="Data Science & Visualization Workshop",
        description="Hands-on with pandas, seaborn, and Power BI",
        date=date(2026, 4, 5), start_time=time(9, 30), end_time=time(16, 30),
        venue_id=v1_id
    ))
    db.flush()
    e3_id = e3.id
    print(f"Created Event 3: {e3.title} (ID: {e3_id}, Venue ID: {v1_id})")

    # Attendees
    a1 = crud.create_attendee(db, schemas.AttendeeCreate(
        name="Varisha mirza", email="varisha.lko@example.com",
        interests="artificial intelligence, machine learning, GenAI, prompt engineering"
    ))
    db.flush()
    a1_id = a1.id
    print(f"Created Attendee 1: {a1.name} (ID: {a1_id})")
    
    a2 = crud.create_attendee(db, schemas.AttendeeCreate(
        name="Rahul Verma", email="rahul.dev@example.com",
        interests="python, fastapi, web development, backend"
    ))
    db.flush()
    a2_id = a2.id
    print(f"Created Attendee 2: {a2.name} (ID: {a2_id})")

    # Registrations
    crud.create_registration(db, schemas.RegistrationBase(event_id=e1_id, attendee_id=a1_id))
    db.flush()
    print(f"Created Registration: Event {e1_id} -> Attendee {a1_id}")
    
    crud.create_registration(db, schemas.RegistrationBase(event_id=e2_id, attendee_id=a2_id))
    db.flush()
    print(f"Created Registration: Event {e2_id} -> Attendee {a2_id}")
    
    crud.create_registration(db, schemas.RegistrationBase(event_id=e1_id, attendee_id=a2_id))
    db.flush()
    print(f"Created Registration: Event {e1_id} -> Attendee {a2_id}")

    print("\n✓ Sample data seeded successfully!")

except Exception as e:
    print(f"✗ Error seeding data: {e}")
    import traceback
    traceback.print_exc()

finally:
    if db:
        db.close()
    print("Database connection closed")