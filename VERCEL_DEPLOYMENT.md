# Vercel Deployment Guide

## Option 1: Deploy Backend and Frontend Separately (Recommended)

This approach gives you more control and better performance.

### Step 1: Deploy Backend to Vercel

1. **Create a GitHub repository** (if not already done):
   ```bash
   cd /Users/eshanpandey/cardekho
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   # Create repo on GitHub, then:
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy Backend**:
   - Go to https://vercel.com/new
   - Import your GitHub repository
   - **Root Directory**: `backend`
   - **Framework Preset**: Other
   - Click "Deploy"

3. **Add Environment Variables** (in Vercel dashboard):
   - `GEMINI_API_KEY`: Your Gemini API key
   - `GEMINI_MODEL`: models/gemini-2.5-flash
   - `GEMINI_TEMPERATURE`: 0.4
   - `GEMINI_MAX_TOKENS`: 16384
   - `MAX_CANDIDATE_CARS`: 20
   - `MIN_RECOMMENDATIONS`: 3
   - `MAX_RECOMMENDATIONS`: 5
   - `DATABASE_URL`: sqlite:///./car_research.db
   - `CORS_ORIGINS`: *

4. **Copy Backend URL**: e.g., `https://cardekho-backend.vercel.app`

### Step 2: Deploy Frontend to Vercel

1. **Deploy Frontend**:
   - Go to https://vercel.com/new
   - Import the same GitHub repository
   - **Root Directory**: `frontend`
   - **Framework Preset**: Next.js
   - Click "Deploy"

2. **Add Environment Variable**:
   - `NEXT_PUBLIC_API_URL`: Your backend URL from Step 1 (e.g., `https://cardekho-backend.vercel.app/api`)

3. **Redeploy** to pick up the environment variable

### Step 3: Update Backend CORS

1. Go to backend project in Vercel
2. Update `CORS_ORIGINS` environment variable:
   - Value: `https://your-frontend-url.vercel.app,http://localhost:3000`
3. Redeploy backend

### Step 4: Initialize Database

**Important**: Vercel's serverless functions are stateless, so SQLite won't persist between requests. You have two options:

#### Option A: Use Vercel Postgres (Recommended for Production)
1. In Vercel dashboard, go to Storage → Create Database → Postgres
2. Update your backend code to use PostgreSQL instead of SQLite
3. Vercel will automatically inject the connection string

#### Option B: Keep SQLite (Demo/Testing Only)
- SQLite will work but data won't persist between deployments
- Good enough for a portfolio demo
- Database will be re-initialized on each cold start

## Option 2: Monorepo Deployment (Single Project)

Deploy both frontend and backend from a single Vercel project:

1. **Deploy to Vercel**:
   - Go to https://vercel.com/new
   - Import your GitHub repository
   - **Root Directory**: Leave empty (use root)
   - **Framework Preset**: Next.js
   - Vercel will detect the `vercel.json` at root

2. **Add Environment Variables**:
   - All backend environment variables (GEMINI_API_KEY, etc.)
   - `NEXT_PUBLIC_API_URL`: `/api`

3. **Deploy**

## Quick Deploy Commands

If you have Vercel CLI installed:

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy backend
cd backend
vercel --prod

# Deploy frontend
cd ../frontend
vercel --prod
```

## Testing Deployment

After deployment:

1. Visit your frontend URL
2. Fill out the preference form
3. Click "Get Recommendations"
4. Verify you get AI-powered recommendations

## Troubleshooting

### Backend Issues
- **500 Error**: Check Vercel function logs for errors
- **Database Error**: SQLite may not persist on Vercel serverless
- **Timeout**: Gemini API calls may take 30+ seconds, increase function timeout in vercel.json

### Frontend Issues
- **API Error**: Check that `NEXT_PUBLIC_API_URL` is set correctly
- **CORS Error**: Update backend `CORS_ORIGINS` to include frontend URL

### Database Persistence
If you need persistent data:
1. Use Vercel Postgres (recommended)
2. Use external database (Supabase, PlanetScale, Neon)
3. Use Vercel Blob storage for SQLite file

## Production Recommendations

For a production-ready deployment:

1. **Switch to PostgreSQL**:
   - Vercel Postgres (easiest)
   - Supabase (free tier)
   - Neon (serverless Postgres)

2. **Update SQLAlchemy connection**:
   ```python
   # In database.py
   DATABASE_URL = os.getenv("POSTGRES_URL", "sqlite:///./car_research.db")
   ```

3. **Add connection pooling** for PostgreSQL

4. **Increase function timeout** in vercel.json:
   ```json
   {
     "functions": {
       "backend/api/main.py": {
         "maxDuration": 60
       }
     }
   }
   ```

## Cost

- **Vercel Hobby Plan**: Free
  - Unlimited deployments
  - 100GB bandwidth/month
  - Serverless function execution included
  
- **Vercel Pro Plan**: $20/month (if you need more)
  - More bandwidth
  - Longer function execution time
  - Team collaboration

- **Gemini API**: Pay-as-you-go (very cheap for demos)

**Total for demo**: $0/month ✨
