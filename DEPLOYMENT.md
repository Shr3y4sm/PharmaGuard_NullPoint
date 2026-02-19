# 🚀 PharmaGuard Deployment Guide

This guide provides comprehensive instructions for deploying PharmaGuard to various platforms.

## 📋 Table of Contents

- [Pre-Deployment Checklist](#pre-deployment-checklist)
- [Local Deployment](#local-deployment)
- [Heroku Deployment](#heroku-deployment)
- [AWS Elastic Beanstalk](#aws-elastic-beanstalk)
- [Azure App Service](#azure-app-service)
- [Google Cloud Platform](#google-cloud-platform)
- [Docker Deployment](#docker-deployment)
- [Production Best Practices](#production-best-practices)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)

---

## ✅ Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- [ ] Python 3.9+ installed
- [ ] All dependencies listed in `requirements.txt`
- [ ] CPIC data file (`data/cpic_gene-drug_pairs.xlsx`)
- [ ] `.env` file configured (use `.env.example` as template)
- [ ] Tested application locally

---

## 🏠 Local Deployment

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Shr3y4sm/PharmaGuard_NullPoint.git
cd PharmaGuard_NullPoint

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 5. Run the application
python app.py
```

The application will be available at `http://localhost:5000`

### Running with Gunicorn (Production Server)

```bash
# Install Gunicorn
pip install gunicorn

# Run with 4 worker processes
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

---

## 🔷 Heroku Deployment

### Prerequisites
- Heroku account ([Sign up](https://signup.heroku.com/))
- Heroku CLI installed ([Download](https://devcenter.heroku.com/articles/heroku-cli))

### Step 1: Create Required Files

**Procfile** (create in root directory):
```
web: gunicorn app:app
```

**runtime.txt** (specify Python version):
```
python-3.11.0
```

### Step 2: Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create new Heroku app
heroku create pharmaguard-app

# Add environment variables
heroku config:set GOOGLE_API_KEY=your_api_key_here

# Deploy
git push heroku main

# Open the app
heroku open
```

### Step 3: Scale Dynos (Optional)

```bash
# Scale to 2 web dynos
heroku ps:scale web=2
```

### Monitoring

```bash
# View logs
heroku logs --tail

# Check app status
heroku ps
```

---

## 🟠 AWS Elastic Beanstalk

### Prerequisites
- AWS account
- EB CLI installed: `pip install awsebcli`

### Step 1: Initialize EB

```bash
# Initialize Elastic Beanstalk
eb init -p python-3.11 pharmaguard-app

# Create environment
eb create pharmaguard-env
```

### Step 2: Configure Environment Variables

```bash
# Set environment variables
eb setenv GOOGLE_API_KEY=your_api_key_here
eb setenv FLASK_ENV=production
```

### Step 3: Deploy

```bash
# Deploy application
eb deploy

# Open in browser
eb open
```

### EB Configuration

Create `.ebextensions/01_flask.config`:

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: app:app
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: "/var/app/current:$PYTHONPATH"
```

---

## 🔵 Azure App Service

### Prerequisites
- Azure account
- Azure CLI installed

### Step 1: Create Resources

```bash
# Login to Azure
az login

# Create resource group
az group create --name pharmaguard-rg --location eastus

# Create App Service plan
az appservice plan create --name pharmaguard-plan --resource-group pharmaguard-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group pharmaguard-rg --plan pharmaguard-plan --name pharmaguard-app --runtime "PYTHON:3.11"
```

### Step 2: Configure Deployment

```bash
# Configure deployment from local Git
az webapp deployment source config-local-git --name pharmaguard-app --resource-group pharmaguard-rg

# Get deployment URL
az webapp deployment list-publishing-credentials --name pharmaguard-app --resource-group pharmaguard-rg
```

### Step 3: Set Environment Variables

```bash
# Set API key
az webapp config appsettings set --resource-group pharmaguard-rg --name pharmaguard-app --settings GOOGLE_API_KEY=your_api_key_here

# Set startup command
az webapp config set --resource-group pharmaguard-rg --name pharmaguard-app --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"
```

### Step 4: Deploy

```bash
# Add Azure remote
git remote add azure <deployment_url>

# Push to Azure
git push azure main
```

---

## 🟢 Google Cloud Platform

### Prerequisites
- GCP account with billing enabled
- `gcloud` CLI installed

### Step 1: Create App Engine Application

```bash
# Login to GCP
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Create App Engine app
gcloud app create --region=us-central
```

### Step 2: Create app.yaml

Create `app.yaml` in root directory:

```yaml
runtime: python311

env_variables:
  GOOGLE_API_KEY: "your_api_key_here"
  FLASK_ENV: "production"

handlers:
- url: /static
  static_dir: static

- url: /.*
  script: auto

automatic_scaling:
  target_cpu_utilization: 0.65
  min_instances: 1
  max_instances: 10
```

### Step 3: Deploy

```bash
# Deploy to App Engine
gcloud app deploy

# View logs
gcloud app logs tail -s default

# Open in browser
gcloud app browse
```

---

## 🐳 Docker Deployment

### Step 1: Create Dockerfile

Create `Dockerfile` in root directory:

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]
```

### Step 2: Create docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - FLASK_ENV=production
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

### Step 3: Build and Run

```bash
# Build image
docker build -t pharmaguard:latest .

# Run container
docker run -d -p 5000:5000 --env-file .env --name pharmaguard pharmaguard:latest

# Or use docker-compose
docker-compose up -d
```

### Step 4: Deploy to Docker Hub (Optional)

```bash
# Tag image
docker tag pharmaguard:latest yourusername/pharmaguard:latest

# Push to Docker Hub
docker push yourusername/pharmaguard:latest
```

---

## 🛡️ Production Best Practices

### Security

1. **Use HTTPS**: Always enable SSL/TLS in production
   ```bash
   # Heroku example
   heroku certs:auto:enable
   ```

2. **Environment Variables**: Never commit `.env` to Git
   ```bash
   # Add to .gitignore
   echo ".env" >> .gitignore
   ```

3. **Secret Key**: Generate strong secret key
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

4. **CORS Configuration**: Restrict origins in production
   ```python
   from flask_cors import CORS
   CORS(app, origins=["https://yourdomain.com"])
   ```

### Performance

1. **Use Gunicorn**: Replace Flask dev server
   ```bash
   gunicorn --workers 4 --worker-class sync --bind 0.0.0.0:5000 app:app
   ```

2. **Worker Calculation**: `(2 x CPU cores) + 1`

3. **Timeout Settings**: Increase for LLM requests
   ```bash
   gunicorn --timeout 120 app:app
   ```

4. **Caching**: Implement Redis for frequent operations

### Monitoring

1. **Logging**: Configure structured logging
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   ```

2. **Error Tracking**: Use services like Sentry
   ```bash
   pip install sentry-sdk[flask]
   ```

3. **Health Checks**: Add `/health` endpoint
   ```python
   @app.route('/health')
   def health():
       return jsonify({"status": "healthy"}), 200
   ```

### Backup

1. **CPIC Data**: Backup `cpic_gene-drug_pairs.xlsx`
2. **Database**: Implement regular backups if using DB
3. **User Data**: Encrypt sensitive information

---

## 🔐 Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Gemini API key | `AIzaSyD...` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | `production` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `5000` |
| `MAX_FILE_SIZE_MB` | Max upload size | `5` |
| `SECRET_KEY` | Flask secret key | Auto-generated |

### Setting Variables by Platform

**Heroku:**
```bash
heroku config:set GOOGLE_API_KEY=your_key
```

**AWS:**
```bash
eb setenv GOOGLE_API_KEY=your_key
```

**Azure:**
```bash
az webapp config appsettings set --settings GOOGLE_API_KEY=your_key
```

**Docker:**
```bash
docker run -e GOOGLE_API_KEY=your_key ...
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError"
**Solution**: Install all dependencies
```bash
pip install -r requirements.txt
```

#### 2. "API Key Invalid"
**Solution**: Verify your Google API key
```bash
# Test API key
curl -H "Content-Type: application/json" -d '{"contents":[{"parts":[{"text":"test"}]}]}' -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=YOUR_API_KEY"
```

#### 3. "File Too Large" Error
**Solution**: Check `MAX_CONTENT_LENGTH` in app.py
```python
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB
```

#### 4. "CPIC Data Not Found"
**Solution**: Ensure file exists and path is correct
```bash
ls -la data/cpic_gene-drug_pairs.xlsx
```

#### 5. Port Already in Use
**Solution**: Change port or kill existing process
```bash
# Find process on port 5000
lsof -ti:5000

# Kill process
kill -9 $(lsof -ti:5000)

# Or use different port
flask run --port 5001
```

### Debug Mode

Enable debug mode for detailed error messages:

```python
# In app.py (development only!)
app.config['DEBUG'] = True
```

### Logs

**Heroku:**
```bash
heroku logs --tail
```

**AWS:**
```bash
eb logs --all
```

**Azure:**
```bash
az webapp log tail --name pharmaguard-app --resource-group pharmaguard-rg
```

**Docker:**
```bash
docker logs -f pharmaguard
```

---

## 📞 Support

If you encounter issues during deployment:

1. Check the [GitHub Issues](https://github.com/Shr3y4sm/PharmaGuard_NullPoint/issues)
2. Review application logs
3. Verify environment variables
4. Contact: your.email@example.com

---

## 📚 Additional Resources

- [Flask Deployment Options](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Heroku Python Guide](https://devcenter.heroku.com/categories/python-support)
- [AWS Elastic Beanstalk Python](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html)
- [Azure App Service Python](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python)
- [GCP App Engine Python](https://cloud.google.com/appengine/docs/standard/python3)

---

**Last Updated**: February 2026  
**Version**: 1.0.0
