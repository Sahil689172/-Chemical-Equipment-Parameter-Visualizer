"""
API Client for Chemical Equipment Visualizer Desktop App
Handles all communication with Django REST API backend
"""

import requests
from typing import Optional, Dict, List, Any
import os
import json


class APIClient:
    """Client for interacting with the Django REST API"""
    
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
        self.timeout = 30
        self.token = None
        self.token_file = os.path.join(os.path.expanduser("~"), ".chemviz_token")
        self.load_token()
    
    def load_token(self):
        """Load token from file if it exists"""
        try:
            if os.path.exists(self.token_file):
                with open(self.token_file, 'r') as f:
                    data = json.load(f)
                    self.token = data.get('token')
        except:
            self.token = None
    
    def save_token(self, token: str):
        """Save token to file"""
        self.token = token
        try:
            with open(self.token_file, 'w') as f:
                json.dump({'token': token}, f)
        except:
            pass
    
    def clear_token(self):
        """Clear token"""
        self.token = None
        try:
            if os.path.exists(self.token_file):
                os.remove(self.token_file)
        except:
            pass
    
    def get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication"""
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Token {self.token}'
        return headers
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Login user and get authentication token
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Response data with token and user info
        """
        response = requests.post(
            f"{self.base_url}/auth/login/",
            json={'username': username, 'password': password},
            timeout=self.timeout
        )
        response.raise_for_status()
        data = response.json()
        if 'token' in data:
            self.save_token(data['token'])
        return data
    
    def register(self, user_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Register a new user
        
        Args:
            user_data: Dictionary with username, email, password, etc.
            
        Returns:
            Response data with token and user info
        """
        response = requests.post(
            f"{self.base_url}/auth/register/",
            json=user_data,
            timeout=self.timeout
        )
        response.raise_for_status()
        data = response.json()
        if 'token' in data:
            self.save_token(data['token'])
        return data
    
    def logout(self) -> bool:
        """
        Logout user and clear token
        
        Returns:
            True if successful
        """
        try:
            response = requests.post(
                f"{self.base_url}/auth/logout/",
                headers=self.get_headers(),
                timeout=self.timeout
            )
            response.raise_for_status()
        except:
            pass
        finally:
            self.clear_token()
        return True
    
    def get_profile(self) -> Dict[str, Any]:
        """
        Get current user profile
        
        Returns:
            User profile data
        """
        response = requests.get(
            f"{self.base_url}/auth/profile/",
            headers=self.get_headers(),
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
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
            headers = {}
            if self.token:
                headers['Authorization'] = f'Token {self.token}'
            response = requests.post(
                f"{self.base_url}/upload/",
                files=files,
                headers=headers,
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
            headers=self.get_headers(),
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
            headers=self.get_headers(),
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
            headers=self.get_headers(),
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
            f"{self.base_url}/datasets/{dataset_id}/chart_data/",
            headers=self.get_headers(),
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
        
        response = requests.get(url, headers=self.get_headers(), timeout=self.timeout)
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
            headers=self.get_headers(),
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
            # Try to access a public endpoint or check if authenticated
            if self.token:
                response = requests.get(
                    f"{self.base_url}/auth/profile/",
                    headers=self.get_headers(),
                    timeout=5
                )
                return response.status_code == 200
            else:
                # Just check if server is reachable
                response = requests.get(
                    f"{self.base_url.replace('/api', '')}/admin/",
                    timeout=5
                )
                return True
        except:
            return False
    
    def is_authenticated(self) -> bool:
        """
        Check if user is authenticated
        
        Returns:
            True if token exists
        """
        return self.token is not None
