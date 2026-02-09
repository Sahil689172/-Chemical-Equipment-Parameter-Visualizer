"""
Quick test script to verify auth URLs are working
Run: python test_auth_urls.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equipment_api.settings')
django.setup()

from django.urls import resolve, reverse

print("Testing Auth URL Configuration...")
print("=" * 50)

# Test URL resolution
test_urls = [
    '/api/auth/register/',
    '/api/auth/login/',
    '/api/auth/logout/',
    '/api/auth/profile/',
]

for url in test_urls:
    try:
        match = resolve(url)
        print(f"[OK] {url}")
        print(f"  -> View: {match.func.__name__}")
        if hasattr(match.func, 'view_class'):
            print(f"  -> Class: {match.func.view_class.__name__}")
    except Exception as e:
        print(f"[ERROR] {url}")
        print(f"  -> ERROR: {e}")

print("\n" + "=" * 50)
print("Testing reverse URL lookup...")

try:
    register_url = reverse('register')
    print(f"[OK] reverse('register') = {register_url}")
except Exception as e:
    print(f"[ERROR] reverse('register') failed: {e}")

try:
    login_url = reverse('login')
    print(f"[OK] reverse('login') = {login_url}")
except Exception as e:
    print(f"[ERROR] reverse('login') failed: {e}")

print("\nIf all tests pass, restart your Django server!")
