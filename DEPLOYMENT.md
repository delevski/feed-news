# 🚀 Deployment Guide - Vercel

## Deploy to Vercel

### Step 1: Install Vercel CLI (Optional)
```bash
npm i -g vercel
```

### Step 2: Set Environment Variables

In Vercel Dashboard, add these environment variables:

1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add:
   - **Name:** `COHERE_API_KEY`
   - **Value:** `your_cohere_api_key_here`

### Step 3: Deploy

**Option A: Using Vercel Dashboard**
1. Go to [vercel.com](https://vercel.com)
2. Click "Import Project"
3. Import from GitHub: `https://github.com/delevski/feed-news`
4. Vercel will auto-detect the configuration
5. Click "Deploy"

**Option B: Using Vercel CLI**
```bash
vercel
```

### Step 4: Test Your Deployment

After deployment, your API will be available at:
```
https://your-project.vercel.app/api/health
https://your-project.vercel.app/api/news?range=daily&limit=30
```

## API Endpoints (Production)

Replace `https://your-project.vercel.app` with your actual Vercel URL:

```bash
# Health Check
curl https://your-project.vercel.app/api/health

# Get Daily News
curl "https://your-project.vercel.app/api/news?range=daily&limit=30"

# Get Only Papers
curl "https://your-project.vercel.app/api/news/papers"

# Get Only Spaces
curl "https://your-project.vercel.app/api/news/spaces"

# Get Only Repos
curl "https://your-project.vercel.app/api/news/repos"
```

## Configuration Files

### `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api.py"
    }
  ]
}
```

### Environment Variables
- `COHERE_API_KEY` - Required for AI summaries

## Troubleshooting

### Issue: Missing handler or app
**Solution:** Make sure `api.py` exports the Flask `app` object at module level.

### Issue: Module not found
**Solution:** Check `requirements.txt` includes all dependencies.

### Issue: Timeout errors
**Solution:** Vercel has a 10-second timeout for serverless functions. Consider:
- Reducing the `limit` parameter
- Caching results
- Using Vercel Pro for longer timeouts

### Issue: Cold starts
**Solution:** First request might be slow. Subsequent requests will be faster.

## Performance Tips

1. **Use lower limits:** `?limit=10` instead of `?limit=100`
2. **Cache responses:** Consider adding caching layer
3. **Upgrade to Vercel Pro:** For longer execution times
4. **Use webhooks:** For scheduled tasks instead of long-running requests

## Alternative: Deploy as Cron Job

For scheduled news fetching, use Vercel Cron Jobs:

Create `vercel.json` with:
```json
{
  "crons": [{
    "path": "/api/news?range=daily&limit=30",
    "schedule": "0 8 * * *"
  }]
}
```

This will fetch news daily at 8 AM UTC.

## Support

- Vercel Docs: https://vercel.com/docs
- Python Runtime: https://vercel.com/docs/functions/serverless-functions/runtimes/python

---

**Your API is now production-ready!** 🎉

