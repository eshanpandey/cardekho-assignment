# 🚀 Deploy to Vercel Now

Your code is live on GitHub: https://github.com/eshanpandey/cardekho-assignment

## Quick Deploy Steps

### 1. Deploy Backend

1. Go to https://vercel.com/new
2. Click "Import Git Repository"
3. Select `eshanpandey/cardekho-assignment`
4. Configure:
   - **Project Name**: `cardekho-backend`
   - **Framework Preset**: Other
   - **Root Directory**: `backend`
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty

5. **Add Environment Variables** (click "Environment Variables"):
   ```
   GEMINI_API_KEY=<your-gemini-api-key>
   GEMINI_MODEL=models/gemini-2.5-flash
   GEMINI_TEMPERATURE=0.4
   GEMINI_MAX_TOKENS=16384
   MAX_CANDIDATE_CARS=20
   MIN_RECOMMENDATIONS=3
   MAX_RECOMMENDATIONS=5
   DATABASE_URL=sqlite:///./car_research.db
   CORS_ORIGINS=*
   ```

6. Click **Deploy**
7. Wait 2-3 minutes
8. **Copy your backend URL** (e.g., `https://cardekho-backend.vercel.app`)

### 2. Deploy Frontend

1. Go to https://vercel.com/new again
2. Click "Import Git Repository"
3. Select `eshanpandey/cardekho-assignment` again
4. Configure:
   - **Project Name**: `cardekho-frontend`
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

5. **Add Environment Variable**:
   ```
   NEXT_PUBLIC_API_URL=<your-backend-url-from-step-1>/api
   ```
   Example: `https://cardekho-backend.vercel.app/api`

6. Click **Deploy**
7. Wait 2-3 minutes
8. **Your app is live!** 🎉

### 3. Update Backend CORS

1. Go back to your backend project in Vercel
2. Go to Settings → Environment Variables
3. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://your-frontend-url.vercel.app,http://localhost:3000
   ```
   Example: `https://cardekho-frontend.vercel.app,http://localhost:3000`

4. Go to Deployments → Click "..." → Redeploy

### 4. Initialize Database

The database will be automatically initialized on first request. The seed data is included in the deployment.

## ✅ Test Your Deployment

1. Visit your frontend URL (e.g., `https://cardekho-frontend.vercel.app`)
2. Fill out the preference form
3. Click "Get Recommendations"
4. You should see AI-powered recommendations! 🚗✨

## 🐛 Troubleshooting

### Backend Issues
- **Check Logs**: Vercel Dashboard → Your Backend Project → Deployments → Click on deployment → View Function Logs
- **Verify Environment Variables**: Settings → Environment Variables
- **Common Issue**: Missing GEMINI_API_KEY

### Frontend Issues
- **Check Logs**: Vercel Dashboard → Your Frontend Project → Deployments → Click on deployment → View Build Logs
- **Verify API URL**: Settings → Environment Variables → Check NEXT_PUBLIC_API_URL
- **Common Issue**: Wrong API URL format (should end with `/api`)

### CORS Errors
- Update backend `CORS_ORIGINS` to include your frontend URL
- Redeploy backend after updating

### API Timeout
- Gemini API can take 30-60 seconds
- This is normal for the first request (cold start)
- Subsequent requests will be faster

## 📊 Monitor Your App

- **Vercel Analytics**: Automatically enabled
- **Function Logs**: Available in Vercel dashboard
- **Error Tracking**: Check function logs for errors

## 💰 Cost

- **Vercel Hobby Plan**: FREE
- **Gemini API**: Pay-as-you-go (~$0.01 per 100 requests)
- **Total**: Essentially free for demo/portfolio

## 🎯 Next Steps

After deployment:
1. Test all features
2. Share the link on your portfolio
3. Add screenshots to README
4. Consider adding more car data
5. Optionally migrate to PostgreSQL for persistence

## 📝 Your URLs

After deployment, update these:
- **Frontend**: https://cardekho-frontend.vercel.app
- **Backend**: https://cardekho-backend.vercel.app
- **GitHub**: https://github.com/eshanpandey/cardekho-assignment

---

**Need Help?** Check the Vercel documentation or the detailed guide in VERCEL_DEPLOYMENT.md
