from django.core.management.base import BaseCommand
import csv
import json
from pathlib import Path
from django.db.models import Avg, Max, Min, Count
from equipment_api.models import EquipmentDataset, EquipmentItem


class Command(BaseCommand):
    help = 'Load equipment data from CSV file into a dataset'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Path to CSV file',
            nargs='?',
            default=None
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        if not csv_file:
            # Default to sample data
            csv_file = Path(__file__).parent.parent.parent.parent.parent / 'sample_data' / 'sample_equipment_data.csv'
        
        csv_path = Path(csv_file)
        
        if not csv_path.exists():
            self.stdout.write(self.style.ERROR(f'CSV file not found: {csv_path}'))
            return
        
        self.stdout.write(f'Loading equipment data from {csv_path}...')
        
        # Create dataset
        dataset = EquipmentDataset.objects.create(
            filename=csv_path.name
        )
        
        # Load equipment items
        items = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                item = EquipmentItem(
                    dataset=dataset,
                    equipment_name=row['Equipment Name'],
                    type=row['Type'],
                    flowrate=float(row['Flowrate']),
                    pressure=float(row['Pressure']),
                    temperature=float(row['Temperature'])
                )
                items.append(item)
        
        # Bulk create items
        EquipmentItem.objects.bulk_create(items)
        
        # Calculate summary statistics
        items_queryset = dataset.equipment_items.all()
        summary = {
            'total_items': items_queryset.count(),
            'equipment_types': list(items_queryset.values_list('type', flat=True).distinct()),
            'avg_flowrate': items_queryset.aggregate(Avg('flowrate'))['flowrate__avg'] or 0,
            'avg_pressure': items_queryset.aggregate(Avg('pressure'))['pressure__avg'] or 0,
            'avg_temperature': items_queryset.aggregate(Avg('temperature'))['temperature__avg'] or 0,
            'max_flowrate': items_queryset.aggregate(Max('flowrate'))['flowrate__max'] or 0,
            'min_flowrate': items_queryset.aggregate(Min('flowrate'))['flowrate__min'] or 0,
            'max_pressure': items_queryset.aggregate(Max('pressure'))['pressure__max'] or 0,
            'min_pressure': items_queryset.aggregate(Min('pressure'))['pressure__min'] or 0,
            'max_temperature': items_queryset.aggregate(Max('temperature'))['temperature__max'] or 0,
            'min_temperature': items_queryset.aggregate(Min('temperature'))['temperature__min'] or 0,
        }
        
        # Update dataset with summary
        dataset.summary_json = summary
        dataset.save()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded {len(items)} equipment items into dataset {dataset.id}. '
                f'Total datasets: {EquipmentDataset.objects.count()}, '
                f'Total equipment items: {EquipmentItem.objects.count()}'
            )
        )
