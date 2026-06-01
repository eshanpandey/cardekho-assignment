"""FastAPI main application - MVP with single recommendation endpoint."""
import os
import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Dict, Any
from dotenv import load_dotenv

from api.database import get_db
from api.schemas import PreferenceProfileCreate
from api.recommendation_engine import RecommendationEngine

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load config from environment
MAX_CANDIDATE_CARS = int(os.getenv("MAX_CANDIDATE_CARS", "50"))
MIN_RECOMMENDATIONS = int(os.getenv("MIN_RECOMMENDATIONS", "3"))
MAX_RECOMMENDATIONS = int(os.getenv("MAX_RECOMMENDATIONS", "10"))

# Create FastAPI app
app = FastAPI(
    title="Car Research Platform API",
    description="AI-powered car recommendation system",
    version="0.1.0"
)

# Configure CORS (allow all origins for MVP)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Car Research Platform API",
        "version": "0.1.0",
        "endpoints": {
            "recommendations": "POST /api/recommendations",
            "health": "GET /health"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/recommendations")
def get_recommendations(
    preferences: PreferenceProfileCreate,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Generate car recommendations based on user preferences.
    
    Args:
        preferences: User preference profile
        db: Database session
    
    Returns:
        Dict with recommendations list and metadata
    
    Example request:
    ```json
    {
      "user_id": 1,
      "budget_min": 800000,
      "budget_max": 1500000,
      "priority_fuel_eff": "high",
      "priority_safety": "high",
      "priority_performance": "medium",
      "priority_comfort": "medium",
      "fuel_type_constraint": "petrol",
      "transmission_pref": "automatic"
    }
    ```
    """
    try:
        logger.info(f"Generating recommendations for budget: ₹{preferences.budget_min}-₹{preferences.budget_max}")
        
        # Convert Pydantic model to dict
        prefs_dict = preferences.model_dump()
        
        # Initialize recommendation engine
        engine = RecommendationEngine(db, use_ai=True)
        
        # Generate recommendations
        result = engine.generate_recommendations(
            prefs_dict,
            max_candidates=MAX_CANDIDATE_CARS,
            min_recommendations=MIN_RECOMMENDATIONS,
            max_recommendations=MAX_RECOMMENDATIONS
        )
        
        logger.info(f"Generated {result.get('count', 0)} recommendations")
        
        return result
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate recommendations: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
