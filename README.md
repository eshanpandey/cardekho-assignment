# CarMatch - AI-Powered Car Recommendation Platform

An intelligent car recommendation system that helps confused car buyers find their perfect match using AI-powered analysis.

## 🚀 Features

- **AI-Powered Recommendations**: Uses Google Gemini AI to analyze preferences and suggest the best cars
- **Smart Filtering**: Pre-filters cars based on budget, fuel type, and transmission preferences
- **Detailed Insights**: Provides confidence scores, match explanations, strengths, and tradeoffs for each recommendation
- **Clean UI**: Simple, intuitive interface built with Next.js and Tailwind CSS
- **Fast API**: Python FastAPI backend with efficient SQL pre-filtering

## 🛠️ Tech Stack

**Frontend:**
- Next.js 15
- TypeScript
- Tailwind CSS

**Backend:**
- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite (demo) / PostgreSQL (production)
- Google Gemini AI API

## 📦 Project Structure

```
cardekho/
├── frontend/          # Next.js frontend
│   ├── app/          # Next.js app directory
│   └── package.json
├── backend/          # FastAPI backend
│   ├── api/         # API modules
│   ├── scripts/     # Database scripts
│   └── requirements.txt
└── README.md
```

## 🏃 Local Development

### Prerequisites
- Node.js 18+
- Python 3.11+
- Google Gemini API key

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your GEMINI_API_KEY to .env

# Initialize database
python -m scripts.init_db
python -m scripts.seed_data

# Run server
python -m api.main
# Backend runs on http://localhost:8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
# Frontend runs on http://localhost:3000
```

## 🚀 Deployment to Vercel

See [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deploy

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   ```

2. **Deploy Backend**:
   - Go to https://vercel.com/new
   - Import repository
   - Root Directory: `backend`
   - Add environment variables (GEMINI_API_KEY, etc.)
   - Deploy

3. **Deploy Frontend**:
   - Go to https://vercel.com/new
   - Import same repository
   - Root Directory: `frontend`
   - Add NEXT_PUBLIC_API_URL environment variable
   - Deploy

## 🧪 Testing

```bash
cd backend
pytest test_integration.py -v
```

## 📝 Environment Variables

### Backend (.env)
```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=models/gemini-2.5-flash
GEMINI_TEMPERATURE=0.4
GEMINI_MAX_TOKENS=16384
MAX_CANDIDATE_CARS=20
MIN_RECOMMENDATIONS=3
MAX_RECOMMENDATIONS=5
DATABASE_URL=sqlite:///./car_research.db
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## 🎯 Use Cases

1. **Safety-Conscious Family Buyer**: Prioritizes safety ratings and comfort
2. **Budget Fuel-Efficiency Seeker**: Focuses on mileage and value for money
3. **Performance Enthusiast**: Values engine power and driving dynamics
4. **Automatic Transmission Preference**: Filters for automatic/CVT only
5. **Balanced Buyer**: Considers all factors equally

## 🔧 API Endpoints

### POST /api/recommendations
Generate car recommendations based on user preferences.

**Request Body:**
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

**Response:**
```json
{
  "recommendations": [
    {
      "variant_id": 8,
      "confidence_score": 88,
      "match_explanation": "The Tata Nexon...",
      "strengths": ["Top safety rating", "Good mileage"],
      "tradeoffs": []
    }
  ],
  "count": 5,
  "total_candidates": 8
}
```

## 📊 Database Schema

- **makes**: Car manufacturers
- **models**: Car models
- **variants**: Specific car variants with specs
- **users**: User accounts
- **preference_profiles**: User preferences
- **shortlists**: Saved recommendations

## 🤝 Contributing

This is a portfolio/demo project. Feel free to fork and adapt for your needs.

## 📄 License

MIT License - feel free to use this project for learning or portfolio purposes.

## 🙏 Acknowledgments

- Google Gemini AI for intelligent recommendations
- FastAPI for the excellent Python web framework
- Next.js for the modern React framework
- Vercel for easy deployment

## 📧 Contact

Built by Eshan Pandey as a portfolio project demonstrating full-stack development with AI integration.
