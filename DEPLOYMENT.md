# Deployment Guide

## Prerequisites
- GitHub account
- Vercel account (sign up at vercel.com)
- Render account (sign up at render.com) OR Railway account

## Step 1: Push to GitHub

```bash
cd /Users/eshanpandey/cardekho
git init
git add .
git commit -m "Initial commit - Car recommendation platform MVP"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

## Step 2: Deploy Backend to Render

1. Go to https://render.com and sign in
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: cardekho-backend
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variables:
   - `GEMINI_API_KEY`: Your Gemini API key
   - `GEMINI_MODEL`: models/gemini-2.5-flash
   - `GEMINI_TEMPERATURE`: 0.4
   - `GEMINI_MAX_TOKENS`: 16384
   - `MAX_CANDIDATE_CARS`: 20
   - `MIN_RECOMMENDATIONS`: 3
   - `MAX_RECOMMENDATIONS`: 5
   - `DATABASE_URL`: sqlite:///./car_research.db
   - `CORS_ORIGINS`: https://your-frontend-url.vercel.app
6. Click "Create Web Service"
7. Wait for deployment (5-10 minutes)
8. Copy the deployed URL (e.g., https://cardekho-backend.onrender.com)

## Step 3: Deploy Frontend to Vercel

1. Go to https://vercel.com and sign in
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
5. Add Environment Variable:
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: Your backend URL from Step 2 (e.g., https://cardekho-backend.onrender.com)
6. Click "Deploy"
7. Wait for deployment (2-3 minutes)
8. Your app is live! 🎉

## Step 4: Update Backend CORS

After frontend is deployed:
1. Go back to Render dashboard
2. Update the `CORS_ORIGINS` environment variable with your Vercel URL
3. Example: `https://cardekho.vercel.app,http://localhost:3000`
4. Render will automatically redeploy

## Step 5: Initialize Database on Render

The database needs to be seeded with initial data:

1. Go to Render dashboard → Your service → "Shell"
2. Run these commands:
```bash
python -m scripts.init_db
python -m scripts.seed_data
```

Alternatively, you can use Render's "Run Command" feature to execute these on startup.

## Alternative: Deploy Backend to Railway

If you prefer Railway over Render:

1. Go to https://railway.app and sign in
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Python
5. Add environment variables (same as Render)
6. Set root directory to `backend` in settings
7. Deploy!

## Troubleshooting

### Backend Issues
- Check logs in Render/Railway dashboard
- Verify all environment variables are set
- Ensure database is initialized with seed data

### Frontend Issues
- Check Vercel deployment logs
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check browser console for CORS errors

### CORS Errors
- Update backend `CORS_ORIGINS` to include your Vercel URL
- Make sure there's no trailing slash in URLs

## Local Development

Frontend:
```bash
cd frontend
npm run dev
```

Backend:
```bash
cd backend
source venv/bin/activate
python -m api.main
```

## Cost Estimate

- **Vercel**: Free tier (sufficient for demo/portfolio)
- **Render**: Free tier (may sleep after inactivity, takes ~30s to wake)
- **Railway**: $5/month credit (free tier available)
- **Gemini API**: Pay-as-you-go (very cheap for demo usage)

**Total**: $0-5/month for a live demo

## Production Considerations

For a production app, consider:
1. Use PostgreSQL instead of SQLite
2. Add authentication/user management
3. Implement rate limiting
4. Add monitoring (Sentry, LogRocket)
5. Use a CDN for static assets
6. Add caching (Redis)
7. Implement proper error tracking
