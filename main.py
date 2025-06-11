"""
Backend API Server for ASN Automation Tool Configuration
Provides secure endpoints for email configuration management
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import os
import json
import secrets
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="ASN Automation Configuration API",
    description="Secure API for managing email configurations",
    version="1.0.0"
)

# Security
security = HTTPBearer()

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your app's domain
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Configuration models
class EmailConfig(BaseModel):
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    use_tls: bool = True
    use_ssl: bool = False
    from_email: EmailStr
    organization_name: str
    organization_code: str

class ConfigResponse(BaseModel):
    success: bool
    data: Optional[EmailConfig] = None
    message: str
    timestamp: datetime

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str

# Security configuration
API_KEY = os.getenv("API_KEY", "your-secret-api-key-change-this")
ADMIN_KEY = os.getenv("ADMIN_KEY", "your-admin-key-change-this")

# In-memory storage (in production, use a database)
config_store: Dict[str, EmailConfig] = {}

def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)) -> bool:
    """Verify the API key from the Authorization header"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key"
        )
    
    if credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    return True

def verify_admin_key(credentials: HTTPAuthorizationCredentials = Depends(security)) -> bool:
    """Verify the admin key for administrative operations"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing admin key"
        )
    
    if credentials.credentials != ADMIN_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin key"
        )
    
    return True

@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0"
    )

@app.get("/config/{organization_code}", response_model=ConfigResponse)
async def get_email_config(
    organization_code: str,
    _: bool = Depends(verify_api_key)
):
    """Get email configuration for a specific organization"""
    try:
        if organization_code not in config_store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Configuration not found for organization: {organization_code}"
            )
        
        config = config_store[organization_code]
        
        # Return configuration without sensitive data in logs
        return ConfigResponse(
            success=True,
            data=config,
            message="Configuration retrieved successfully",
            timestamp=datetime.utcnow()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/config/{organization_code}", response_model=ConfigResponse)
async def create_email_config(
    organization_code: str,
    config: EmailConfig,
    _: bool = Depends(verify_admin_key)
):
    """Create or update email configuration for an organization"""
    try:
        # Validate organization code matches
        if config.organization_code != organization_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization code mismatch"
            )
        
        # Store configuration
        config_store[organization_code] = config
        
        return ConfigResponse(
            success=True,
            data=config,
            message="Configuration created successfully",
            timestamp=datetime.utcnow()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.put("/config/{organization_code}", response_model=ConfigResponse)
async def update_email_config(
    organization_code: str,
    config: EmailConfig,
    _: bool = Depends(verify_admin_key)
):
    """Update existing email configuration"""
    try:
        if organization_code not in config_store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Configuration not found for organization: {organization_code}"
            )
        
        # Validate organization code matches
        if config.organization_code != organization_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization code mismatch"
            )
        
        # Update configuration
        config_store[organization_code] = config
        
        return ConfigResponse(
            success=True,
            data=config,
            message="Configuration updated successfully",
            timestamp=datetime.utcnow()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.delete("/config/{organization_code}")
async def delete_email_config(
    organization_code: str,
    _: bool = Depends(verify_admin_key)
):
    """Delete email configuration for an organization"""
    try:
        if organization_code not in config_store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Configuration not found for organization: {organization_code}"
            )
        
        del config_store[organization_code]
        
        return {
            "success": True,
            "message": f"Configuration deleted for organization: {organization_code}",
            "timestamp": datetime.utcnow()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/configs", response_model=Dict[str, str])
async def list_organizations(_: bool = Depends(verify_admin_key)):
    """List all organization codes with configurations"""
    try:
        return {
            "organizations": list(config_store.keys()),
            "count": len(config_store),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

if __name__ == "__main__":
    # Load initial configuration from environment or file
    initial_config = os.getenv("INITIAL_CONFIG")
    if initial_config:
        try:
            config_data = json.loads(initial_config)
            for org_code, config in config_data.items():
                config_store[org_code] = EmailConfig(**config)
        except Exception as e:
            print(f"Warning: Could not load initial configuration: {e}")
    
    # Run the server
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 