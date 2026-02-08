from rest_framework import serializers
from .models import EquipmentDataset, EquipmentItem


class EquipmentItemSerializer(serializers.ModelSerializer):
    """Serializer for EquipmentItem model"""
    class Meta:
        model = EquipmentItem
        fields = ['id', 'dataset', 'equipment_name', 'type', 'flowrate', 'pressure', 'temperature', 'created_at']
        read_only_fields = ['id', 'created_at']


class EquipmentDatasetSerializer(serializers.ModelSerializer):
    """Serializer for EquipmentDataset model"""
    equipment_items = EquipmentItemSerializer(many=True, read_only=True)
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = EquipmentDataset
        fields = ['id', 'uploaded_at', 'filename', 'summary_json', 'equipment_items', 'item_count']
        read_only_fields = ['id', 'uploaded_at']

    def get_item_count(self, obj):
        """Get the count of equipment items in this dataset"""
        return obj.equipment_items.count()
