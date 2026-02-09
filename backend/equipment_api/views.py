import pandas as pd
from collections import defaultdict
from django.db import models, transaction
from django.db.models import Avg, Max, Min, Count
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action, parser_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import EquipmentDataset, EquipmentItem
from .serializers import (
    EquipmentDatasetSerializer, EquipmentItemSerializer,
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer
)


class EquipmentDatasetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing equipment datasets.
    """
    queryset = EquipmentDataset.objects.all().order_by('-uploaded_at')
    serializer_class = EquipmentDatasetSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        GET /api/datasets/
        List all datasets (last 5) with id, filename, uploaded_at, summary
        """
        # Get last 5 datasets
        datasets = self.get_queryset()[:5]
        
        result = []
        for dataset in datasets:
            summary = dataset.summary_json or {}
            result.append({
                'id': dataset.id,
                'filename': dataset.filename,
                'uploaded_at': dataset.uploaded_at,
                'summary': summary
            })
        
        return Response(result)

    def retrieve(self, request, *args, **kwargs):
        """
        GET /api/datasets/<id>/
        Get specific dataset details including all equipment items
        """
        dataset = self.get_object()
        items = dataset.equipment_items.all()
        
        items_serializer = EquipmentItemSerializer(items, many=True)
        
        return Response({
            'id': dataset.id,
            'filename': dataset.filename,
            'uploaded_at': dataset.uploaded_at,
            'summary': dataset.summary_json or {},
            'equipment_items': items_serializer.data
        })

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """
        GET /api/datasets/<id>/summary/
        Get summary statistics only
        """
        dataset = self.get_object()
        summary = dataset.summary_json or {}
        
        # Format summary in the requested format
        formatted_summary = {
            'dataset_id': dataset.id,
            'filename': dataset.filename,
            'total_count': summary.get('total_equipment_count', 0),
            'averages': {
                'flowrate': summary.get('average_flowrate', 0),
                'pressure': summary.get('average_pressure', 0),
                'temperature': summary.get('average_temperature', 0)
            },
            'type_distribution': summary.get('equipment_type_distribution', {})
        }
        
        return Response(formatted_summary)

    @action(detail=True, methods=['get'])
    def chart_data(self, request, pk=None):
        """
        GET /api/datasets/<id>/chart-data/
        Return data formatted for Chart.js
        Group by equipment type and calculate averages per type
        """
        dataset = self.get_object()
        items = dataset.equipment_items.all()
        
        # Group by equipment type and calculate averages
        type_data = defaultdict(lambda: {'flowrates': [], 'pressures': [], 'temperatures': [], 'count': 0})
        
        for item in items:
            type_data[item.type]['flowrates'].append(item.flowrate)
            type_data[item.type]['pressures'].append(item.pressure)
            type_data[item.type]['temperatures'].append(item.temperature)
            type_data[item.type]['count'] += 1
        
        # Calculate averages per type - simplified format
        labels = []
        flowrate_data = []
        pressure_data = []
        temperature_data = []
        
        for eq_type, data in sorted(type_data.items()):
            labels.append(eq_type)
            
            # Calculate averages
            avg_flowrate = sum(data['flowrates']) / len(data['flowrates']) if data['flowrates'] else 0
            avg_pressure = sum(data['pressures']) / len(data['pressures']) if data['pressures'] else 0
            avg_temperature = sum(data['temperatures']) / len(data['temperatures']) if data['temperatures'] else 0
            
            flowrate_data.append(round(avg_flowrate, 2))
            pressure_data.append(round(avg_pressure, 2))
            temperature_data.append(round(avg_temperature, 2))
        
        chart_data = {
            'labels': labels,
            'flowrate': flowrate_data,
            'pressure': pressure_data,
            'temperature': temperature_data
        }
        
        return Response(chart_data)

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        """Get all equipment items for a specific dataset"""
        dataset = self.get_object()
        items = dataset.equipment_items.all()
        serializer = EquipmentItemSerializer(items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get statistics about all datasets"""
        queryset = self.get_queryset()
        stats = {
            'total_datasets': queryset.count(),
            'total_equipment_items': EquipmentItem.objects.count(),
        }
        return Response(stats)


class EquipmentItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing equipment items.
    """
    queryset = EquipmentItem.objects.all()
    serializer_class = EquipmentItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Optionally filter by dataset"""
        queryset = EquipmentItem.objects.all()
        dataset_id = self.request.query_params.get('dataset', None)
        if dataset_id is not None:
            queryset = queryset.filter(dataset_id=dataset_id)
        return queryset

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get statistics about equipment items"""
        queryset = self.get_queryset()
        stats = {
            'total_items': queryset.count(),
            'equipment_types': list(queryset.values_list('type', flat=True).distinct()),
            'avg_flowrate': queryset.aggregate(models.Avg('flowrate'))['flowrate__avg'] or 0,
            'avg_pressure': queryset.aggregate(models.Avg('pressure'))['pressure__avg'] or 0,
            'avg_temperature': queryset.aggregate(models.Avg('temperature'))['temperature__avg'] or 0,
        }
        return Response(stats)


class UploadCSVView(APIView):
    permission_classes = [IsAuthenticated]
    """
    API endpoint for uploading and parsing CSV files containing equipment data.
    """
    parser_classes = [MultiPartParser, FormParser]
    
    REQUIRED_COLUMNS = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    
    def post(self, request, *args, **kwargs):
        """
        Handle CSV file upload, parse data, and create dataset with equipment items.
        """
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided. Please upload a CSV file.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        csv_file = request.FILES['file']
        
        # Validate file extension
        if not csv_file.name.endswith('.csv'):
            return Response(
                {'error': 'Invalid file type. Please upload a CSV file.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Read CSV file using pandas
            df = pd.read_csv(csv_file)
            
            # Validate required columns
            missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
            if missing_columns:
                return Response(
                    {
                        'error': f'Missing required columns: {", ".join(missing_columns)}',
                        'required_columns': self.REQUIRED_COLUMNS,
                        'found_columns': list(df.columns)
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate data types and non-empty values
            errors = []
            for idx, row in df.iterrows():
                row_num = idx + 2  # +2 because index is 0-based and we skip header
                
                # Check for empty required fields
                if pd.isna(row['Equipment Name']) or str(row['Equipment Name']).strip() == '':
                    errors.append(f'Row {row_num}: Equipment Name is required')
                
                if pd.isna(row['Type']) or str(row['Type']).strip() == '':
                    errors.append(f'Row {row_num}: Type is required')
                
                # Validate numeric fields
                try:
                    flowrate = float(row['Flowrate'])
                    pressure = float(row['Pressure'])
                    temperature = float(row['Temperature'])
                except (ValueError, TypeError):
                    errors.append(f'Row {row_num}: Flowrate, Pressure, and Temperature must be numeric')
            
            if errors:
                return Response(
                    {
                        'error': 'Data validation failed',
                        'errors': errors[:10]  # Limit to first 10 errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Process data in a transaction
            with transaction.atomic():
                # Create dataset
                dataset = EquipmentDataset.objects.create(
                    filename=csv_file.name
                )
                
                # Prepare equipment items for bulk creation
                equipment_items = []
                for _, row in df.iterrows():
                    item = EquipmentItem(
                        dataset=dataset,
                        equipment_name=str(row['Equipment Name']).strip(),
                        type=str(row['Type']).strip(),
                        flowrate=float(row['Flowrate']),
                        pressure=float(row['Pressure']),
                        temperature=float(row['Temperature'])
                    )
                    equipment_items.append(item)
                
                # Bulk create equipment items
                EquipmentItem.objects.bulk_create(equipment_items)
                
                # Calculate summary statistics
                items_queryset = dataset.equipment_items.all()
                
                # Equipment type distribution
                type_distribution = {
                    item['type']: item['count']
                    for item in items_queryset.values('type')
                    .annotate(count=Count('id'))
                }
                
                # Create summary in the requested format
                summary = {
                    'total_equipment_count': items_queryset.count(),
                    'average_flowrate': round(
                        items_queryset.aggregate(Avg('flowrate'))['flowrate__avg'] or 0, 2
                    ),
                    'average_pressure': round(
                        items_queryset.aggregate(Avg('pressure'))['pressure__avg'] or 0, 2
                    ),
                    'average_temperature': round(
                        items_queryset.aggregate(Avg('temperature'))['temperature__avg'] or 0, 2
                    ),
                    'equipment_type_distribution': type_distribution,
                    # Additional statistics for detailed view
                    'max_flowrate': round(
                        items_queryset.aggregate(Max('flowrate'))['flowrate__max'] or 0, 2
                    ),
                    'min_flowrate': round(
                        items_queryset.aggregate(Min('flowrate'))['flowrate__min'] or 0, 2
                    ),
                    'max_pressure': round(
                        items_queryset.aggregate(Max('pressure'))['pressure__max'] or 0, 2
                    ),
                    'min_pressure': round(
                        items_queryset.aggregate(Min('pressure'))['pressure__min'] or 0, 2
                    ),
                    'max_temperature': round(
                        items_queryset.aggregate(Max('temperature'))['temperature__max'] or 0, 2
                    ),
                    'min_temperature': round(
                        items_queryset.aggregate(Min('temperature'))['temperature__min'] or 0, 2
                    ),
                }
                
                # Update dataset with summary
                dataset.summary_json = summary
                dataset.save()
                
                # Keep only last 5 datasets (delete older ones)
                all_datasets = EquipmentDataset.objects.all().order_by('-uploaded_at')
                if all_datasets.count() > 5:
                    datasets_to_delete = all_datasets[5:]
                    for old_dataset in datasets_to_delete:
                        # Delete associated equipment items first
                        old_dataset.equipment_items.all().delete()
                        old_dataset.delete()
            
            # Return success response
            return Response(
                {
                    'success': True,
                    'message': f'Successfully uploaded and processed {len(equipment_items)} equipment items',
                    'dataset_id': dataset.id,
                    'filename': dataset.filename,
                    'uploaded_at': dataset.uploaded_at,
                    'summary': summary
                },
                status=status.HTTP_201_CREATED
            )
            
        except pd.errors.EmptyDataError:
            return Response(
                {'error': 'The CSV file is empty or invalid.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except pd.errors.ParserError as e:
            return Response(
                {'error': f'Error parsing CSV file: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'An error occurred while processing the file: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RegisterView(APIView):
    """User registration endpoint"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Return endpoint information for testing"""
        return Response({
            'message': 'Registration endpoint is working',
            'method': 'POST',
            'required_fields': ['username', 'email', 'password', 'password_confirm'],
            'optional_fields': ['first_name', 'last_name']
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'User registered successfully',
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """User login endpoint"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Return endpoint information for testing"""
        return Response({
            'message': 'Login endpoint is working',
            'method': 'POST',
            'required_fields': ['username', 'password']
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Login successful',
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """User logout endpoint"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """Get current user profile"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
