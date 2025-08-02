# 🚀 LinkedIn Post Generator - Deployment Guide

## Option 1: Deploy on Render (FREE) ⭐ Recommended

### Steps:
1. **Create GitHub Repository:**
   - Push your code to GitHub
   - Make sure all files are committed

2. **Go to Render.com:**
   - Sign up with GitHub account
   - Click "New Web Service"
   - Connect your GitHub repo

3. **Configure Settings:**
   - **Name:** linkedin-post-generator
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Port:** 5000

4. **Add Environment Variable:**
   - Key: `GROQ_API_KEY`
   - Value: Your actual GROQ API key

5. **Deploy:**
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment

## Option 2: Deploy on Railway

### Steps:
1. Go to railway.app
2. Sign up with GitHub
3. Click "Deploy from GitHub repo"
4. Select your repo
5. Add GROQ_API_KEY environment variable
6. Deploy!

## Option 3: Deploy on PythonAnywhere

### Steps:
1. Create account on pythonanywhere.com
2. Upload your files via Files tab
3. Create a new web app (Flask)
4. Configure WSGI file
5. Add environment variables
6. Reload and test

## 💡 Before Deployment:

1. **Make sure your .env file is NOT committed to GitHub**
2. **Add .gitignore file:**
   ```
   .env
   __pycache__/
   *.pyc
   ```

3. **Test locally:**
   ```bash
   python app.py
   ```

## 🔑 Environment Variables Needed:
- `GROQ_API_KEY`: Your Groq API key

## 📁 Required Files:
- ✅ app.py
- ✅ requirements.txt  
- ✅ runtime.txt
- ✅ gunicorn.conf.py
- ✅ templates/index.html
- ✅ static/css/styles.css
- ✅ static/js/app.js
- ✅ All your Python modules (post_generator.py, few_shot.py, etc.)

## 🎉 After Deployment:
Your app will be live at:
- Render: `https://your-app-name.onrender.com`
- Railway: `https://your-app-name.up.railway.app`
- PythonAnywhere: `https://yourusername.pythonanywhere.com`

## 🐛 Troubleshooting:
- Check logs in your hosting platform
- Ensure all dependencies are in requirements.txt
- Verify environment variables are set
- Make sure data/processed_posts.json exists
