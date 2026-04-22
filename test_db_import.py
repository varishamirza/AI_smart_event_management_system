import traceback
import sys

try:
    print("Attempting to import sqlalchemy...")
    from sqlalchemy import create_engine
    print("✓ sqlalchemy imported")
    
    print("Attempting to import sqlalchemy.orm...")
    from sqlalchemy.orm import sessionmaker, declarative_base, Session
    print("✓ sqlalchemy.orm imported")
    
    print("Attempting to create database config...")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./events.db"
    print(f"✓ Database URL: {SQLALCHEMY_DATABASE_URL}")
    
    print("Attempting to create engine...")
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    print(f"✓ Engine created: {engine}")
    
    print("Attempting to create SessionLocal...")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print(f"✓ SessionLocal created: {SessionLocal}")
    
    print("Attempting to create Base...")
    Base = declarative_base()
    print(f"✓ Base created: {Base}")
    
    print("\n✓ All database components created successfully!")
    
except Exception as e:
    print(f"\n✗ Error occurred:")
    traceback.print_exc()
    sys.exit(1)
