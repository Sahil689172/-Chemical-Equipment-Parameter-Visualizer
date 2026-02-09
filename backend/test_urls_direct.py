"""
Direct test of URL configuration
Run this while server is running to verify URLs are loaded
"""
import requests

print("Testing Auth Endpoints...")
print("=" * 50)

# Test register endpoint
try:
    response = requests.get('http://127.0.0.1:8000/api/auth/register/')
    if response.status_code == 200:
        print("[OK] GET /api/auth/register/ - Working!")
        print(f"Response: {response.json()}")
    elif response.status_code == 404:
        print("[ERROR] GET /api/auth/register/ - 404 Not Found")
        print("Server is running OLD CODE - RESTART REQUIRED!")
    else:
        print(f"[WARNING] GET /api/auth/register/ - Status {response.status_code}")
except Exception as e:
    print(f"[ERROR] Could not connect: {e}")

print("\n" + "=" * 50)
print("If you see 404, RESTART your Django server!")
