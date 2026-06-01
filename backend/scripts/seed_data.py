"""Script to seed the database with sample car data."""
import sys
import os
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.database import SessionLocal, init_db
from api.models import Make, Model, Variant

# Sample car data
SAMPLE_CARS = [
    {
        "make": {"name": "Maruti Suzuki", "country": "India"},
        "model": {"name": "Swift", "year": 2024},
        "variants": [
            {
                "name": "LXI",
                "price": 599000,
                "engine_type": "1.2L K-Series Petrol",
                "transmission": "Manual",
                "fuel_type": "petrol",
                "seating_capacity": 5,
                "length_mm": 3845,
                "width_mm": 1735,
                "height_mm": 1530,
                "wheelbase_mm": 2450,
                "city_mileage": 21.0,
                "highway_mileage": 25.0,
                "combined_mileage": 23.2,
                "safety_rating": 3.5
            },
            {
                "name": "ZXI Plus AMT",
                "price": 849000,
                "engine_type": "1.2L K-Series Petrol",
                "transmission": "AMT",
                "fuel_type": "petrol",
                "seating_capacity": 5,
                "length_mm": 3845,
                "width_mm": 1735,
                "height_mm": 1530,
                "wheelbase_mm": 2450,
                "city_mileage": 22.0,
                "highway_mileage": 26.0,
                "combined_mileage": 24.0,
                "safety_rating": 3.5
            }
        ]
    },
    {
        "make": {"name": "Honda", "country": "Japan"},
        "model": {"name": "City", "year": 2024},
        "variants": [
            {
                "name": "V MT",
                "price": 1199000,
                "engine_type": "1.5L i-VTEC Petrol",
                "transmission": "Manual",
                "fuel_type": "petrol",
                "seating_capacity": 5,
                "length_mm": 4549,
                "width_mm": 1748,
                "height_mm": 1489,
                "wheelbase_mm": 2600,
                "city_mileage": 16.5,
                "highway_mileage": 21.0,
                "combined_mileage": 18.4,
                "safety_rating": 4.5
            },
            {
                "name": "VX CVT",
                "price": 1449000,
                "engine_type": "1.5L i-VTEC Petrol",
                "transmission": "CVT",
                "fuel_type": "petrol",
                "seating_capacity": 5,
                "length_mm": 4549,
                "width_mm": 1748,
                "height_mm": 1489,
                "wheelbase_mm": 2600,
                "city_mileage": 17.0,
                "highway_mileage": 21.5,
                "combined_mileage": 18.9,
                "safety_rating": 4.5
            }
        ]
    },
    {
        "make": {"name": "Hyundai", "country": "South Korea"},
        "model": {"name": "Verna", "year": 2024},
        "variants": [
            {
                "name": "SX MT",
                "price": 1099000,
                "engine_type": "1.5L MPi Petrol",
                "transmission": "Manual",
                "fuel_type": "petrol",
                "seating_capacity": 5,
                "length_mm": 4535,
                "width_mm": 1765,
                "height_mm": 1475,
                "wheelbase_mm": 2670,
                "city_mileage": 16.8,
                "highway_mileage": 20.5,
                "combined_mileage": 18.0,
                "safety_rating": 4.0
            },
            {
                "name": "SX(O) DCT",
                "price": 1599000,
                "engine_type": "1.5L Turbo GDi Petrol",
                "transmission": "DCT",
                "fuel_type": "petrol",
                "seating_capacity": 5,
                "length_mm": 4535,
                "width_mm": 1765,
                "height_mm": 1475,
                "wheelbase_mm": 2670,
                "city_mileage": 15.5,
                "highway_mileage": 19.0,
                "combined_mileage": 17.0,
                "safety_rating": 4.0
            }
        ]
    },
    {
        "make": {"name": "Tata", "country": "India"},
        "model": {"name": "Nexon", "year": 2024},
        "variants": [
            {
                "name": "Smart Plus",
                "price": 899000,
                "engine_type": "1.2L Revotron Petrol",
                "transmission": "Manual",
                "fuel_type": "petrol",
                "seating_capacity": 5,
                "length_mm": 3993,
                "width_mm": 1811,
                "height_mm": 1606,
                "wheelbase_mm": 2498,
                "city_mileage": 15.5,
                "highway_mileage": 19.5,
                "combined_mileage": 17.0,
                "safety_rating": 5.0
            },
            {
                "name": "Fearless Plus DCA",
                "price": 1349000,
                "engine_type": "1.2L Revotron Turbo Petrol",
                "transmission": "DCA",
                "fuel_type": "petrol",
                "seating_capacity": 5,
                "length_mm": 3993,
                "width_mm": 1811,
                "height_mm": 1606,
                "wheelbase_mm": 2498,
                "city_mileage": 16.0,
                "highway_mileage": 20.0,
                "combined_mileage": 17.5,
                "safety_rating": 5.0
            }
        ]
    },
    {
        "make": {"name": "Mahindra", "country": "India"},
        "model": {"name": "XUV700", "year": 2024},
        "variants": [
            {
                "name": "MX Petrol",
                "price": 1399000,
                "engine_type": "2.0L mStallion Turbo Petrol",
                "transmission": "Manual",
                "fuel_type": "petrol",
                "seating_capacity": 7,
                "length_mm": 4695,
                "width_mm": 1890,
                "height_mm": 1755,
                "wheelbase_mm": 2750,
                "city_mileage": 11.5,
                "highway_mileage": 15.0,
                "combined_mileage": 13.0,
                "safety_rating": 5.0
            },
            {
                "name": "AX7 Diesel AT",
                "price": 2199000,
                "engine_type": "2.2L mHawk Diesel",
                "transmission": "Automatic",
                "fuel_type": "diesel",
                "seating_capacity": 7,
                "length_mm": 4695,
                "width_mm": 1890,
                "height_mm": 1755,
                "wheelbase_mm": 2750,
                "city_mileage": 14.0,
                "highway_mileage": 18.0,
                "combined_mileage": 16.0,
                "safety_rating": 5.0
            }
        ]
    }
]


def seed_database():
    """Seed the database with sample car data."""
    # Initialize database first
    init_db()
    
    db = SessionLocal()
    try:
        # Check if data already exists
        existing_makes = db.query(Make).count()
        if existing_makes > 0:
            print(f"Database already contains {existing_makes} makes. Skipping seed.")
            return
        
        print("Seeding database with sample car data...")
        
        for car_data in SAMPLE_CARS:
            # Create or get make
            make = db.query(Make).filter(Make.name == car_data["make"]["name"]).first()
            if not make:
                make = Make(**car_data["make"])
                db.add(make)
                db.flush()
            
            # Create model
            model = Model(
                make_id=make.id,
                name=car_data["model"]["name"],
                year=car_data["model"]["year"]
            )
            db.add(model)
            db.flush()
            
            # Create variants
            for variant_data in car_data["variants"]:
                variant = Variant(
                    model_id=model.id,
                    **variant_data
                )
                db.add(variant)
            
            print(f"Added {car_data['make']['name']} {car_data['model']['name']} with {len(car_data['variants'])} variants")
        
        db.commit()
        print("\nDatabase seeded successfully!")
        
        # Print summary
        total_makes = db.query(Make).count()
        total_models = db.query(Model).count()
        total_variants = db.query(Variant).count()
        print(f"\nSummary:")
        print(f"  Makes: {total_makes}")
        print(f"  Models: {total_models}")
        print(f"  Variants: {total_variants}")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
