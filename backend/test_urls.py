#!/usr/bin/env python
"""Quick script to test if URLs are registered correctly"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equipment_api.settings')
django.setup()

from django.urls import reverse
from rest_framework.routers import DefaultRouter
from equipment_api.views import EquipmentDatasetViewSet

router = DefaultRouter()
router.register(r'datasets', EquipmentDatasetViewSet, basename='dataset')

print("Registered URLs:")
for url_pattern in router.urls:
    print(f"  {url_pattern.pattern} -> {url_pattern.name}")

# Test if chart-data action is registered
try:
    url = reverse('dataset-chart-data', kwargs={'pk': 1})
    print(f"\nChart data URL for dataset 1: {url}")
except Exception as e:
    print(f"\nError getting chart-data URL: {e}")
