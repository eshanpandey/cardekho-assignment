# Car Research Platform - Backend

FastAPI backend with SQLite database and Gemini AI integration.

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 4. Initialize Database

```bash
python scripts/init_db.py
```

### 5. Seed Sample Data

```bash
python scripts/seed_data.py
```

## Database Schema

### Tables

1. **makes** - Car manufacturers (Honda, Maruti, etc.)
2. **models** - Car models (City, Swift, etc.)
3. **variants** - Specific variants with full specs
4. **users** - User accounts
5. **preference_profiles** - User preferences for recommendations
6. **shortlists** - Generated recommendations

### Relationships

```
Make (1) ──→ (N) Model (1) ──→ (N) Variant
User (1) ──→ (N) PreferenceProfile (1) ──→ (N) Shortlist
Shortlist (N) ──→ (1) Variant
```

## Sample Data

The seed script includes 5 popular Indian car brands:
- Maruti Suzuki Swift (2 variants)
- Honda City (2 variants)
- Hyundai Verna (2 variants)
- Tata Nexon (2 variants)
- Mahindra XUV700 (2 variants)

Total: 5 makes, 5 models, 10 variants

## Database Operations

### View Database

```bash
sqlite3 car_research.db
.tables
.schema variants
SELECT * FROM makes;
.quit
```

### Reset Database

```bash
rm car_research.db
python scripts/init_db.py
python scripts/seed_data.py
```

## Next Steps

- [ ] Create Pydantic schemas
- [ ] Implement API routes
- [ ] Integrate Gemini API
- [ ] Add recommendation engine
- [ ] Create FastAPI main app
