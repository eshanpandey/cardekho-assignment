"""SQLAlchemy database models."""
from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, 
    DateTime, Text, CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from api.database import Base


class Make(Base):
    """Car manufacturer/make table."""
    __tablename__ = "makes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    country = Column(String(100))
    
    # Relationships
    models = relationship("Model", back_populates="make", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Make(id={self.id}, name='{self.name}')>"


class Model(Base):
    """Car model table."""
    __tablename__ = "models"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    make_id = Column(Integer, ForeignKey("makes.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    year = Column(Integer, nullable=False)
    
    # Relationships
    make = relationship("Make", back_populates="models")
    variants = relationship("Variant", back_populates="model", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('make_id', 'name', 'year', name='uq_model_make_name_year'),
    )
    
    def __repr__(self):
        return f"<Model(id={self.id}, name='{self.name}', year={self.year})>"


class Variant(Base):
    """Car variant table with specifications."""
    __tablename__ = "variants"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    
    # Pricing
    price = Column(Float, nullable=False, index=True)
    
    # Engine & Transmission
    engine_type = Column(String(100), nullable=False)
    transmission = Column(String(50), nullable=False, index=True)
    fuel_type = Column(String(50), nullable=False, index=True)
    
    # Capacity & Dimensions
    seating_capacity = Column(Integer, nullable=False)
    length_mm = Column(Integer)
    width_mm = Column(Integer)
    height_mm = Column(Integer)
    wheelbase_mm = Column(Integer)
    
    # Mileage (km/l)
    city_mileage = Column(Float)
    highway_mileage = Column(Float)
    combined_mileage = Column(Float)
    
    # Safety
    safety_rating = Column(Float, index=True)
    
    # Relationships
    model = relationship("Model", back_populates="variants")
    shortlists = relationship("Shortlist", back_populates="variant")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('price > 0', name='check_price_positive'),
        CheckConstraint('seating_capacity BETWEEN 1 AND 20', name='check_seating_capacity'),
        CheckConstraint('length_mm BETWEEN 1000 AND 10000', name='check_length'),
        CheckConstraint('width_mm BETWEEN 1000 AND 10000', name='check_width'),
        CheckConstraint('height_mm BETWEEN 1000 AND 10000', name='check_height'),
        CheckConstraint('wheelbase_mm BETWEEN 1000 AND 10000', name='check_wheelbase'),
        CheckConstraint('city_mileage > 0', name='check_city_mileage'),
        CheckConstraint('highway_mileage > 0', name='check_highway_mileage'),
        CheckConstraint('combined_mileage > 0', name='check_combined_mileage'),
        CheckConstraint('safety_rating BETWEEN 0 AND 5', name='check_safety_rating'),
    )
    
    def __repr__(self):
        return f"<Variant(id={self.id}, name='{self.name}', price={self.price})>"


class User(Base):
    """User table."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    preference_profiles = relationship("PreferenceProfile", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"


class PreferenceProfile(Base):
    """User preference profile table."""
    __tablename__ = "preference_profiles"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Budget
    budget_min = Column(Float, nullable=False)
    budget_max = Column(Float, nullable=False)
    
    # Usage Patterns
    commute_distance = Column(Float)  # km per day
    highway_city_ratio = Column(Float)  # 0-100 (percentage highway driving)
    passenger_count = Column(Integer)
    
    # Priorities (low, medium, high)
    priority_fuel_eff = Column(String(10))
    priority_safety = Column(String(10))
    priority_performance = Column(String(10))
    priority_comfort = Column(String(10))
    
    # Constraints
    fuel_type_constraint = Column(String(50))  # e.g., "petrol", "diesel", "electric"
    transmission_pref = Column(String(50))  # e.g., "manual", "automatic"
    brand_exclusions = Column(Text)  # Comma-separated list of brands to exclude
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="preference_profiles")
    shortlists = relationship("Shortlist", back_populates="profile", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('budget_min >= 0 AND budget_min <= 100000000', name='check_budget_min'),
        CheckConstraint('budget_max >= 0 AND budget_max <= 100000000', name='check_budget_max'),
        CheckConstraint('budget_min < budget_max', name='check_budget_range'),
        CheckConstraint('commute_distance >= 0 AND commute_distance <= 1000', name='check_commute'),
        CheckConstraint('highway_city_ratio BETWEEN 0 AND 100', name='check_highway_ratio'),
        CheckConstraint('passenger_count BETWEEN 1 AND 10', name='check_passenger_count'),
        CheckConstraint(
            "priority_fuel_eff IN ('low', 'medium', 'high')", 
            name='check_priority_fuel_eff'
        ),
        CheckConstraint(
            "priority_safety IN ('low', 'medium', 'high')", 
            name='check_priority_safety'
        ),
        CheckConstraint(
            "priority_performance IN ('low', 'medium', 'high')", 
            name='check_priority_performance'
        ),
        CheckConstraint(
            "priority_comfort IN ('low', 'medium', 'high')", 
            name='check_priority_comfort'
        ),
    )
    
    def __repr__(self):
        return f"<PreferenceProfile(id={self.id}, user_id={self.user_id})>"


class Shortlist(Base):
    """Shortlist table storing recommendations."""
    __tablename__ = "shortlists"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey("preference_profiles.id"), nullable=False, index=True)
    variant_id = Column(Integer, ForeignKey("variants.id"), nullable=False)
    
    # Recommendation details
    confidence_score = Column(Float, nullable=False, index=True)
    match_explanation = Column(Text, nullable=False)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    profile = relationship("PreferenceProfile", back_populates="shortlists")
    variant = relationship("Variant", back_populates="shortlists")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('confidence_score BETWEEN 0 AND 100', name='check_confidence_score'),
        UniqueConstraint('profile_id', 'variant_id', name='uq_profile_variant'),
    )
    
    def __repr__(self):
        return f"<Shortlist(id={self.id}, confidence_score={self.confidence_score})>"
