from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import venues, events, attendees, registrations, ai
import logging
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
app = FastAPI(title="AI Smart Event Management System")

# Include routers
app.include_router(venues.router)
app.include_router(events.router)
app.include_router(attendees.router)
app.include_router(registrations.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {"message": "AI Smart Event Management System is running 🚀"}

# Provide alias `main` for ASGI servers that expect `main` attribute
main = app