# Backend Server Deployment Guide

This guide will help you deploy the ASN Automation backend server to Render.com for free.

## Prerequisites

1. A GitHub account
2. A Render.com account (free)
3. Basic understanding of APIs

## Step 1: Prepare Your Backend Code

### 1.1 Create a GitHub Repository

1. Create a new repository on GitHub
2. Upload the `backend/` folder contents to your repository
3. Make sure you have these files:
   - `main.py` (FastAPI server)
   - `requirements.txt` (dependencies)
   - `README.md` (optional)

### 1.2 Generate Secure API Keys

Generate secure API keys for your application:

```python
import secrets

# Generate API key
api_key = secrets.token_urlsafe(32)
print(f"API Key: {api_key}")

# Generate admin key
admin_key = secrets.token_urlsafe(32)
print(f"Admin Key: {admin_key}")
```

**Save these keys securely!** You'll need them for configuration.

## Step 2: Deploy to Render

### 2.1 Create a New Web Service

1. Go to [Render.com](https://render.com) and sign up/login
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:

**Basic Settings:**
- **Name**: `asn-automation-backend` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)
- **Root Directory**: Leave empty (if backend is in root) or specify `backend/`

**Build Settings:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python main.py`

### 2.2 Configure Environment Variables

In your Render service settings, add these environment variables:

```
API_KEY=your-generated-api-key-here
ADMIN_KEY=your-generated-admin-key-here
PORT=10000
```

**Important Security Notes:**
- Use the API keys you generated in step 1.2
- Never commit these keys to your repository
- Keep them secure and private

### 2.3 Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy your service
3. Wait for the build to complete (usually 2-5 minutes)
4. Your service will be available at: `https://your-service-name.onrender.com`

## Step 3: Test Your Deployment

### 3.1 Test Health Endpoint

Visit your service URL to test the health endpoint:
```
https://your-service-name.onrender.com/health
```

You should see a JSON response like:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "version": "1.0.0"
}
```

### 3.2 Test API Documentation

Visit the automatic API documentation:
```
https://your-service-name.onrender.com/docs
```

This will show you all available endpoints and allow you to test them.

## Step 4: Configure Your Desktop App

### 4.1 Update Configuration

Update your `config.py` file with your deployed server URL:

```python
# Replace with your actual Render service URL
BACKEND_BASE_URL = "https://your-service-name.onrender.com"
BACKEND_API_KEY = "your-generated-api-key-here"
```

### 4.2 Test Connection

Use the configuration client to test the connection:

```python
from utils.config_client import initialize_config_client, test_server_connection

# Initialize the client
client = initialize_config_client(
    base_url="https://your-service-name.onrender.com",
    api_key="your-generated-api-key-here"
)

# Test connection
if test_server_connection():
    print("✅ Backend server connection successful!")
else:
    print("❌ Backend server connection failed!")
```

## Step 5: Add Initial Configuration

### 5.1 Using the API Documentation

1. Go to `https://your-service-name.onrender.com/docs`
2. Click "Authorize" and enter your admin key
3. Use the POST `/config/{organization_code}` endpoint to add your first configuration

### 5.2 Example Configuration

```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "smtp_username": "your-email@gmail.com",
  "smtp_password": "your-app-password",
  "use_tls": true,
  "use_ssl": false,
  "from_email": "your-email@gmail.com",
  "organization_name": "Your Organization",
  "organization_code": "400418"
}
```

## Security Best Practices

### 1. API Key Security
- Generate strong, random API keys
- Never expose API keys in client-side code
- Rotate keys regularly
- Use different keys for different environments

### 2. HTTPS Only
- Always use HTTPS in production
- Render provides HTTPS automatically
- Never send sensitive data over HTTP

### 3. Input Validation
- The FastAPI server includes automatic validation
- Always validate organization codes
- Sanitize all inputs

### 4. Rate Limiting
- Consider adding rate limiting for production
- Monitor API usage
- Set up alerts for unusual activity

## Monitoring and Maintenance

### 1. Render Dashboard
- Monitor your service in the Render dashboard
- Check logs for errors
- Monitor resource usage

### 2. Health Checks
- The `/health` endpoint provides basic health monitoring
- Set up external monitoring if needed
- Monitor response times

### 3. Logs
- Check Render logs for errors
- Monitor API usage patterns
- Set up alerts for critical errors

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check `requirements.txt` for correct dependencies
   - Ensure Python version compatibility
   - Check build logs in Render dashboard

2. **Connection Timeouts**
   - Render services sleep after 15 minutes of inactivity
   - First request after sleep may take 30-60 seconds
   - Consider using a paid plan for always-on service

3. **Authentication Errors**
   - Verify API keys are correct
   - Check environment variables in Render
   - Ensure keys are not exposed in logs

4. **CORS Issues**
   - Update CORS settings in `main.py` if needed
   - Add your app's domain to allowed origins

## Next Steps

1. **Database Integration**: Consider adding a database for persistent storage
2. **Enhanced Security**: Add rate limiting and additional security measures
3. **Monitoring**: Set up comprehensive monitoring and alerting
4. **Scaling**: Upgrade to paid plans for better performance and reliability

## Support

If you encounter issues:
1. Check Render documentation: https://render.com/docs
2. Review FastAPI documentation: https://fastapi.tiangolo.com/
3. Check service logs in Render dashboard
4. Test endpoints using the automatic API documentation 