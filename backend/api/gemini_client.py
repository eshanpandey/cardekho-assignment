"""Google Gemini API client for car recommendations."""
import os
import json
import logging
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

logger = logging.getLogger(__name__)


class GeminiClient:
    """Client for Google Gemini API to generate car recommendations."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-1.5-flash",
        temperature: float = 0.4,
        max_tokens: int = 2048
    ):
        """
        Initialize Gemini client.
        
        Args:
            api_key: Google Gemini API key (defaults to GEMINI_API_KEY env var)
            model_name: Model to use (default: gemini-1.5-flash)
            temperature: Temperature for generation (0.0-1.0, default: 0.4)
            max_tokens: Maximum tokens to generate (default: 2048)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        
        logger.info(f"Initialized GeminiClient with model: {model_name}")
    
    def generate_recommendations(
        self,
        preference_profile: Dict[str, Any],
        candidate_cars: List[Dict[str, Any]],
        min_recommendations: int = 3,
        max_recommendations: int = 10
    ) -> Dict[str, Any]:
        """
        Generate car recommendations using Gemini AI.
        
        Args:
            preference_profile: User preferences (budget, priorities, constraints)
            candidate_cars: List of candidate cars (after SQL pre-filtering)
            min_recommendations: Minimum number of recommendations (default: 3)
            max_recommendations: Maximum number of recommendations (default: 10)
        
        Returns:
            Dict with recommendations list and reasoning_summary
        
        Raises:
            ValueError: If API call fails or returns invalid JSON
        """
        try:
            # Build prompt
            prompt = self._build_prompt(
                preference_profile,
                candidate_cars,
                min_recommendations,
                max_recommendations
            )
            
            # Call Gemini API
            logger.info(f"Calling Gemini API with {len(candidate_cars)} candidates")
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                    response_mime_type="application/json",
                )
            )
            
            # Extract and parse JSON
            response_text = response.text.strip()
            logger.debug(f"Gemini response: {response_text[:200]}...")
            
            # Try to extract JSON from response (handle markdown code blocks)
            json_text = self._extract_json(response_text)
            result = json.loads(json_text)
            
            # Validate response structure
            self._validate_response(result)
            
            logger.info(f"Generated {len(result['recommendations'])} recommendations")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response as JSON: {e}")
            logger.error(f"Response text: {response_text}")
            raise ValueError(f"Invalid JSON response from Gemini: {e}")
        
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            raise ValueError(f"Failed to generate recommendations: {e}")
    
    def _build_prompt(
        self,
        preference_profile: Dict[str, Any],
        candidate_cars: List[Dict[str, Any]],
        min_recommendations: int,
        max_recommendations: int
    ) -> str:
        """Build the prompt for Gemini API."""
        
        # Format preference profile
        prefs_json = json.dumps(preference_profile, indent=2)
        
        # Format candidate cars (simplified for context window)
        cars_json = json.dumps(candidate_cars, indent=2)
        
        prompt = f"""You are a car recommendation expert. Analyze the user's preferences and recommend the best cars from the provided list.

User Preferences:
{prefs_json}

Available Cars (after filtering):
{cars_json}

Instructions:
1. Score each car from 0-100 based on how well it matches the user's priorities
2. Consider these factors:
   - Fuel efficiency (use city_mileage, highway_mileage, combined_mileage)
   - Safety (use safety_rating)
   - Performance (consider engine_type, transmission)
   - Comfort (consider seating_capacity, dimensions)
   - Price (prefer cars closer to budget_min for value)

3. Weight priorities based on user's settings:
   - high priority = 3x weight
   - medium priority = 2x weight
   - low priority = 1x weight

4. Select top {min_recommendations} to {max_recommendations} cars (minimum {min_recommendations}, maximum {max_recommendations})

5. For each recommended car, provide:
   - variant_id: The car's ID
   - confidence_score: Score from 0-100
   - match_explanation: 2-3 sentences explaining why this car matches
   - strengths: Array of 3-5 key strengths
   - tradeoffs: Array of any compromises (empty array if none)

6. Include a reasoning_summary explaining your overall recommendation strategy

CRITICAL: Return ONLY valid JSON. No markdown, no code blocks, no extra text. Just pure JSON.
Ensure all strings are properly closed with quotes and all arrays/objects are properly closed with brackets.

Response format:
{{"recommendations":[{{"variant_id":123,"confidence_score":85,"match_explanation":"Short explanation here.","strengths":["Strength 1","Strength 2"],"tradeoffs":["Tradeoff 1"]}}],"reasoning_summary":"Summary here."}}
"""
        return prompt
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from response text (handle markdown code blocks)."""
        text = text.strip()
        
        # Remove markdown code blocks if present
        if text.startswith("```json"):
            text = text[7:]  # Remove ```json
        elif text.startswith("```"):
            text = text[3:]  # Remove ```
        
        if text.endswith("```"):
            text = text[:-3]  # Remove trailing ```
        
        return text.strip()
    
    def _validate_response(self, result: Dict[str, Any]) -> None:
        """Validate the structure of Gemini's response."""
        if "recommendations" not in result:
            raise ValueError("Response missing 'recommendations' field")
        
        if not isinstance(result["recommendations"], list):
            raise ValueError("'recommendations' must be a list")
        
        for i, rec in enumerate(result["recommendations"]):
            required_fields = ["variant_id", "confidence_score", "match_explanation"]
            for field in required_fields:
                if field not in rec:
                    raise ValueError(f"Recommendation {i} missing required field: {field}")
            
            # Validate confidence score range
            score = rec["confidence_score"]
            if not isinstance(score, (int, float)) or score < 0 or score > 100:
                raise ValueError(f"Invalid confidence_score: {score} (must be 0-100)")
        
        logger.debug("Response validation passed")


class FallbackRecommendationEngine:
    """Simple rule-based fallback when Gemini API fails."""
    
    @staticmethod
    def generate_recommendations(
        preference_profile: Dict[str, Any],
        candidate_cars: List[Dict[str, Any]],
        max_recommendations: int = 5
    ) -> Dict[str, Any]:
        """
        Generate recommendations using simple rule-based scoring.
        
        Args:
            preference_profile: User preferences
            candidate_cars: List of candidate cars
            max_recommendations: Maximum number to return
        
        Returns:
            Dict with recommendations (same format as Gemini)
        """
        logger.warning("Using fallback recommendation engine")
        
        scored_cars = []
        budget_min = preference_profile.get("budget_min", 0)
        budget_max = preference_profile.get("budget_max", float('inf'))
        
        for car in candidate_cars:
            score = 0.0
            
            # Price score (30%): prefer cars closer to budget_min
            price = car.get("price", 0)
            if budget_min <= price <= budget_max:
                price_range = budget_max - budget_min
                if price_range > 0:
                    price_position = (price - budget_min) / price_range
                    price_score = 1.0 - (price_position * 0.5)  # Prefer lower prices
                else:
                    price_score = 1.0
                score += price_score * 30
            
            # Mileage score (30%): higher is better
            combined_mileage = car.get("combined_mileage", 0)
            if combined_mileage > 0:
                # Normalize to 0-1 (assume max 30 km/l)
                mileage_score = min(combined_mileage / 30.0, 1.0)
                score += mileage_score * 30
            
            # Safety score (40%): higher is better
            safety_rating = car.get("safety_rating", 0)
            if safety_rating > 0:
                safety_score = safety_rating / 5.0
                score += safety_score * 40
            
            scored_cars.append({
                "car": car,
                "score": score
            })
        
        # Sort by score and take top N
        scored_cars.sort(key=lambda x: x["score"], reverse=True)
        top_cars = scored_cars[:max_recommendations]
        
        # Format as recommendations
        recommendations = []
        for item in top_cars:
            car = item["car"]
            score = item["score"]
            
            recommendations.append({
                "variant_id": car.get("id"),
                "confidence_score": round(score, 1),
                "match_explanation": f"This {car.get('make', 'car')} {car.get('model', '')} {car.get('name', '')} "
                                    f"scores {score:.0f}/100 based on price (₹{car.get('price', 0):,.0f}), "
                                    f"fuel efficiency ({car.get('combined_mileage', 0)} km/l), "
                                    f"and safety rating ({car.get('safety_rating', 0)}/5 stars). "
                                    f"It offers good value within your budget.",
                "strengths": [
                    f"Price: ₹{car.get('price', 0):,.0f}",
                    f"Mileage: {car.get('combined_mileage', 0)} km/l",
                    f"Safety: {car.get('safety_rating', 0)}/5 stars"
                ],
                "tradeoffs": []
            })
        
        return {
            "recommendations": recommendations,
            "reasoning_summary": "Recommendations based on price, fuel efficiency, and safety ratings."
        }
