from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EquipmentDatasetViewSet, EquipmentItemViewSet, UploadCSVView,
    RegisterView, LoginView, LogoutView, UserProfileView
)

router = DefaultRouter()
router.register(r'datasets', EquipmentDatasetViewSet, basename='dataset')
router.register(r'equipment', EquipmentItemViewSet, basename='equipment')

urlpatterns = [
    # Authentication endpoints (must be before router to avoid conflicts)
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    # Equipment endpoints
    path('upload/', UploadCSVView.as_view(), name='upload-csv'),
    path('', include(router.urls)),
]
