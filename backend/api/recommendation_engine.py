"""Recommendation engine with SQL pre-filtering and Gemini AI."""
import os
import logging
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from api.models import Variant, Model, Make
from api.gemini_client import GeminiClient, FallbackRecommendationEngine

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """Engine for generating car recommendations."""
    
    def __init__(self, db: Session, use_ai: bool = True):
        """
        Initialize recommendation engine.
        
        Args:
            db: Database session
            use_ai: Whether to use Gemini AI (default: True, falls back to rule-based)
        """
        self.db = db
        self.use_ai = use_ai
        
        if use_ai:
            try:
                model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
                temperature = float(os.getenv("GEMINI_TEMPERATURE", "0.4"))
                max_tokens = int(os.getenv("GEMINI_MAX_TOKENS", "2048"))
                self.gemini_client = GeminiClient(
                    model_name=model_name,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                logger.info(f"Initialized with Gemini AI (model: {model_name}, temp: {temperature}, max_tokens: {max_tokens})")
            except ValueError as e:
                logger.warning(f"Gemini API not available: {e}. Using fallback engine.")
                self.gemini_client = None
        else:
            self.gemini_client = None
            logger.info("Initialized with fallback engine only")
    
    def generate_recommendations(
        self,
        preference_profile: Dict[str, Any],
        max_candidates: int = 50,
        min_recommendations: int = 3,
        max_recommendations: int = 10
    ) -> Dict[str, Any]:
        """
        Generate car recommendations based on user preferences.
        
        Args:
            preference_profile: User preferences dict
            max_candidates: Maximum candidates to pass to AI (default: 50)
            min_recommendations: Minimum recommendations to return (default: 3)
            max_recommendations: Maximum recommendations to return (default: 10)
        
        Returns:
            Dict with recommendations list and metadata
        """
        # Step 1: SQL pre-filtering
        candidates = self._filter_candidates(preference_profile, max_candidates)
        
        if not candidates:
            return {
                "recommendations": [],
                "count": 0,
                "message": "No cars match your criteria. Try relaxing your budget or constraints.",
                "suggestions": [
                    "Increase your budget range",
                    "Remove fuel type or transmission constraints",
                    "Consider more brands"
                ]
            }
        
        logger.info(f"Found {len(candidates)} candidates after SQL filtering")
        
        # Step 2: Format candidates for AI
        candidate_dicts = self._format_candidates(candidates)
        
        # Step 3: Generate recommendations using AI or fallback
        try:
            if self.gemini_client:
                result = self.gemini_client.generate_recommendations(
                    preference_profile,
                    candidate_dicts,
                    min_recommendations,
                    max_recommendations
                )
            else:
                result = FallbackRecommendationEngine.generate_recommendations(
                    preference_profile,
                    candidate_dicts,
                    max_recommendations
                )
            
            # Add metadata
            result["count"] = len(result["recommendations"])
            result["total_candidates"] = len(candidates)
            
            return result
            
        except Exception as e:
            logger.error(f"Recommendation generation failed: {e}")
            # Fall back to rule-based
            logger.info("Falling back to rule-based engine")
            result = FallbackRecommendationEngine.generate_recommendations(
                preference_profile,
                candidate_dicts,
                max_recommendations
            )
            result["count"] = len(result["recommendations"])
            result["total_candidates"] = len(candidates)
            result["fallback_used"] = True
            return result
    
    def _filter_candidates(
        self,
        preference_profile: Dict[str, Any],
        max_candidates: int
    ) -> List[Variant]:
        """
        Pre-filter candidates using SQL based on hard constraints.
        
        Args:
            preference_profile: User preferences
            max_candidates: Maximum number of candidates to return
        
        Returns:
            List of Variant model instances
        """
        query = self.db.query(Variant).join(Model).join(Make)
        
        # Budget filter (required)
        budget_min = preference_profile.get("budget_min", 0)
        budget_max = preference_profile.get("budget_max", float('inf'))
        query = query.filter(and_(
            Variant.price >= budget_min,
            Variant.price <= budget_max
        ))
        
        # Fuel type constraint
        fuel_type = preference_profile.get("fuel_type_constraint")
        if fuel_type:
            query = query.filter(Variant.fuel_type == fuel_type)
        
        # Transmission preference
        transmission = preference_profile.get("transmission_pref")
        if transmission:
            query = query.filter(Variant.transmission.ilike(f"%{transmission}%"))
        
        # Brand exclusions
        brand_exclusions = preference_profile.get("brand_exclusions", "")
        if brand_exclusions:
            excluded_brands = [b.strip() for b in brand_exclusions.split(",")]
            query = query.filter(~Make.name.in_(excluded_brands))
        
        # Order by safety rating (desc) and price (asc) for better candidates
        query = query.order_by(
            Variant.safety_rating.desc().nullslast(),
            Variant.price.asc()
        )
        
        # Limit results
        candidates = query.limit(max_candidates).all()
        
        return candidates
    
    def _format_candidates(self, candidates: List[Variant]) -> List[Dict[str, Any]]:
        """
        Format Variant models as dicts for AI processing.
        
        Args:
            candidates: List of Variant model instances
        
        Returns:
            List of candidate dicts
        """
        formatted = []
        
        for variant in candidates:
            formatted.append({
                "id": variant.id,
                "make": variant.model.make.name,
                "model": variant.model.name,
                "name": variant.name,
                "year": variant.model.year,
                "price": variant.price,
                "engine_type": variant.engine_type,
                "transmission": variant.transmission,
                "fuel_type": variant.fuel_type,
                "seating_capacity": variant.seating_capacity,
                "length_mm": variant.length_mm,
                "width_mm": variant.width_mm,
                "height_mm": variant.height_mm,
                "wheelbase_mm": variant.wheelbase_mm,
                "city_mileage": variant.city_mileage,
                "highway_mileage": variant.highway_mileage,
                "combined_mileage": variant.combined_mileage,
                "safety_rating": variant.safety_rating
            })
        
        return formatted
