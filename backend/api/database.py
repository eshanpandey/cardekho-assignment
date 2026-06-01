"""Database configuration and session management."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Use in-memory SQLite for Vercel (or file-based for local)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False  # Disable logging in production
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Track if database is initialized
_db_initialized = False


def ensure_db_initialized():
    """Ensure database is initialized and seeded."""
    global _db_initialized
    
    if _db_initialized:
        return
    
    from api.models import Make, Model, Variant, User, PreferenceProfile, Shortlist
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Seed data
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Make).count() > 0:
            _db_initialized = True
            return
        
        # Add makes
        makes_data = [
            {"name": "Maruti Suzuki", "country": "India"},
            {"name": "Hyundai", "country": "South Korea"},
            {"name": "Tata", "country": "India"},
            {"name": "Honda", "country": "Japan"},
            {"name": "Mahindra", "country": "India"},
        ]
        
        makes = []
        for make_data in makes_data:
            make = Make(**make_data)
            db.add(make)
            makes.append(make)
        db.commit()
        
        for make in makes:
            db.refresh(make)
        
        # Add models
        models_data = [
            {"make_id": makes[0].id, "name": "Swift", "year": 2024},
            {"make_id": makes[1].id, "name": "Creta", "year": 2024},
            {"make_id": makes[2].id, "name": "Nexon", "year": 2024},
            {"make_id": makes[3].id, "name": "City", "year": 2024},
            {"make_id": makes[4].id, "name": "XUV700", "year": 2024},
        ]
        
        models = []
        for model_data in models_data:
            model = Model(**model_data)
            db.add(model)
            models.append(model)
        db.commit()
        
        for model in models:
            db.refresh(model)
        
        # Add variants
        variants_data = [
            {"model_id": models[0].id, "name": "VXI", "price": 649000, "engine_type": "1.2L K-Series Petrol", "transmission": "Manual", "fuel_type": "petrol", "seating_capacity": 5, "combined_mileage": 22.5, "safety_rating": 3.0},
            {"model_id": models[0].id, "name": "ZXI Plus AT", "price": 899000, "engine_type": "1.2L K-Series Petrol", "transmission": "Automatic", "fuel_type": "petrol", "seating_capacity": 5, "combined_mileage": 21.0, "safety_rating": 3.0},
            {"model_id": models[1].id, "name": "EX", "price": 1099000, "engine_type": "1.5L Petrol", "transmission": "Manual", "fuel_type": "petrol", "seating_capacity": 5, "combined_mileage": 17.4, "safety_rating": 4.0},
            {"model_id": models[1].id, "name": "SX Diesel AT", "price": 1799000, "engine_type": "1.5L Diesel", "transmission": "Automatic", "fuel_type": "diesel", "seating_capacity": 5, "combined_mileage": 19.1, "safety_rating": 4.0},
            {"model_id": models[2].id, "name": "Smart Plus", "price": 899000, "engine_type": "1.2L Revotron Petrol", "transmission": "Manual", "fuel_type": "petrol", "seating_capacity": 5, "combined_mileage": 17.0, "safety_rating": 5.0},
            {"model_id": models[2].id, "name": "Fearless Plus DCA", "price": 1449000, "engine_type": "1.2L Turbo Petrol", "transmission": "Automatic", "fuel_type": "petrol", "seating_capacity": 5, "combined_mileage": 17.5, "safety_rating": 5.0},
            {"model_id": models[3].id, "name": "V MT", "price": 1299000, "engine_type": "1.5L i-VTEC Petrol", "transmission": "Manual", "fuel_type": "petrol", "seating_capacity": 5, "combined_mileage": 18.4, "safety_rating": 4.5},
            {"model_id": models[3].id, "name": "VX CVT", "price": 1549000, "engine_type": "1.5L i-VTEC Petrol", "transmission": "CVT", "fuel_type": "petrol", "seating_capacity": 5, "combined_mileage": 18.0, "safety_rating": 4.5},
            {"model_id": models[4].id, "name": "MX Petrol", "price": 1399000, "engine_type": "2.0L Turbo Petrol", "transmission": "Manual", "fuel_type": "petrol", "seating_capacity": 7, "combined_mileage": 13.0, "safety_rating": 5.0},
            {"model_id": models[4].id, "name": "AX7 Diesel AT", "price": 2199000, "engine_type": "2.2L Diesel", "transmission": "Automatic", "fuel_type": "diesel", "seating_capacity": 7, "combined_mileage": 16.0, "safety_rating": 5.0},
        ]
        
        for variant_data in variants_data:
            variant = Variant(**variant_data)
            db.add(variant)
        db.commit()
        
        _db_initialized = True
        print("Database initialized and seeded successfully!")
        
    finally:
        db.close()


def get_db():
    """Dependency for getting database session."""
    ensure_db_initialized()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
