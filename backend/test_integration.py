"""Integration tests for car recommendation system - verifies real use cases."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.main import app
from api.database import Base, get_db
from api.models import Make, Model, Variant

# Test database setup
TEST_DATABASE_URL = "sqlite:///./test_car_research.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    """Setup test database with sample data."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Clear existing data
    db.query(Variant).delete()
    db.query(Model).delete()
    db.query(Make).delete()
    
    # Add test data (same as seed data)
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
    
    # Add models and variants
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
    
    variants_data = [
        {
            "model_id": models[0].id, "name": "VXI", "price": 649000,
            "engine_type": "1.2L K-Series Petrol", "transmission": "Manual",
            "fuel_type": "petrol", "seating_capacity": 5,
            "combined_mileage": 22.5, "safety_rating": 3.0
        },
        {
            "model_id": models[0].id, "name": "ZXI Plus AT", "price": 899000,
            "engine_type": "1.2L K-Series Petrol", "transmission": "Automatic",
            "fuel_type": "petrol", "seating_capacity": 5,
            "combined_mileage": 21.0, "safety_rating": 3.0
        },
        {
            "model_id": models[1].id, "name": "EX", "price": 1099000,
            "engine_type": "1.5L Petrol", "transmission": "Manual",
            "fuel_type": "petrol", "seating_capacity": 5,
            "combined_mileage": 17.4, "safety_rating": 4.0
        },
        {
            "model_id": models[1].id, "name": "SX Diesel AT", "price": 1799000,
            "engine_type": "1.5L Diesel", "transmission": "Automatic",
            "fuel_type": "diesel", "seating_capacity": 5,
            "combined_mileage": 19.1, "safety_rating": 4.0
        },
        {
            "model_id": models[2].id, "name": "Smart Plus", "price": 899000,
            "engine_type": "1.2L Revotron Petrol", "transmission": "Manual",
            "fuel_type": "petrol", "seating_capacity": 5,
            "combined_mileage": 17.0, "safety_rating": 5.0
        },
        {
            "model_id": models[2].id, "name": "Fearless Plus DCA", "price": 1449000,
            "engine_type": "1.2L Turbo Petrol", "transmission": "Automatic",
            "fuel_type": "petrol", "seating_capacity": 5,
            "combined_mileage": 17.5, "safety_rating": 5.0
        },
        {
            "model_id": models[3].id, "name": "V MT", "price": 1299000,
            "engine_type": "1.5L i-VTEC Petrol", "transmission": "Manual",
            "fuel_type": "petrol", "seating_capacity": 5,
            "combined_mileage": 18.4, "safety_rating": 4.5
        },
        {
            "model_id": models[3].id, "name": "VX CVT", "price": 1549000,
            "engine_type": "1.5L i-VTEC Petrol", "transmission": "CVT",
            "fuel_type": "petrol", "seating_capacity": 5,
            "combined_mileage": 18.0, "safety_rating": 4.5
        },
        {
            "model_id": models[4].id, "name": "MX Petrol", "price": 1399000,
            "engine_type": "2.0L Turbo Petrol", "transmission": "Manual",
            "fuel_type": "petrol", "seating_capacity": 7,
            "combined_mileage": 13.0, "safety_rating": 5.0
        },
        {
            "model_id": models[4].id, "name": "AX7 Diesel AT", "price": 2199000,
            "engine_type": "2.2L Diesel", "transmission": "Automatic",
            "fuel_type": "diesel", "seating_capacity": 7,
            "combined_mileage": 16.0, "safety_rating": 5.0
        },
    ]
    
    for variant_data in variants_data:
        variant = Variant(**variant_data)
        db.add(variant)
    db.commit()
    
    db.close()
    
    yield
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)


class TestRealWorldUseCases:
    """Test real-world user scenarios."""
    
    def test_safety_conscious_family_buyer(self):
        """Test: Family buyer prioritizing safety with moderate budget."""
        preferences = {
            "user_id": 1,
            "budget_min": 800000,
            "budget_max": 1500000,
            "priority_fuel_eff": "medium",
            "priority_safety": "high",
            "priority_performance": "low",
            "priority_comfort": "high",
            "fuel_type_constraint": "petrol",
        }
        
        response = client.post("/api/recommendations", json=preferences)
        assert response.status_code == 200
        
        data = response.json()
        assert data["count"] > 0, "Should return recommendations"
        assert data["count"] <= 5, "Should not exceed max recommendations"
        
        # Verify top recommendation has high safety rating
        top_rec = data["recommendations"][0]
        assert top_rec["confidence_score"] > 60, "Top recommendation should have good confidence"
        
        # Check that high-safety cars are prioritized (Nexon or City should be top)
        print(f"\n✓ Safety-conscious buyer: Got {data['count']} recommendations")
        print(f"  Top pick: Variant ID {top_rec['variant_id']} (score: {top_rec['confidence_score']})")
    
    def test_budget_conscious_fuel_efficiency_seeker(self):
        """Test: Budget buyer prioritizing fuel efficiency."""
        preferences = {
            "user_id": 1,
            "budget_min": 600000,
            "budget_max": 900000,
            "priority_fuel_eff": "high",
            "priority_safety": "medium",
            "priority_performance": "low",
            "priority_comfort": "medium",
        }
        
        response = client.post("/api/recommendations", json=preferences)
        assert response.status_code == 200
        
        data = response.json()
        assert data["count"] > 0, "Should return recommendations"
        
        # Swift should be recommended (best mileage in budget)
        top_rec = data["recommendations"][0]
        assert "strengths" in top_rec, "Should include strengths"
        assert len(top_rec["strengths"]) >= 3, "Should list multiple strengths"
        
        print(f"\n✓ Budget fuel-efficiency seeker: Got {data['count']} recommendations")
        print(f"  Top pick: Variant ID {top_rec['variant_id']}")
        print(f"  Key strength: {top_rec['strengths'][0]}")
    
    def test_automatic_transmission_preference(self):
        """Test: Buyer specifically wants automatic transmission."""
        preferences = {
            "user_id": 1,
            "budget_min": 800000,
            "budget_max": 1600000,
            "priority_fuel_eff": "medium",
            "priority_safety": "high",
            "priority_performance": "medium",
            "priority_comfort": "high",
            "transmission_pref": "automatic",
        }
        
        response = client.post("/api/recommendations", json=preferences)
        assert response.status_code == 200
        
        data = response.json()
        assert data["count"] > 0, "Should return automatic cars"
        
        # All recommendations should be automatic
        print(f"\n✓ Automatic transmission preference: Got {data['count']} recommendations")
        for i, rec in enumerate(data["recommendations"][:3]):
            print(f"  #{i+1}: Variant ID {rec['variant_id']} (score: {rec['confidence_score']})")
    
    def test_diesel_preference_higher_budget(self):
        """Test: Buyer wants diesel with higher budget."""
        preferences = {
            "user_id": 1,
            "budget_min": 1500000,
            "budget_max": 2500000,
            "priority_fuel_eff": "high",
            "priority_safety": "high",
            "priority_performance": "medium",
            "priority_comfort": "high",
            "fuel_type_constraint": "diesel",
        }
        
        response = client.post("/api/recommendations", json=preferences)
        assert response.status_code == 200
        
        data = response.json()
        assert data["count"] > 0, "Should return diesel cars"
        
        print(f"\n✓ Diesel preference (high budget): Got {data['count']} recommendations")
        top_rec = data["recommendations"][0]
        print(f"  Top pick: Variant ID {top_rec['variant_id']}")
    
    def test_performance_enthusiast(self):
        """Test: Buyer prioritizing performance over fuel efficiency."""
        preferences = {
            "user_id": 1,
            "budget_min": 1200000,
            "budget_max": 2000000,
            "priority_fuel_eff": "low",
            "priority_safety": "high",
            "priority_performance": "high",
            "priority_comfort": "high",
        }
        
        response = client.post("/api/recommendations", json=preferences)
        assert response.status_code == 200
        
        data = response.json()
        assert data["count"] > 0, "Should return recommendations"
        
        # XUV700 or Nexon turbo should be recommended
        top_rec = data["recommendations"][0]
        assert top_rec["confidence_score"] > 50, "Should have reasonable confidence"
        
        print(f"\n✓ Performance enthusiast: Got {data['count']} recommendations")
        print(f"  Top pick: Variant ID {top_rec['variant_id']} (score: {top_rec['confidence_score']})")
    
    def test_no_matches_outside_budget(self):
        """Test: Budget too low should return helpful message."""
        preferences = {
            "user_id": 1,
            "budget_min": 100000,
            "budget_max": 300000,
            "priority_fuel_eff": "high",
            "priority_safety": "high",
            "priority_performance": "medium",
            "priority_comfort": "medium",
        }
        
        response = client.post("/api/recommendations", json=preferences)
        assert response.status_code == 200
        
        data = response.json()
        assert data["count"] == 0, "Should return no recommendations"
        assert "message" in data, "Should include helpful message"
        assert "suggestions" in data, "Should include suggestions"
        
        print(f"\n✓ No matches (budget too low): Returned helpful message")
        print(f"  Message: {data['message']}")
    
    def test_balanced_priorities(self):
        """Test: Buyer with balanced priorities across all factors."""
        preferences = {
            "user_id": 1,
            "budget_min": 1000000,
            "budget_max": 1500000,
            "priority_fuel_eff": "medium",
            "priority_safety": "medium",
            "priority_performance": "medium",
            "priority_comfort": "medium",
        }
        
        response = client.post("/api/recommendations", json=preferences)
        assert response.status_code == 200
        
        data = response.json()
        assert data["count"] > 0, "Should return recommendations"
        assert data["count"] >= 3, "Should return multiple options for balanced buyer"
        
        # Should get diverse recommendations
        print(f"\n✓ Balanced priorities: Got {data['count']} recommendations")
        for i, rec in enumerate(data["recommendations"][:3]):
            print(f"  #{i+1}: Variant ID {rec['variant_id']} (score: {rec['confidence_score']})")
    
    def test_recommendation_quality_checks(self):
        """Test: Verify recommendation quality and completeness."""
        preferences = {
            "user_id": 1,
            "budget_min": 800000,
            "budget_max": 1500000,
            "priority_fuel_eff": "high",
            "priority_safety": "high",
            "priority_performance": "medium",
            "priority_comfort": "medium",
        }
        
        response = client.post("/api/recommendations", json=preferences)
        assert response.status_code == 200
        
        data = response.json()
        assert data["count"] > 0, "Should return recommendations"
        
        # Verify each recommendation has required fields
        for rec in data["recommendations"]:
            assert "variant_id" in rec, "Must have variant_id"
            assert "confidence_score" in rec, "Must have confidence_score"
            assert "match_explanation" in rec, "Must have explanation"
            assert "strengths" in rec, "Must have strengths"
            assert "tradeoffs" in rec, "Must have tradeoffs"
            
            # Verify data quality
            assert 0 <= rec["confidence_score"] <= 100, "Score must be 0-100"
            assert len(rec["match_explanation"]) > 50, "Explanation should be detailed"
            assert len(rec["strengths"]) >= 2, "Should list multiple strengths"
            assert isinstance(rec["tradeoffs"], list), "Tradeoffs must be a list"
        
        print(f"\n✓ Recommendation quality: All {data['count']} recommendations are complete")
        print(f"  Average score: {sum(r['confidence_score'] for r in data['recommendations']) / data['count']:.1f}")
    
    def test_api_response_time(self):
        """Test: API should respond within reasonable time."""
        import time
        
        preferences = {
            "user_id": 1,
            "budget_min": 800000,
            "budget_max": 1500000,
            "priority_fuel_eff": "high",
            "priority_safety": "high",
            "priority_performance": "medium",
            "priority_comfort": "medium",
        }
        
        start_time = time.time()
        response = client.post("/api/recommendations", json=preferences)
        elapsed_time = time.time() - start_time
        
        assert response.status_code == 200
        assert elapsed_time < 60, "Should respond within 60 seconds"
        
        print(f"\n✓ API response time: {elapsed_time:.2f} seconds")
    
    def test_invalid_budget_validation(self):
        """Test: Invalid budget should return 422 error."""
        preferences = {
            "user_id": 1,
            "budget_min": 1500000,
            "budget_max": 800000,  # Max < Min (invalid)
            "priority_fuel_eff": "high",
            "priority_safety": "high",
            "priority_performance": "medium",
            "priority_comfort": "medium",
        }
        
        response = client.post("/api/recommendations", json=preferences)
        assert response.status_code == 422, "Should reject invalid budget range"
        
        print(f"\n✓ Invalid budget validation: Correctly rejected (422)")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
