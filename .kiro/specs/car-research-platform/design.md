# Design Document

## System Architecture

### High-Level Architecture

```
┌─────────────────┐
│   Next.js       │
│   Frontend      │
│  (Vercel)       │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│   FastAPI       │
│   Backend       │
│  (Vercel        │
│  Serverless)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   SQLite        │
│   Database      │
│  (File-based)   │
└─────────────────┘
```

### Technology Stack

**Frontend:**
- Next.js 14+ (App Router)
- React 18+
- TypeScript
- Tailwind CSS for styling
- Deployed on Vercel

**Backend:**
- Python 3.11+
- FastAPI framework
- SQLAlchemy ORM
- Pydantic for validation
- SQLite database
- Google Gemini API for recommendations
- Deployed on Vercel as serverless functions

**Deployment:**
- Vercel for both frontend and backend
- SQLite database file stored in persistent storage or mounted volume
- Google Gemini API for AI-powered recommendations
- Environment variables for configuration (API keys, model settings)

## Database Design

### Entity Relationship Diagram

```
┌──────────────┐
│    Make      │
│──────────────│
│ id (PK)      │
│ name         │
│ country      │
└──────┬───────┘
       │ 1
       │
       │ N
┌──────▼───────┐
│    Model     │
│──────────────│
│ id (PK)      │
│ make_id (FK) │
│ name         │
│ year         │
└──────┬───────┘
       │ 1
       │
       │ N
┌──────▼────────────┐
│    Variant        │
│───────────────────│
│ id (PK)           │
│ model_id (FK)     │
│ name              │
│ price             │
│ engine_type       │
│ transmission      │
│ fuel_type         │
│ seating_capacity  │
│ length_mm         │
│ width_mm          │
│ height_mm         │
│ wheelbase_mm      │
│ city_mileage      │
│ highway_mileage   │
│ combined_mileage  │
│ safety_rating     │
└───────────────────┘

┌──────────────────┐
│  User            │
│──────────────────│
│ id (PK)          │
│ email            │
│ created_at       │
└──────┬───────────┘
       │ 1
       │
       │ N
┌──────▼────────────────┐
│  PreferenceProfile    │
│───────────────────────│
│ id (PK)               │
│ user_id (FK)          │
│ budget_min            │
│ budget_max            │
│ commute_distance      │
│ highway_city_ratio    │
│ passenger_count       │
│ priority_fuel_eff     │
│ priority_safety       │
│ priority_performance  │
│ priority_comfort      │
│ fuel_type_constraint  │
│ transmission_pref     │
│ brand_exclusions      │
│ created_at            │
│ updated_at            │
└──────┬────────────────┘
       │ 1
       │
       │ N
┌──────▼────────────┐
│  Shortlist        │
│───────────────────│
│ id (PK)           │
│ profile_id (FK)   │
│ variant_id (FK)   │
│ confidence_score  │
│ match_explanation │
│ created_at        │
└───────────────────┘
```

### Database Schema (SQLite)

**makes table:**
```sql
CREATE TABLE makes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    country TEXT
);
CREATE INDEX idx_makes_name ON makes(name);
```

**models table:**
```sql
CREATE TABLE models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    make_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    year INTEGER NOT NULL,
    FOREIGN KEY (make_id) REFERENCES makes(id),
    UNIQUE(make_id, name, year)
);
CREATE INDEX idx_models_make_id ON models(make_id);
CREATE INDEX idx_models_name ON models(name);
```

**variants table:**
```sql
CREATE TABLE variants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    price REAL NOT NULL CHECK(price > 0),
    engine_type TEXT NOT NULL,
    transmission TEXT NOT NULL,
    fuel_type TEXT NOT NULL,
    seating_capacity INTEGER NOT NULL CHECK(seating_capacity BETWEEN 1 AND 20),
    length_mm INTEGER CHECK(length_mm BETWEEN 1000 AND 10000),
    width_mm INTEGER CHECK(width_mm BETWEEN 1000 AND 10000),
    height_mm INTEGER CHECK(height_mm BETWEEN 1000 AND 10000),
    wheelbase_mm INTEGER CHECK(wheelbase_mm BETWEEN 1000 AND 10000),
    city_mileage REAL CHECK(city_mileage > 0),
    highway_mileage REAL CHECK(highway_mileage > 0),
    combined_mileage REAL CHECK(combined_mileage > 0),
    safety_rating REAL CHECK(safety_rating BETWEEN 0 AND 5),
    FOREIGN KEY (model_id) REFERENCES models(id)
);
CREATE INDEX idx_variants_model_id ON variants(model_id);
CREATE INDEX idx_variants_price ON variants(price);
CREATE INDEX idx_variants_fuel_type ON variants(fuel_type);
CREATE INDEX idx_variants_transmission ON variants(transmission);
CREATE INDEX idx_variants_safety_rating ON variants(safety_rating);
```

**users table:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**preference_profiles table:**
```sql
CREATE TABLE preference_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    budget_min REAL NOT NULL CHECK(budget_min >= 0 AND budget_min <= 100000000),
    budget_max REAL NOT NULL CHECK(budget_max >= 0 AND budget_max <= 100000000),
    commute_distance REAL CHECK(commute_distance >= 0 AND commute_distance <= 1000),
    highway_city_ratio REAL CHECK(highway_city_ratio BETWEEN 0 AND 100),
    passenger_count INTEGER CHECK(passenger_count BETWEEN 1 AND 10),
    priority_fuel_eff TEXT CHECK(priority_fuel_eff IN ('low', 'medium', 'high')),
    priority_safety TEXT CHECK(priority_safety IN ('low', 'medium', 'high')),
    priority_performance TEXT CHECK(priority_performance IN ('low', 'medium', 'high')),
    priority_comfort TEXT CHECK(priority_comfort IN ('low', 'medium', 'high')),
    fuel_type_constraint TEXT,
    transmission_pref TEXT,
    brand_exclusions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    CHECK(budget_min < budget_max)
);
CREATE INDEX idx_profiles_user_id ON preference_profiles(user_id);
```

**shortlists table:**
```sql
CREATE TABLE shortlists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    variant_id INTEGER NOT NULL,
    confidence_score REAL NOT NULL CHECK(confidence_score BETWEEN 0 AND 100),
    match_explanation TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id) REFERENCES preference_profiles(id),
    FOREIGN KEY (variant_id) REFERENCES variants(id),
    UNIQUE(profile_id, variant_id)
);
CREATE INDEX idx_shortlists_profile_id ON shortlists(profile_id);
CREATE INDEX idx_shortlists_confidence_score ON shortlists(confidence_score DESC);
```

## Recommendation Engine Design

### Approach: AI-Powered Recommendations with Google Gemini

We'll use **Google Gemini API** for intelligent car recommendations for the following reasons:
1. **Natural Intelligence**: AI understands nuanced user preferences and tradeoffs
2. **Better Explanations**: Human-like, personalized explanations for each recommendation
3. **Flexible Reasoning**: Handles complex scenarios and edge cases gracefully
4. **Free Tier**: Generous free quota (15 requests/minute) perfect for demo/portfolio
5. **Fast Integration**: Less code to write and maintain

### Recommendation Flow

**Step 1: Pre-filter Database (SQL Query)**
Apply hard constraints to reduce dataset:
- Budget: `budget_min <= price <= budget_max`
- Fuel type constraint: If specified, must match
- Transmission preference: If specified, must match
- Brand exclusions: Exclude specified makes
- Result: 20-50 candidate cars (manageable for AI context)

**Step 2: Prepare AI Prompt**
Structure the prompt with:
1. User preference profile (JSON)
2. Candidate cars list (JSON array with all specs)
3. Instructions for scoring and explanation

**Step 3: Call Gemini API**
```python
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

prompt = f"""
You are a car recommendation expert. Analyze the user's preferences and recommend the best cars from the provided list.

User Preferences:
{json.dumps(preference_profile, indent=2)}

Available Cars (after filtering):
{json.dumps(candidate_cars, indent=2)}

Instructions:
1. Score each car from 0-100 based on how well it matches the user's priorities
2. Consider: fuel efficiency, safety, performance, comfort, and price
3. Weight priorities: high=3x, medium=2x, low=1x
4. Select top 3-10 cars (minimum 3, maximum 10)
5. For each recommended car, provide:
   - confidence_score (0-100)
   - match_explanation (100-300 words, 8th grade reading level)
   - strengths (list of 3-5 points)
   - tradeoffs (list of any compromises, if applicable)

Return ONLY valid JSON in this exact format:
{{
  "recommendations": [
    {{
      "variant_id": 123,
      "confidence_score": 85,
      "match_explanation": "...",
      "strengths": ["...", "..."],
      "tradeoffs": ["..."]
    }}
  ],
  "reasoning_summary": "Brief explanation of recommendation strategy"
}}
"""

response = model.generate_content(prompt)
result = json.loads(response.text)
```

**Step 4: Parse and Store Results**
- Extract recommendations from AI response
- Validate JSON structure
- Store in `shortlists` table with confidence scores and explanations
- Return to frontend

**Step 5: Fallback Strategy**
If Gemini API fails or returns invalid JSON:
1. Log error
2. Fall back to simple rule-based scoring:
   - Score = (price_match * 0.3) + (mileage_percentile * 0.3) + (safety_rating/5 * 0.4)
   - Generate basic explanation template
3. Return top 5 cars

### Gemini API Configuration

**Model Selection:**
- **gemini-1.5-flash**: Fast, cheap, good for structured outputs (recommended)
- **gemini-1.5-pro**: More capable but slower and more expensive

**API Limits (Free Tier):**
- 15 requests per minute
- 1,500 requests per day
- 1 million requests per month

**Rate Limiting Strategy:**
```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def get_recommendations_cached(preference_hash: str):
    # Cache recommendations for identical preferences
    # Reduces API calls for duplicate requests
    pass

def rate_limit_check():
    # Track requests per minute
    # Return 429 if limit exceeded
    pass
```

### Prompt Engineering Best Practices

1. **Structured Output**: Request JSON format explicitly
2. **Clear Instructions**: Specify scoring criteria and weights
3. **Context Window**: Keep candidate list to 20-50 cars (fits in context)
4. **Temperature**: Use 0.3-0.5 for consistent, focused outputs
5. **Validation**: Parse JSON and validate schema before returning

### Configuration Parameters

Stored in environment variables:

```bash
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-flash
GEMINI_TEMPERATURE=0.4
GEMINI_MAX_TOKENS=2048
MAX_CANDIDATE_CARS=50
MIN_RECOMMENDATIONS=3
MAX_RECOMMENDATIONS=10
CACHE_TTL_SECONDS=3600
```

## API Design

### Backend API Endpoints

**Base URL:** `/api/v1`

#### Car Data Endpoints

```
GET /cars
Query params: make, model, fuel_type, transmission, min_price, max_price, min_safety_rating, max_mileage
Response: List of car variants with full details

GET /cars/{variant_id}
Response: Single car variant with full details

GET /makes
Response: List of all car makes

GET /models?make_id={make_id}
Response: List of models for a make
```

#### Recommendation Endpoints

```
POST /recommendations
Body: PreferenceProfile
Response: {
  "shortlist": [
    {
      "variant": {...},
      "confidence_score": 85,
      "match_explanation": "..."
    }
  ],
  "count": 5
}

GET /recommendations/{profile_id}
Response: Previously generated shortlist
```

#### User & Profile Endpoints

```
POST /users
Body: { "email": "user@example.com" }
Response: User object

POST /profiles
Body: PreferenceProfile
Response: Created profile with ID

GET /profiles/{profile_id}
Response: Profile details

PUT /profiles/{profile_id}
Body: Updated PreferenceProfile
Response: Updated profile

GET /users/{user_id}/profiles
Response: List of user's profiles

GET /users/{user_id}/shortlists
Response: List of user's saved shortlists
```

#### Admin Endpoints

```
POST /admin/cars/import
Body: JSON array of car data
Response: Import summary

GET /admin/config
Response: Current recommendation engine config

PUT /admin/config
Body: Updated config
Response: Updated config
```

### Request/Response Models

**PreferenceProfile:**
```json
{
  "user_id": 1,
  "budget_min": 500000,
  "budget_max": 1000000,
  "commute_distance": 30,
  "highway_city_ratio": 60,
  "passenger_count": 5,
  "priority_fuel_eff": "high",
  "priority_safety": "high",
  "priority_performance": "medium",
  "priority_comfort": "medium",
  "fuel_type_constraint": "petrol",
  "transmission_pref": "automatic",
  "brand_exclusions": "Maruti,Hyundai"
}
```

**CarVariant:**
```json
{
  "id": 1,
  "make": "Honda",
  "model": "City",
  "variant": "VX CVT",
  "year": 2024,
  "price": 850000,
  "engine_type": "1.5L i-VTEC",
  "transmission": "CVT",
  "fuel_type": "petrol",
  "seating_capacity": 5,
  "dimensions": {
    "length_mm": 4549,
    "width_mm": 1748,
    "height_mm": 1489,
    "wheelbase_mm": 2600
  },
  "mileage": {
    "city": 16.5,
    "highway": 21.0,
    "combined": 18.4
  },
  "safety_rating": 4.5
}
```

## Frontend Design

### Page Structure

```
/                          → Landing page with CTA
/preferences               → Multi-step preference form
/recommendations           → Shortlist display
/recommendations/compare   → Side-by-side comparison
/cars                      → Browse all cars with filters
/cars/{id}                 → Car detail page
/profile                   → User's saved profiles & shortlists
```

### Component Hierarchy

```
App
├── Layout
│   ├── Header
│   └── Footer
├── HomePage
├── PreferenceForm
│   ├── BudgetStep
│   ├── UsageStep
│   ├── PrioritiesStep
│   └── ConstraintsStep
├── RecommendationsPage
│   ├── ShortlistCard
│   └── MatchExplanation
├── ComparisonPage
│   └── ComparisonTable
├── BrowseCarsPage
│   ├── FilterSidebar
│   └── CarGrid
└── CarDetailPage
    ├── SpecsTable
    └── ImageGallery
```

### State Management

Use React Context + hooks for:
- User authentication state
- Current preference profile
- Shortlist data
- Filter state

### Key User Flows

**Flow 1: New User → Recommendation**
1. Land on homepage
2. Click "Find My Car"
3. Fill preference form (4 steps)
4. Submit → API call to `/recommendations`
5. View shortlist with confidence scores
6. Click car → View details
7. Compare 2-3 cars
8. Save shortlist

**Flow 2: Browse & Filter**
1. Navigate to /cars
2. Apply filters (price, fuel, transmission, safety)
3. View filtered results
4. Click car → View details

## Deployment Architecture

### Vercel Deployment

**Frontend (Next.js):**
- Deploy Next.js app to Vercel
- Automatic builds on git push
- Environment variables for API URL

**Backend (FastAPI):**
- Deploy as Vercel Serverless Functions
- Create `api/` directory with Python functions
- Each endpoint becomes a serverless function
- Cold start optimization with minimal dependencies

**Database (SQLite):**
- Option 1: Mount persistent volume (Vercel Pro)
- Option 2: Use Vercel Postgres (migrate from SQLite)
- Option 3: Use Turso (SQLite-compatible edge database)

**Recommended: Turso for SQLite**
- Distributed SQLite
- Edge replication
- Compatible with SQLAlchemy
- Free tier available

### Environment Variables

```
# Backend
DATABASE_URL=libsql://your-db.turso.io
DATABASE_AUTH_TOKEN=your-token
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-1.5-flash
GEMINI_TEMPERATURE=0.4
CORS_ORIGINS=https://your-app.vercel.app

# Frontend
NEXT_PUBLIC_API_URL=https://your-app.vercel.app/api
```

### File Structure

```
car-research-platform/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── database.py
│   │   ├── gemini_client.py
│   │   ├── recommendation_engine.py
│   │   └── routes/
│   │       ├── cars.py
│   │       ├── recommendations.py
│   │       ├── users.py
│   │       └── admin.py
│   ├── requirements.txt
│   └── vercel.json
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── preferences/
│   │   ├── recommendations/
│   │   ├── cars/
│   │   └── profile/
│   ├── components/
│   ├── lib/
│   ├── package.json
│   └── next.config.js
├── data/
│   └── sample_cars.json
└── README.md
```

## Data Import Strategy

### Initial Dataset

Create `data/sample_cars.json` with 50-100 popular Indian cars:

```json
[
  {
    "make": "Maruti Suzuki",
    "model": "Swift",
    "year": 2024,
    "variants": [
      {
        "name": "VXI",
        "price": 650000,
        "engine_type": "1.2L K-Series",
        "transmission": "Manual",
        "fuel_type": "petrol",
        ...
      }
    ]
  }
]
```

### Import Script

```python
# scripts/import_data.py
import json
import requests

def import_cars(json_file):
    with open(json_file) as f:
        data = json.load(f)
    
    response = requests.post(
        'http://localhost:8000/api/v1/admin/cars/import',
        json=data
    )
    print(response.json())
```

## Testing Strategy

### Backend Tests
- Unit tests for recommendation engine scoring
- Integration tests for API endpoints
- Database migration tests

### Frontend Tests
- Component tests with React Testing Library
- E2E tests with Playwright
- Preference form validation tests

### Performance Tests
- Load testing for recommendation endpoint
- Database query optimization
- API response time monitoring

## Security Considerations

1. **Input Validation**: Pydantic models for all inputs
2. **SQL Injection**: Use SQLAlchemy ORM (parameterized queries)
3. **CORS**: Configure allowed origins
4. **Rate Limiting**: Implement on recommendation endpoint
5. **Authentication**: JWT tokens for user sessions (future)

## Future Enhancements

1. **Natural Language Input**: Allow users to describe preferences in plain English, parse with Gemini
2. **Image Upload**: Car images and galleries
3. **User Reviews**: Add review system (removed from MVP)
4. **Comparison History**: Track user comparison patterns
5. **Email Notifications**: Send shortlist via email
6. **Mobile App**: React Native version
7. **Multi-modal AI**: Use Gemini Vision to analyze car images
8. **Chat Interface**: Conversational car shopping assistant
