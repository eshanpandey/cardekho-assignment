"""Test script for Gemini client and fallback engine."""
import sys
sys.path.insert(0, '.')

from api.gemini_client import FallbackRecommendationEngine

def test_fallback_engine():
    """Test the fallback recommendation engine."""
    print("=" * 60)
    print("Testing Fallback Recommendation Engine")
    print("=" * 60)
    
    # Sample preference profile
    preference_profile = {
        "user_id": 1,
        "budget_min": 800000,
        "budget_max": 1500000,
        "priority_fuel_eff": "high",
        "priority_safety": "high",
        "priority_performance": "medium",
        "priority_comfort": "medium"
    }
    
    # Sample candidate cars (from our seeded data)
    candidate_cars = [
        {
            "id": 1,
            "make": "Maruti Suzuki",
            "model": "Swift",
            "name": "ZXI Plus AMT",
            "price": 849000,
            "fuel_type": "petrol",
            "transmission": "AMT",
            "combined_mileage": 24.0,
            "safety_rating": 3.5,
            "seating_capacity": 5
        },
        {
            "id": 2,
            "make": "Honda",
            "model": "City",
            "name": "V MT",
            "price": 1199000,
            "fuel_type": "petrol",
            "transmission": "Manual",
            "combined_mileage": 18.4,
            "safety_rating": 4.5,
            "seating_capacity": 5
        },
        {
            "id": 3,
            "make": "Honda",
            "model": "City",
            "name": "VX CVT",
            "price": 1449000,
            "fuel_type": "petrol",
            "transmission": "CVT",
            "combined_mileage": 18.9,
            "safety_rating": 4.5,
            "seating_capacity": 5
        },
        {
            "id": 4,
            "make": "Tata",
            "model": "Nexon",
            "name": "Smart Plus",
            "price": 899000,
            "fuel_type": "petrol",
            "transmission": "Manual",
            "combined_mileage": 17.0,
            "safety_rating": 5.0,
            "seating_capacity": 5
        },
        {
            "id": 5,
            "make": "Tata",
            "model": "Nexon",
            "name": "Fearless Plus DCA",
            "price": 1349000,
            "fuel_type": "petrol",
            "transmission": "DCA",
            "combined_mileage": 17.5,
            "safety_rating": 5.0,
            "seating_capacity": 5
        }
    ]
    
    print(f"\nUser Budget: ₹{preference_profile['budget_min']:,} - ₹{preference_profile['budget_max']:,}")
    print(f"Priorities: Fuel Efficiency={preference_profile['priority_fuel_eff']}, Safety={preference_profile['priority_safety']}")
    print(f"\nCandidate Cars: {len(candidate_cars)}")
    
    # Generate recommendations
    engine = FallbackRecommendationEngine()
    result = engine.generate_recommendations(
        preference_profile,
        candidate_cars,
        max_recommendations=3
    )
    
    print(f"\n{'=' * 60}")
    print("RECOMMENDATIONS")
    print("=" * 60)
    
    for i, rec in enumerate(result["recommendations"], 1):
        print(f"\n{i}. Variant ID: {rec['variant_id']}")
        print(f"   Confidence Score: {rec['confidence_score']}/100")
        print(f"   Explanation: {rec['match_explanation'][:150]}...")
        print(f"   Strengths:")
        for strength in rec['strengths']:
            print(f"     - {strength}")
        if rec['tradeoffs']:
            print(f"   Tradeoffs:")
            for tradeoff in rec['tradeoffs']:
                print(f"     - {tradeoff}")
    
    print(f"\n{'=' * 60}")
    print(f"Reasoning: {result['reasoning_summary']}")
    print("=" * 60)
    
    # Validate structure
    assert "recommendations" in result
    assert isinstance(result["recommendations"], list)
    assert len(result["recommendations"]) > 0
    assert len(result["recommendations"]) <= 3
    
    for rec in result["recommendations"]:
        assert "variant_id" in rec
        assert "confidence_score" in rec
        assert "match_explanation" in rec
        assert "strengths" in rec
        assert "tradeoffs" in rec
        assert 0 <= rec["confidence_score"] <= 100
    
    print("\n✅ All fallback engine tests passed!")

if __name__ == "__main__":
    test_fallback_engine()
