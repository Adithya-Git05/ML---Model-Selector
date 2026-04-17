"""
Quick Start Testing Script

Run this script to quickly test all authentication endpoints.
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:5000"
COLORS = {
    'GREEN': '\033[92m',
    'RED': '\033[91m',
    'YELLOW': '\033[93m',
    'BLUE': '\033[94m',
    'END': '\033[0m'
}


def print_header(text):
    """Print formatted header"""
    print(f"\n{COLORS['BLUE']}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{COLORS['END']}\n")


def print_success(text):
    """Print success message"""
    print(f"{COLORS['GREEN']}✓ {text}{COLORS['END']}")


def print_error(text):
    """Print error message"""
    print(f"{COLORS['RED']}✗ {text}{COLORS['END']}")


def print_info(text):
    """Print info message"""
    print(f"{COLORS['YELLOW']}ℹ {text}{COLORS['END']}")


def print_response(response):
    """Print API response"""
    print("\nResponse:")
    print(json.dumps(response, indent=2, default=str))


def test_health_check():
    """Test health check endpoint"""
    print_header("Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print_success("Health check passed")
            print_response(response.json())
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Connection error: {str(e)}")
        return False


def test_registration():
    """Test user registration"""
    print_header("User Registration")
    
    data = {
        "email": f"test_{int(datetime.now().timestamp())}@gmail.com",
        "password": "TestPassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    print_info(f"Registering user: {data['email']}")
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
        print_info(f"Status Code: {response.status_code}")
        
        result = response.json()
        print_response(result)
        
        if response.status_code == 201 and result.get('success'):
            print_success("Registration successful")
            return result
        else:
            print_error("Registration failed")
            return None
    except Exception as e:
        print_error(f"Request error: {str(e)}")
        return None


def test_login(email, password):
    """Test user login"""
    print_header("User Login")
    
    data = {
        "email": email,
        "password": password
    }
    
    print_info(f"Logging in user: {email}")
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
        print_info(f"Status Code: {response.status_code}")
        
        result = response.json()
        print_response(result)
        
        if response.status_code == 200 and result.get('success'):
            print_success("Login successful")
            return result
        else:
            print_error("Login failed")
            return None
    except Exception as e:
        print_error(f"Request error: {str(e)}")
        return None


def test_verify_token(token):
    """Test token verification"""
    print_header("Token Verification")
    
    data = {"token": token}
    
    print_info("Verifying token...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/verify-token", json=data)
        print_info(f"Status Code: {response.status_code}")
        
        result = response.json()
        print_response(result)
        
        if response.status_code == 200 and result.get('success'):
            print_success("Token verification successful")
            return result
        else:
            print_error("Token verification failed")
            return None
    except Exception as e:
        print_error(f"Request error: {str(e)}")
        return None


def test_get_profile(token):
    """Test getting user profile"""
    print_header("Get User Profile")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print_info("Fetching user profile...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/users/profile", headers=headers)
        print_info(f"Status Code: {response.status_code}")
        
        result = response.json()
        print_response(result)
        
        if response.status_code == 200 and result.get('success'):
            print_success("Profile retrieved successfully")
            return result
        else:
            print_error("Failed to get profile")
            return None
    except Exception as e:
        print_error(f"Request error: {str(e)}")
        return None


def test_refresh_token(token):
    """Test token refresh"""
    print_header("Token Refresh")
    
    data = {"token": token}
    
    print_info("Refreshing token...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/refresh-token", json=data)
        print_info(f"Status Code: {response.status_code}")
        
        result = response.json()
        print_response(result)
        
        if response.status_code == 200 and result.get('success'):
            print_success("Token refreshed successfully")
            return result
        else:
            print_error("Token refresh failed")
            return None
    except Exception as e:
        print_error(f"Request error: {str(e)}")
        return None


def test_logout(token):
    """Test user logout"""
    print_header("User Logout")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print_info("Logging out user...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/logout", headers=headers)
        print_info(f"Status Code: {response.status_code}")
        
        result = response.json()
        print_response(result)
        
        if response.status_code == 200 and result.get('success'):
            print_success("Logout successful")
            return result
        else:
            print_error("Logout failed")
            return None
    except Exception as e:
        print_error(f"Request error: {str(e)}")
        return None


def test_invalid_login():
    """Test invalid login attempt"""
    print_header("Invalid Login Test")
    
    data = {
        "email": "nonexistent@example.com",
        "password": "WrongPassword123"
    }
    
    print_info("Attempting login with invalid credentials...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
        print_info(f"Status Code: {response.status_code}")
        
        result = response.json()
        print_response(result)
        
        if response.status_code == 401 and not result.get('success'):
            print_success("Invalid login correctly rejected")
            return True
        else:
            print_error("Invalid login not properly rejected")
            return False
    except Exception as e:
        print_error(f"Request error: {str(e)}")
        return False


def run_all_tests():
    """Run all tests"""
    print(f"\n{COLORS['BLUE']}")
    print("╔════════════════════════════════════════════════════════╗")
    print("║     AutoML Backend - API Testing Suite                ║")
    print("╚════════════════════════════════════════════════════════╝")
    print(f"{COLORS['END']}")
    
    print_info(f"Base URL: {BASE_URL}")
    print_info(f"Timestamp: {datetime.now().isoformat()}")
    
    # Test 1: Health Check
    if not test_health_check():
        print_error("Failed to connect to server. Make sure the backend is running.")
        print_info(f"Run: python app.py")
        return
    
    # Test 2: Registration
    registration = test_registration()
    if not registration:
        print_error("Registration test failed. Stopping tests.")
        return
    
    email = registration['user']['email']
    password = "TestPassword123"
    token = registration['token']
    
    # Test 3: Verify Registration Token
    test_verify_token(token)
    
    # Test 4: Get Profile with Registration Token
    test_get_profile(token)
    
    # Test 5: Login
    login = test_login(email, password)
    if not login:
        print_error("Login test failed. Stopping tests.")
        return
    
    token = login['token']
    
    # Test 6: Verify Login Token
    test_verify_token(token)
    
    # Test 7: Get Profile with Login Token
    test_get_profile(token)
    
    # Test 8: Refresh Token
    refresh = test_refresh_token(token)
    if refresh:
        new_token = refresh['token']
        test_verify_token(new_token)
    
    # Test 9: Logout
    test_logout(token)
    
    # Test 10: Invalid Login
    test_invalid_login()
    
    # Summary
    print_header("Test Summary")
    print_success("All tests completed!")
    print_info("Check the responses above for any failures.")


if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print_error("\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)
