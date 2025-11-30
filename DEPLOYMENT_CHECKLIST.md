# Quick Start - Deployment Checklist

## ✅ Your Project is Ready for Deployment!

All necessary files have been created and configured for deployment.

## Files Created/Modified:

1. ✅ `requirements.txt` - All Python dependencies
2. ✅ `Procfile` - Instructions for web servers
3. ✅ `build.sh` - Build script for Render
4. ✅ `.gitignore` - Excludes unnecessary files from Git
5. ✅ `.env.example` - Environment variables template
6. ✅ `settings.py` - Updated for production
7. ✅ `DEPLOYMENT.md` - Complete deployment guide
8. ✅ `staticfiles/` - Static files collected

## Next Steps:

### Option 1: Deploy to Render (Recommended - Easiest)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Prepare for deployment"
   git remote add origin https://github.com/yourusername/your-repo.git
   git push -u origin main
   ```

2. **Go to [render.com](https://render.com) and sign up**

3. **Create New Web Service:**
   - Connect your GitHub repository
   - Set Build Command: `./build.sh`
   - Set Start Command: `gunicorn recommendationSystem.wsgi:application`

4. **Add Environment Variables:**
   ```
   SECRET_KEY=<generate-new-key>
   DEBUG=False
   ```

5. **Deploy and wait 5-10 minutes**

### Option 2: Deploy to Railway

1. Push code to GitHub (same as above)
2. Go to [railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Add environment variables (SECRET_KEY, DEBUG)
5. Generate domain

### Option 3: Deploy to PythonAnywhere

See detailed instructions in `DEPLOYMENT.md`

## Generate SECRET_KEY:

Run this command to generate a secure SECRET_KEY:
```bash
D:/E-commerce_recommendation_system/myenv/Scripts/python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Important Notes:

- ⚠️ **Always use a NEW SECRET_KEY in production**
- ⚠️ **Set DEBUG=False in production**
- ⚠️ **Add your domain to ALLOWED_HOSTS**
- ⚠️ **Don't commit .env file with secrets**

## Full Documentation:

Read `DEPLOYMENT.md` for comprehensive deployment instructions for all platforms.

## Test Locally with Production Settings:

```bash
# Set environment variables temporarily (PowerShell)
$env:SECRET_KEY="your-generated-key"
$env:DEBUG="False"
$env:ALLOWED_HOSTS="localhost,127.0.0.1"

# Run with gunicorn
D:/E-commerce_recommendation_system/myenv/Scripts/gunicorn.exe recommendationSystem.wsgi:application
```

---

**Need help?** Check `DEPLOYMENT.md` for troubleshooting tips!
