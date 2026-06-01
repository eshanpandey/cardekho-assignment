"""Test the recommendations API endpoint."""
import requests
import json

API_URL = "http://localhost:8000"

def test_recommendations():
    """Test the recommendations endpoint."""
    print("=" * 60)
    print("Testing Recommendations API")
    print("=" * 60)
    
    # Test data
    preferences = {
        "user_id": 1,
        "budget_min": 800000,
        "budget_max": 1500000,
        "priority_fuel_eff": "high",
        "priority_safety": "high",
        "priority_performance": "medium",
        "priority_comfort": "medium",
        "fuel_type_constraint": "petrol"
    }
    
    print(f"\nSending preferences:")
    print(f"  Budget: ₹{preferences['budget_min']:,} - ₹{preferences['budget_max']:,}")
    print(f"  Fuel Type: {preferences['fuel_type_constraint']}")
    print(f"  Priorities: Fuel Eff={preferences['priority_fuel_eff']}, Safety={preferences['priority_safety']}")
    
    # Make API call
    print(f"\nCalling POST {API_URL}/api/recommendations...")
    response = requests.post(
        f"{API_URL}/api/recommendations",
        json=preferences
    )
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return
    
    result = response.json()
    
    print(f"\n{'=' * 60}")
    print(f"✅ SUCCESS - Got {result.get('count', 0)} recommendations")
    print(f"Total candidates considered: {result.get('total_candidates', 0)}")
    print("=" * 60)
    
    for i, rec in enumerate(result.get("recommendations", []), 1):
        print(f"\n{i}. Variant ID: {rec['variant_id']}")
        print(f"   Confidence Score: {rec['confidence_score']}/100")
        print(f"   Explanation: {rec['match_explanation'][:200]}...")
        print(f"   Strengths:")
        for strength in rec.get('strengths', [])[:3]:
            print(f"     - {strength}")
    
    print(f"\n{'=' * 60}")
    print(f"Reasoning: {result.get('reasoning_summary', 'N/A')}")
    print("=" * 60)

if __name__ == "__main__":
    test_recommendations()
