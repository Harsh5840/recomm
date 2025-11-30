# Deployment Guide for E-commerce Recommendation System

This guide covers deployment options for your Django e-commerce recommendation system on various platforms.

## Prerequisites

Before deploying, ensure:
- Your code is pushed to a Git repository (GitHub, GitLab, or Bitbucket)
- All files in this project are committed:
  - `requirements.txt`
  - `Procfile`
  - `build.sh`
  - `.gitignore`
  - Updated `settings.py`

## Deployment Options

### 1. Deploy on Render (Recommended - Free Tier Available)

Render offers a free tier and is easy to set up.

#### Steps:

1. **Sign up at [render.com](https://render.com)**

2. **Create a New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub/GitLab repository
   - Select your repository

3. **Configure the Service**
   - **Name**: `ecommerce-recommendation-system`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn recommendationSystem.wsgi:application`
   - **Instance Type**: `Free` (or paid if needed)

4. **Add Environment Variables**
   - Click "Environment" tab
   - Add these variables:
     ```
     SECRET_KEY=your-super-secret-key-here-change-this
     DEBUG=False
     ALLOWED_HOSTS=your-app-name.onrender.com
     ```
   - Generate a secure SECRET_KEY using: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your app will be live at `https://your-app-name.onrender.com`

---

### 2. Deploy on Railway (Free Tier Available)

Railway provides $5 free credit per month.

#### Steps:

1. **Sign up at [railway.app](https://railway.app)**

2. **Create a New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Settings**
   - Railway will auto-detect Django
   - Go to "Variables" tab and add:
     ```
     SECRET_KEY=your-super-secret-key-here-change-this
     DEBUG=False
     ```

4. **Generate Domain**
   - Go to "Settings" tab
   - Click "Generate Domain"
   - Your app will be accessible at the generated URL

5. **Deploy**
   - Railway will automatically deploy
   - Check logs to ensure successful deployment

---

### 3. Deploy on PythonAnywhere (Beginner-Friendly, Free Tier)

PythonAnywhere is great for Django apps with a simple free tier.

#### Steps:

1. **Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)**

2. **Upload Your Code**
   - Open a Bash console
   - Clone your repository:
     ```bash
     git clone https://github.com/yourusername/E-commerce_recommendation_system.git
     cd E-commerce_recommendation_system
     ```

3. **Create Virtual Environment**
   ```bash
   python3.11 -m venv myenv
   source myenv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration" with Python 3.11
   - Set source code directory: `/home/yourusername/E-commerce_recommendation_system`
   - Set virtualenv path: `/home/yourusername/E-commerce_recommendation_system/myenv`

5. **Configure WSGI File**
   - Click on WSGI configuration file link
   - Replace content with:
     ```python
     import os
     import sys
     
     path = '/home/yourusername/E-commerce_recommendation_system'
     if path not in sys.path:
         sys.path.append(path)
     
     os.environ['DJANGO_SETTINGS_MODULE'] = 'recommendationSystem.settings'
     
     from django.core.wsgi import get_wsgi_application
     application = get_wsgi_application()
     ```

6. **Set Environment Variables**
   - In WSGI file, add before imports:
     ```python
     os.environ['SECRET_KEY'] = 'your-super-secret-key-here'
     os.environ['DEBUG'] = 'False'
     os.environ['ALLOWED_HOSTS'] = 'yourusername.pythonanywhere.com'
     ```

7. **Collect Static Files**
   - In Bash console:
     ```bash
     cd ~/E-commerce_recommendation_system
     source myenv/bin/activate
     python manage.py collectstatic
     python manage.py migrate
     ```

8. **Configure Static Files**
   - In "Web" tab, add static files mapping:
     - URL: `/static/`
     - Directory: `/home/yourusername/E-commerce_recommendation_system/staticfiles/`

9. **Reload Web App**
   - Click "Reload" button
   - Visit `https://yourusername.pythonanywhere.com`

---

### 4. Deploy on Heroku

Heroku is a popular platform but no longer offers a free tier.

#### Steps:

1. **Install Heroku CLI**
   - Download from [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   cd E-commerce_recommendation_system
   heroku create your-app-name
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY="your-super-secret-key"
   heroku config:set DEBUG=False
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Run Migrations**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py collectstatic --noinput
   ```

7. **Open App**
   ```bash
   heroku open
   ```

---

## Important Security Notes

### Generate a New SECRET_KEY

For production, always use a unique SECRET_KEY. Generate one:

**Python:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**PowerShell:**
```powershell
D:/E-commerce_recommendation_system/myenv/Scripts/python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Environment Variables Checklist

Set these on your deployment platform:
- `SECRET_KEY` - Your generated secret key
- `DEBUG` - Set to `False` in production
- `ALLOWED_HOSTS` - Your domain (e.g., `yourapp.onrender.com`)

---

## Troubleshooting

### Static Files Not Loading
- Ensure `python manage.py collectstatic` was run
- Check `STATIC_ROOT` and `STATIC_URL` in settings.py
- Verify WhiteNoise is installed: `pip install whitenoise`

### Database Issues
- Run migrations: `python manage.py migrate`
- Check database file permissions (for SQLite)

### Import Errors
- Ensure all dependencies are in `requirements.txt`
- Check that Python version matches (3.11)

### Server Won't Start
- Check logs on your deployment platform
- Verify `gunicorn` is installed
- Ensure `Procfile` has correct syntax

---

## Post-Deployment

After successful deployment:

1. **Test Your App**: Visit your deployed URL
2. **Monitor Logs**: Check platform logs for errors
3. **Set Up Custom Domain** (optional): Most platforms allow custom domain mapping
4. **Enable HTTPS**: Most platforms provide free SSL certificates

---

## Recommended Platform Comparison

| Platform | Free Tier | Ease of Use | Build Time | Best For |
|----------|-----------|-------------|------------|----------|
| **Render** | ✅ Yes | ⭐⭐⭐⭐⭐ | ~5 min | Most users |
| **Railway** | ✅ $5/mo credit | ⭐⭐⭐⭐⭐ | ~3 min | Quick deploys |
| **PythonAnywhere** | ✅ Yes | ⭐⭐⭐⭐ | ~10 min | Beginners |
| **Heroku** | ❌ No | ⭐⭐⭐⭐ | ~5 min | Enterprises |

**Recommendation**: Start with **Render** for the best free tier and ease of use.

---

## Need Help?

If you encounter issues:
1. Check platform-specific documentation
2. Review deployment logs
3. Verify all environment variables are set
4. Ensure your repository is up-to-date

Good luck with your deployment! 🚀
