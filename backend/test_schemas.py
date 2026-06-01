"""Quick test script for Pydantic schemas."""
import sys
sys.path.insert(0, '.')

from api.schemas import (
    MakeCreate, ModelCreate, VariantCreate,
    PreferenceProfileCreate, DimensionsSchema, MileageSchema
)
from pydantic import ValidationError

def test_make_schema():
    """Test Make schema validation."""
    print("Testing MakeSchema...")
    
    # Valid make
    make = MakeCreate(name="Honda", country="Japan")
    print(f"✓ Valid make: {make.name}")
    
    # Invalid make (empty name)
    try:
        MakeCreate(name="", country="Japan")
        print("✗ Should have failed for empty name")
    except ValidationError:
        print("✓ Correctly rejected empty name")

def test_variant_schema():
    """Test Variant schema validation."""
    print("\nTesting VariantSchema...")
    
    # Valid variant
    variant = VariantCreate(
        name="VX CVT",
        model_id=1,
        price=1449000,
        engine_type="1.5L i-VTEC",
        transmission="CVT",
        fuel_type="petrol",
        seating_capacity=5,
        length_mm=4549,
        city_mileage=17.0,
        safety_rating=4.5
    )
    print(f"✓ Valid variant: {variant.name}, price={variant.price}")
    
    # Invalid price
    try:
        VariantCreate(
            name="Test",
            model_id=1,
            price=-100,  # Invalid
            engine_type="1.5L",
            transmission="Manual",
            fuel_type="petrol",
            seating_capacity=5
        )
        print("✗ Should have failed for negative price")
    except ValidationError:
        print("✓ Correctly rejected negative price")
    
    # Invalid seating capacity
    try:
        VariantCreate(
            name="Test",
            model_id=1,
            price=1000000,
            engine_type="1.5L",
            transmission="Manual",
            fuel_type="petrol",
            seating_capacity=25  # Invalid (>20)
        )
        print("✗ Should have failed for seating > 20")
    except ValidationError:
        print("✓ Correctly rejected seating_capacity > 20")
    
    # Invalid dimensions
    try:
        VariantCreate(
            name="Test",
            model_id=1,
            price=1000000,
            engine_type="1.5L",
            transmission="Manual",
            fuel_type="petrol",
            seating_capacity=5,
            length_mm=500  # Invalid (<1000)
        )
        print("✗ Should have failed for length < 1000mm")
    except ValidationError:
        print("✓ Correctly rejected length_mm < 1000")
    
    # Invalid safety rating
    try:
        VariantCreate(
            name="Test",
            model_id=1,
            price=1000000,
            engine_type="1.5L",
            transmission="Manual",
            fuel_type="petrol",
            seating_capacity=5,
            safety_rating=6.0  # Invalid (>5)
        )
        print("✗ Should have failed for safety_rating > 5")
    except ValidationError:
        print("✓ Correctly rejected safety_rating > 5")

def test_preference_profile_schema():
    """Test PreferenceProfile schema validation."""
    print("\nTesting PreferenceProfileSchema...")
    
    # Valid profile
    profile = PreferenceProfileCreate(
        user_id=1,
        budget_min=500000,
        budget_max=1000000,
        commute_distance=30,
        highway_city_ratio=60,
        passenger_count=5,
        priority_fuel_eff="high",
        priority_safety="high",
        priority_performance="medium",
        priority_comfort="medium"
    )
    print(f"✓ Valid profile: budget {profile.budget_min}-{profile.budget_max}")
    
    # Invalid budget range
    try:
        PreferenceProfileCreate(
            user_id=1,
            budget_min=1000000,
            budget_max=500000  # Invalid (< budget_min)
        )
        print("✗ Should have failed for budget_max < budget_min")
    except ValidationError:
        print("✓ Correctly rejected budget_max < budget_min")
    
    # Invalid priority value
    try:
        PreferenceProfileCreate(
            user_id=1,
            budget_min=500000,
            budget_max=1000000,
            priority_fuel_eff="very_high"  # Invalid (not low/medium/high)
        )
        print("✗ Should have failed for invalid priority value")
    except ValidationError:
        print("✓ Correctly rejected invalid priority value")

def test_nested_schemas():
    """Test nested schemas."""
    print("\nTesting nested schemas...")
    
    # Valid dimensions
    dims = DimensionsSchema(
        length_mm=4549,
        width_mm=1748,
        height_mm=1489,
        wheelbase_mm=2600
    )
    print(f"✓ Valid dimensions: {dims.length_mm}x{dims.width_mm}x{dims.height_mm}mm")
    
    # Valid mileage
    mileage = MileageSchema(
        city_mileage=17.0,
        highway_mileage=21.5,
        combined_mileage=18.9
    )
    print(f"✓ Valid mileage: city={mileage.city_mileage}, highway={mileage.highway_mileage}")

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Pydantic Schemas")
    print("=" * 60)
    
    test_make_schema()
    test_variant_schema()
    test_preference_profile_schema()
    test_nested_schemas()
    
    print("\n" + "=" * 60)
    print("✅ All schema tests passed!")
    print("=" * 60)
