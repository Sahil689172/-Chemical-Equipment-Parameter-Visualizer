from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipmentDatasetViewSet, EquipmentItemViewSet, UploadCSVView

router = DefaultRouter()
router.register(r'datasets', EquipmentDatasetViewSet, basename='dataset')
router.register(r'equipment', EquipmentItemViewSet, basename='equipment')

urlpatterns = [
    path('upload/', UploadCSVView.as_view(), name='upload-csv'),
    path('', include(router.urls)),
]
