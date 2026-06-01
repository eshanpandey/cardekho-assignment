"""Pydantic schemas for API request/response validation."""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict


# Nested schemas for Variant
class DimensionsSchema(BaseModel):
    """Schema for vehicle dimensions in millimeters."""
    length_mm: Optional[int] = Field(None, ge=1000, le=10000, description="Length in millimeters")
    width_mm: Optional[int] = Field(None, ge=1000, le=10000, description="Width in millimeters")
    height_mm: Optional[int] = Field(None, ge=1000, le=10000, description="Height in millimeters")
    wheelbase_mm: Optional[int] = Field(None, ge=1000, le=10000, description="Wheelbase in millimeters")

    model_config = ConfigDict(from_attributes=True)


class MileageSchema(BaseModel):
    """Schema for vehicle mileage in km/l."""
    city_mileage: Optional[float] = Field(None, gt=0, description="City mileage in km/l")
    highway_mileage: Optional[float] = Field(None, gt=0, description="Highway mileage in km/l")
    combined_mileage: Optional[float] = Field(None, gt=0, description="Combined mileage in km/l")

    model_config = ConfigDict(from_attributes=True)


# Make schemas
class MakeBase(BaseModel):
    """Base schema for Make with common fields."""
    name: str = Field(..., min_length=1, max_length=100, description="Manufacturer name")
    country: Optional[str] = Field(None, max_length=100, description="Country of origin")

    model_config = ConfigDict(from_attributes=True)


class MakeCreate(MakeBase):
    """Schema for creating a new Make."""
    pass


class MakeUpdate(BaseModel):
    """Schema for updating a Make."""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Manufacturer name")
    country: Optional[str] = Field(None, max_length=100, description="Country of origin")

    model_config = ConfigDict(from_attributes=True)


class MakeSchema(MakeBase):
    """Schema for Make response with ID."""
    id: int = Field(..., description="Unique identifier")

    model_config = ConfigDict(from_attributes=True)


class MakeWithModels(MakeSchema):
    """Schema for Make with nested models."""
    models: List["ModelSchema"] = Field(default_factory=list, description="List of models")

    model_config = ConfigDict(from_attributes=True)


# Model schemas
class ModelBase(BaseModel):
    """Base schema for Model with common fields."""
    name: str = Field(..., min_length=1, max_length=100, description="Model name")
    year: int = Field(..., ge=1900, le=2100, description="Model year")
    make_id: int = Field(..., description="Foreign key to Make")

    model_config = ConfigDict(from_attributes=True)


class ModelCreate(ModelBase):
    """Schema for creating a new Model."""
    pass


class ModelUpdate(BaseModel):
    """Schema for updating a Model."""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Model name")
    year: Optional[int] = Field(None, ge=1900, le=2100, description="Model year")
    make_id: Optional[int] = Field(None, description="Foreign key to Make")

    model_config = ConfigDict(from_attributes=True)


class ModelSchema(ModelBase):
    """Schema for Model response with ID."""
    id: int = Field(..., description="Unique identifier")

    model_config = ConfigDict(from_attributes=True)


class ModelWithMake(ModelSchema):
    """Schema for Model with nested Make."""
    make: MakeSchema = Field(..., description="Manufacturer details")

    model_config = ConfigDict(from_attributes=True)


class ModelWithVariants(ModelSchema):
    """Schema for Model with nested variants."""
    variants: List["VariantSchema"] = Field(default_factory=list, description="List of variants")

    model_config = ConfigDict(from_attributes=True)


class ModelWithMakeAndVariants(ModelSchema):
    """Schema for Model with nested Make and variants."""
    make: MakeSchema = Field(..., description="Manufacturer details")
    variants: List["VariantSchema"] = Field(default_factory=list, description="List of variants")

    model_config = ConfigDict(from_attributes=True)


# Variant schemas
class VariantBase(BaseModel):
    """Base schema for Variant with common fields."""
    name: str = Field(..., min_length=1, max_length=100, description="Variant name")
    model_id: int = Field(..., description="Foreign key to Model")
    
    # Pricing
    price: float = Field(..., gt=0, description="Price in currency units")
    
    # Engine & Transmission
    engine_type: str = Field(..., min_length=1, max_length=100, description="Engine type")
    transmission: str = Field(..., min_length=1, max_length=50, description="Transmission type")
    fuel_type: str = Field(..., min_length=1, max_length=50, description="Fuel type")
    
    # Capacity
    seating_capacity: int = Field(..., ge=1, le=20, description="Number of seats")
    
    # Dimensions (optional)
    length_mm: Optional[int] = Field(None, ge=1000, le=10000, description="Length in millimeters")
    width_mm: Optional[int] = Field(None, ge=1000, le=10000, description="Width in millimeters")
    height_mm: Optional[int] = Field(None, ge=1000, le=10000, description="Height in millimeters")
    wheelbase_mm: Optional[int] = Field(None, ge=1000, le=10000, description="Wheelbase in millimeters")
    
    # Mileage (optional)
    city_mileage: Optional[float] = Field(None, gt=0, description="City mileage in km/l")
    highway_mileage: Optional[float] = Field(None, gt=0, description="Highway mileage in km/l")
    combined_mileage: Optional[float] = Field(None, gt=0, description="Combined mileage in km/l")
    
    # Safety (optional)
    safety_rating: Optional[float] = Field(None, ge=0, le=5, description="Safety rating (0-5)")

    model_config = ConfigDict(from_attributes=True)


class VariantCreate(VariantBase):
    """Schema for creating a new Variant."""
    pass


class VariantUpdate(BaseModel):
    """Schema for updating a Variant."""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Variant name")
    model_id: Optional[int] = Field(None, description="Foreign key to Model")
    
    # Pricing
    price: Optional[float] = Field(None, gt=0, description="Price in currency units")
    
    # Engine & Transmission
    engine_type: Optional[str] = Field(None, min_length=1, max_length=100, description="Engine type")
    transmission: Optional[str] = Field(None, min_length=1, max_length=50, description="Transmission type")
    fuel_type: Optional[str] = Field(None, min_length=1, max_length=50, description="Fuel type")
    
    # Capacity
    seating_capacity: Optional[int] = Field(None, ge=1, le=20, description="Number of seats")
    
    # Dimensions (optional)
    length_mm: Optional[int] = Field(None, ge=1000, le=10000, description="Length in millimeters")
    width_mm: Optional[int] = Field(None, ge=1000, le=10000, description="Width in millimeters")
    height_mm: Optional[int] = Field(None, ge=1000, le=10000, description="Height in millimeters")
    wheelbase_mm: Optional[int] = Field(None, ge=1000, le=10000, description="Wheelbase in millimeters")
    
    # Mileage (optional)
    city_mileage: Optional[float] = Field(None, gt=0, description="City mileage in km/l")
    highway_mileage: Optional[float] = Field(None, gt=0, description="Highway mileage in km/l")
    combined_mileage: Optional[float] = Field(None, gt=0, description="Combined mileage in km/l")
    
    # Safety (optional)
    safety_rating: Optional[float] = Field(None, ge=0, le=5, description="Safety rating (0-5)")

    model_config = ConfigDict(from_attributes=True)


class VariantSchema(VariantBase):
    """Schema for Variant response with ID."""
    id: int = Field(..., description="Unique identifier")

    model_config = ConfigDict(from_attributes=True)


class VariantWithModel(VariantSchema):
    """Schema for Variant with nested Model."""
    model: ModelSchema = Field(..., description="Model details")

    model_config = ConfigDict(from_attributes=True)


class VariantWithModelAndMake(VariantSchema):
    """Schema for Variant with nested Model and Make."""
    model: ModelWithMake = Field(..., description="Model details with manufacturer")

    model_config = ConfigDict(from_attributes=True)


class VariantWithDimensionsAndMileage(VariantSchema):
    """Schema for Variant with structured dimensions and mileage."""
    dimensions: DimensionsSchema = Field(..., description="Vehicle dimensions")
    mileage: MileageSchema = Field(..., description="Vehicle mileage")

    @classmethod
    def from_variant(cls, variant):
        """Create schema from Variant model instance."""
        dimensions = DimensionsSchema(
            length_mm=variant.length_mm,
            width_mm=variant.width_mm,
            height_mm=variant.height_mm,
            wheelbase_mm=variant.wheelbase_mm
        )
        mileage = MileageSchema(
            city_mileage=variant.city_mileage,
            highway_mileage=variant.highway_mileage,
            combined_mileage=variant.combined_mileage
        )
        return cls(
            id=variant.id,
            name=variant.name,
            model_id=variant.model_id,
            price=variant.price,
            engine_type=variant.engine_type,
            transmission=variant.transmission,
            fuel_type=variant.fuel_type,
            seating_capacity=variant.seating_capacity,
            length_mm=variant.length_mm,
            width_mm=variant.width_mm,
            height_mm=variant.height_mm,
            wheelbase_mm=variant.wheelbase_mm,
            city_mileage=variant.city_mileage,
            highway_mileage=variant.highway_mileage,
            combined_mileage=variant.combined_mileage,
            safety_rating=variant.safety_rating,
            dimensions=dimensions,
            mileage=mileage
        )

    model_config = ConfigDict(from_attributes=True)


# User schemas
class UserBase(BaseModel):
    """Base schema for User with common fields."""
    email: str = Field(..., max_length=255, description="User email address")

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format."""
        if '@' not in v or '.' not in v.split('@')[-1]:
            raise ValueError('Invalid email format')
        return v.lower()

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    """Schema for creating a new User."""
    pass


class UserSchema(UserBase):
    """Schema for User response with ID and timestamp."""
    id: int = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Account creation timestamp")

    model_config = ConfigDict(from_attributes=True)


# Preference Profile schemas
class PreferenceProfileBase(BaseModel):
    """Base schema for PreferenceProfile with common fields."""
    user_id: int = Field(..., description="Foreign key to User")
    
    # Budget
    budget_min: float = Field(..., ge=0, le=100000000, description="Minimum budget")
    budget_max: float = Field(..., ge=0, le=100000000, description="Maximum budget")
    
    # Usage Patterns
    commute_distance: Optional[float] = Field(None, ge=0, le=1000, description="Daily commute distance in km")
    highway_city_ratio: Optional[float] = Field(None, ge=0, le=100, description="Percentage of highway driving")
    passenger_count: Optional[int] = Field(None, ge=1, le=10, description="Typical passenger count")
    
    # Priorities
    priority_fuel_eff: Optional[str] = Field(None, pattern="^(low|medium|high)$", description="Fuel efficiency priority")
    priority_safety: Optional[str] = Field(None, pattern="^(low|medium|high)$", description="Safety priority")
    priority_performance: Optional[str] = Field(None, pattern="^(low|medium|high)$", description="Performance priority")
    priority_comfort: Optional[str] = Field(None, pattern="^(low|medium|high)$", description="Comfort priority")
    
    # Constraints
    fuel_type_constraint: Optional[str] = Field(None, max_length=50, description="Preferred fuel type")
    transmission_pref: Optional[str] = Field(None, max_length=50, description="Preferred transmission type")
    brand_exclusions: Optional[str] = Field(None, description="Comma-separated list of excluded brands")

    @field_validator('budget_max')
    @classmethod
    def validate_budget_range(cls, v: float, info) -> float:
        """Validate that budget_max > budget_min."""
        if 'budget_min' in info.data and v <= info.data['budget_min']:
            raise ValueError('budget_max must be greater than budget_min')
        return v

    model_config = ConfigDict(from_attributes=True)


class PreferenceProfileCreate(PreferenceProfileBase):
    """Schema for creating a new PreferenceProfile."""
    pass


class PreferenceProfileUpdate(BaseModel):
    """Schema for updating a PreferenceProfile."""
    # Budget
    budget_min: Optional[float] = Field(None, ge=0, le=100000000, description="Minimum budget")
    budget_max: Optional[float] = Field(None, ge=0, le=100000000, description="Maximum budget")
    
    # Usage Patterns
    commute_distance: Optional[float] = Field(None, ge=0, le=1000, description="Daily commute distance in km")
    highway_city_ratio: Optional[float] = Field(None, ge=0, le=100, description="Percentage of highway driving")
    passenger_count: Optional[int] = Field(None, ge=1, le=10, description="Typical passenger count")
    
    # Priorities
    priority_fuel_eff: Optional[str] = Field(None, pattern="^(low|medium|high)$", description="Fuel efficiency priority")
    priority_safety: Optional[str] = Field(None, pattern="^(low|medium|high)$", description="Safety priority")
    priority_performance: Optional[str] = Field(None, pattern="^(low|medium|high)$", description="Performance priority")
    priority_comfort: Optional[str] = Field(None, pattern="^(low|medium|high)$", description="Comfort priority")
    
    # Constraints
    fuel_type_constraint: Optional[str] = Field(None, max_length=50, description="Preferred fuel type")
    transmission_pref: Optional[str] = Field(None, max_length=50, description="Preferred transmission type")
    brand_exclusions: Optional[str] = Field(None, description="Comma-separated list of excluded brands")

    model_config = ConfigDict(from_attributes=True)


class PreferenceProfileSchema(PreferenceProfileBase):
    """Schema for PreferenceProfile response with ID and timestamps."""
    id: int = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Profile creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Profile last update timestamp")

    model_config = ConfigDict(from_attributes=True)


# Shortlist schemas
class ShortlistBase(BaseModel):
    """Base schema for Shortlist with common fields."""
    profile_id: int = Field(..., description="Foreign key to PreferenceProfile")
    variant_id: int = Field(..., description="Foreign key to Variant")
    confidence_score: float = Field(..., ge=0, le=100, description="Recommendation confidence score")
    match_explanation: str = Field(..., min_length=1, description="Explanation of why this variant matches")

    model_config = ConfigDict(from_attributes=True)


class ShortlistCreate(ShortlistBase):
    """Schema for creating a new Shortlist entry."""
    pass


class ShortlistSchema(ShortlistBase):
    """Schema for Shortlist response with ID and timestamp."""
    id: int = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Shortlist creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class ShortlistWithVariant(ShortlistSchema):
    """Schema for Shortlist with nested Variant details."""
    variant: VariantWithModelAndMake = Field(..., description="Variant details with model and make")

    model_config = ConfigDict(from_attributes=True)
