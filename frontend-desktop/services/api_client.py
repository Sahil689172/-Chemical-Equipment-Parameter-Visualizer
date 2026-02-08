"""
API Client for Chemical Equipment Visualizer Desktop App
Handles all communication with Django REST API backend
"""

import requests
from typing import Optional, Dict, List, Any
import os


class APIClient:
    """Client for interacting with the Django REST API"""
    
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
        self.timeout = 30
    
    def upload_csv(self, file_path: str) -> Dict[str, Any]:
        """
        Upload a CSV file to the backend
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            Response data from the API
            
        Raises:
            requests.RequestException: If the request fails
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'text/csv')}
            response = requests.post(
                f"{self.base_url}/upload/",
                files=files,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
    
    def get_datasets(self) -> List[Dict[str, Any]]:
        """
        Get list of all datasets (last 5)
        
        Returns:
            List of dataset dictionaries
        """
        response = requests.get(
            f"{self.base_url}/datasets/",
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def get_dataset(self, dataset_id: int) -> Dict[str, Any]:
        """
        Get specific dataset details
        
        Args:
            dataset_id: ID of the dataset
            
        Returns:
            Dataset details dictionary
        """
        response = requests.get(
            f"{self.base_url}/datasets/{dataset_id}/",
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def get_dataset_summary(self, dataset_id: int) -> Dict[str, Any]:
        """
        Get dataset summary statistics
        
        Args:
            dataset_id: ID of the dataset
            
        Returns:
            Summary statistics dictionary
        """
        response = requests.get(
            f"{self.base_url}/datasets/{dataset_id}/summary/",
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def get_chart_data(self, dataset_id: int) -> Dict[str, Any]:
        """
        Get chart data for a dataset
        
        Args:
            dataset_id: ID of the dataset
            
        Returns:
            Chart data dictionary
        """
        response = requests.get(
            f"{self.base_url}/datasets/{dataset_id}/chart-data/",
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def get_equipment_items(self, dataset_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get equipment items, optionally filtered by dataset
        
        Args:
            dataset_id: Optional dataset ID to filter by
            
        Returns:
            List of equipment item dictionaries
        """
        url = f"{self.base_url}/equipment/"
        if dataset_id:
            url += f"?dataset={dataset_id}"
        
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        
        # Handle paginated response
        if isinstance(data, dict) and 'results' in data:
            return data['results']
        return data if isinstance(data, list) else []
    
    def delete_dataset(self, dataset_id: int) -> bool:
        """
        Delete a dataset
        
        Args:
            dataset_id: ID of the dataset to delete
            
        Returns:
            True if successful
        """
        response = requests.delete(
            f"{self.base_url}/datasets/{dataset_id}/",
            timeout=self.timeout
        )
        response.raise_for_status()
        return True
    
    def test_connection(self) -> bool:
        """
        Test connection to the API
        
        Returns:
            True if connection is successful
        """
        try:
            response = requests.get(
                f"{self.base_url}/datasets/",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
