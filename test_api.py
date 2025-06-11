"""
Test script for the ASN Automation Backend API
Run this to test your deployed backend server
"""

import requests
import json
import sys

def test_backend_api(base_url: str, api_key: str, admin_key: str):
    """Test all backend API endpoints"""
    
    print(f"Testing backend API at: {base_url}")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: API documentation
    print("\n2. Testing API documentation...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            print("✅ API documentation accessible")
        else:
            print(f"❌ API documentation error: {response.status_code}")
    except Exception as e:
        print(f"❌ API documentation error: {e}")
    
    # Test 3: Create configuration (requires admin key)
    print("\n3. Testing configuration creation...")
    test_config = {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "smtp_username": "test@example.com",
        "smtp_password": "test-password",
        "use_tls": True,
        "use_ssl": False,
        "from_email": "test@example.com",
        "organization_name": "Test Organization",
        "organization_code": "TEST001"
    }
    
    try:
        headers = {"Authorization": f"Bearer {admin_key}"}
        response = requests.post(
            f"{base_url}/config/TEST001",
            json=test_config,
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Configuration created successfully")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Configuration creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Configuration creation error: {e}")
    
    # Test 4: Retrieve configuration (requires API key)
    print("\n4. Testing configuration retrieval...")
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(
            f"{base_url}/config/TEST001",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Configuration retrieved successfully")
            data = response.json()
            if data.get('success') and data.get('data'):
                config = data['data']
                print(f"   Organization: {config['organization_name']}")
                print(f"   SMTP Server: {config['smtp_server']}")
                print(f"   SMTP Port: {config['smtp_port']}")
        else:
            print(f"❌ Configuration retrieval failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Configuration retrieval error: {e}")
    
    # Test 5: List configurations (requires admin key)
    print("\n5. Testing configuration listing...")
    try:
        headers = {"Authorization": f"Bearer {admin_key}"}
        response = requests.get(
            f"{base_url}/configs",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Configuration listing successful")
            data = response.json()
            print(f"   Organizations: {data.get('organizations', [])}")
            print(f"   Count: {data.get('count', 0)}")
        else:
            print(f"❌ Configuration listing failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Configuration listing error: {e}")
    
    # Test 6: Delete test configuration (requires admin key)
    print("\n6. Testing configuration deletion...")
    try:
        headers = {"Authorization": f"Bearer {admin_key}"}
        response = requests.delete(
            f"{base_url}/config/TEST001",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Configuration deleted successfully")
        else:
            print(f"❌ Configuration deletion failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Configuration deletion error: {e}")
    
    print("\n" + "=" * 50)
    print("API testing completed!")
    return True

def main():
    """Main function to run the test"""
    
    # Get configuration from command line or use defaults
    if len(sys.argv) >= 4:
        base_url = sys.argv[1]
        api_key = sys.argv[2]
        admin_key = sys.argv[3]
    else:
        print("Usage: python test_api.py <base_url> <api_key> <admin_key>")
        print("Example: python test_api.py https://your-service.onrender.com your-api-key your-admin-key")
        print("\nOr enter the details interactively:")
        
        base_url = input("Backend URL: ").strip()
        if not base_url:
            print("❌ Backend URL is required")
            return
        
        api_key = input("API Key: ").strip()
        if not api_key:
            print("❌ API Key is required")
            return
        
        admin_key = input("Admin Key: ").strip()
        if not admin_key:
            print("❌ Admin Key is required")
            return
    
    # Run the test
    test_backend_api(base_url, api_key, admin_key)

if __name__ == "__main__":
    main() 