from django.contrib import admin
from .models import EquipmentDataset, EquipmentItem


class EquipmentItemInline(admin.TabularInline):
    """Inline admin for EquipmentItem"""
    model = EquipmentItem
    extra = 0
    fields = ['equipment_name', 'type', 'flowrate', 'pressure', 'temperature']


@admin.register(EquipmentDataset)
class EquipmentDatasetAdmin(admin.ModelAdmin):
    list_display = ['id', 'filename', 'uploaded_at', 'get_item_count']
    list_filter = ['uploaded_at']
    search_fields = ['filename']
    inlines = [EquipmentItemInline]
    readonly_fields = ['uploaded_at']

    def get_item_count(self, obj):
        """Display count of equipment items"""
        return obj.equipment_items.count()
    get_item_count.short_description = 'Item Count'


@admin.register(EquipmentItem)
class EquipmentItemAdmin(admin.ModelAdmin):
    list_display = ['equipment_name', 'type', 'flowrate', 'pressure', 'temperature', 'dataset', 'created_at']
    list_filter = ['type', 'dataset', 'created_at']
    search_fields = ['equipment_name', 'type']
    readonly_fields = ['created_at']
