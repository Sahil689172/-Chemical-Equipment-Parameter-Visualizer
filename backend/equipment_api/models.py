from django.db import models
import json


class EquipmentDataset(models.Model):
    """Model to track uploaded equipment datasets"""
    id = models.AutoField(primary_key=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255)
    summary_json = models.JSONField(default=dict, help_text="Summary statistics in JSON format")

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Equipment Dataset"
        verbose_name_plural = "Equipment Datasets"

    def __str__(self):
        return f"{self.filename} (Uploaded: {self.uploaded_at.strftime('%Y-%m-%d %H:%M')})"


class EquipmentItem(models.Model):
    """Model for individual equipment items"""
    id = models.AutoField(primary_key=True)
    dataset = models.ForeignKey(
        EquipmentDataset,
        on_delete=models.CASCADE,
        related_name='equipment_items',
        help_text="The dataset this equipment belongs to"
    )
    equipment_name = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    flowrate = models.FloatField(help_text="Flowrate in L/min")
    pressure = models.FloatField(help_text="Pressure in bar")
    temperature = models.FloatField(help_text="Temperature in °C")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Equipment Item"
        verbose_name_plural = "Equipment Items"
        indexes = [
            models.Index(fields=['dataset', 'equipment_name']),
        ]

    def __str__(self):
        return f"{self.equipment_name} ({self.type})"
