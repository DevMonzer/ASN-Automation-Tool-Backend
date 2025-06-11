# ASN Automation Tool Backend

A secure FastAPI backend server for managing email configurations for the ASN Automation Tool.

## 🚀 Features

- **Secure API**: Bearer token authentication with separate API and admin keys
- **Email Configuration Management**: CRUD operations for SMTP configurations
- **Organization Support**: Multi-organization configuration management
- **Automatic Documentation**: Interactive API docs at `/docs`
- **Health Monitoring**: Built-in health check endpoints
- **Input Validation**: Automatic Pydantic validation
- **CORS Support**: Configurable cross-origin requests

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

## 🛠️ Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/DevMonzer/ASN-Automation-Tool-Backend.git
   cd ASN-Automation-Tool-Backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   ```bash
   # Create a .env file or set environment variables
   export API_KEY="your-secret-api-key-change-this"
   export ADMIN_KEY="your-admin-key-change-this"
   export PORT=8000
   ```

4. **Run the server**
   ```bash
   python main.py
   ```

5. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Production Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed deployment instructions to Render.com.

## 🔑 API Authentication

The API uses Bearer token authentication with two types of keys:

- **API Key**: For regular operations (retrieving configurations)
- **Admin Key**: For administrative operations (creating, updating, deleting configurations)

### Generate Secure Keys

```python
import secrets

# Generate API key
api_key = secrets.token_urlsafe(32)
print(f"API Key: {api_key}")

# Generate admin key
admin_key = secrets.token_urlsafe(32)
print(f"Admin Key: {admin_key}")
```

## 📡 API Endpoints

### Health Check
- **GET** `/health` - Server health status
- **GET** `/` - Root endpoint (same as health)

### Configuration Management
- **GET** `/config/{organization_code}` - Retrieve configuration (requires API key)
- **POST** `/config/{organization_code}` - Create configuration (requires admin key)
- **PUT** `/config/{organization_code}` - Update configuration (requires admin key)
- **DELETE** `/config/{organization_code}` - Delete configuration (requires admin key)
- **GET** `/configs` - List all organizations (requires admin key)

## 📊 Data Models

### EmailConfig
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

### Response Format
```json
{
  "success": true,
  "data": {
    // EmailConfig object
  },
  "message": "Operation completed successfully",
  "timestamp": "2024-01-01T12:00:00"
}
```

## 🧪 Testing

### Using the Test Script

```bash
# Test with command line arguments
python test_api.py https://your-service.onrender.com your-api-key your-admin-key

# Interactive testing
python test_api.py
```

### Manual Testing

1. **Test Health Endpoint**
   ```bash
   curl https://your-service.onrender.com/health
   ```

2. **Create Configuration** (requires admin key)
   ```bash
   curl -X POST "https://your-service.onrender.com/config/TEST001" \
     -H "Authorization: Bearer your-admin-key" \
     -H "Content-Type: application/json" \
     -d '{
       "smtp_server": "smtp.gmail.com",
       "smtp_port": 587,
       "smtp_username": "test@example.com",
       "smtp_password": "test-password",
       "use_tls": true,
       "use_ssl": false,
       "from_email": "test@example.com",
       "organization_name": "Test Organization",
       "organization_code": "TEST001"
     }'
   ```

3. **Retrieve Configuration** (requires API key)
   ```bash
   curl -H "Authorization: Bearer your-api-key" \
     https://your-service.onrender.com/config/TEST001
   ```

## 🔒 Security Features

- **Bearer Token Authentication**: Secure API key validation
- **Input Validation**: Automatic Pydantic validation for all inputs
- **HTTPS Enforcement**: All production communications encrypted
- **CORS Protection**: Configurable cross-origin request handling
- **Error Handling**: Secure error responses without sensitive data exposure

## 📁 Project Structure

```
backend/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── test_api.py         # API testing script
├── README.md           # This file
└── DEPLOYMENT_GUIDE.md # Deployment instructions
```

## 🚀 Deployment

### Quick Deploy to Render

1. **Fork/Clone this repository**
2. **Generate API keys** (see above)
3. **Deploy to Render**:
   - Go to [Render.com](https://render.com)
   - Create new Web Service
   - Connect your GitHub repository
   - Set environment variables:
     - `API_KEY`: Your generated API key
     - `ADMIN_KEY`: Your generated admin key
     - `PORT`: 10000
4. **Test deployment** using the test script

For detailed instructions, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEY` | API key for regular operations | `your-secret-api-key-change-this` |
| `ADMIN_KEY` | Admin key for administrative operations | `your-admin-key-change-this` |
| `PORT` | Server port | `8000` |
| `INITIAL_CONFIG` | JSON string of initial configurations | None |

### Example Initial Configuration

```bash
export INITIAL_CONFIG='{
  "400418": {
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
}'
```

## 📈 Monitoring

### Health Checks
- **Endpoint**: `/health`
- **Response**: Server status and version information
- **Use Case**: External monitoring and load balancers

### Logs
- **Development**: Console output
- **Production**: Render dashboard logs
- **Monitoring**: Track API usage and errors

## 🆘 Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify API keys are correct
   - Check environment variables
   - Ensure keys are not exposed in logs

2. **Connection Issues**
   - Check server URL
   - Verify network connectivity
   - Test with health endpoint

3. **Validation Errors**
   - Check request format
   - Verify required fields
   - Review API documentation

### Getting Help

- **Documentation**: Check `/docs` endpoint for interactive API docs
- **Issues**: Create an issue on GitHub
- **Contact**: dev.monzer@gmail.com

## 📄 License

This project is part of the ASN Automation Tool suite.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Note**: This backend is designed to work with the ASN Automation Tool desktop application. For integration instructions, see the main project documentation. 