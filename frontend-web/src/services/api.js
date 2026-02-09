import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle 401 errors (unauthorized)
let isReloading = false;
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Only clear auth if we have a token (avoid infinite loops)
      const token = localStorage.getItem('authToken');
      if (token && !isReloading) {
        isReloading = true;
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        // Only reload if we're not already on a login/register page
        const path = window.location.pathname;
        if (path === '/' || (!path.includes('login') && !path.includes('register'))) {
          setTimeout(() => {
            window.location.reload();
          }, 100);
        } else {
          isReloading = false;
        }
      }
    }
    return Promise.reject(error);
  }
);

// Authentication functions
export const login = async (username, password) => {
  const response = await api.post('/auth/login/', { username, password });
  return response.data;
};

export const register = async (userData) => {
  const response = await api.post('/auth/register/', userData);
  return response.data;
};

export const logout = async () => {
  const response = await api.post('/auth/logout/');
  localStorage.removeItem('authToken');
  localStorage.removeItem('user');
  return response.data;
};

export const getProfile = async () => {
  const response = await api.get('/auth/profile/');
  return response.data;
};

// CSV Upload
export const uploadCSV = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

// Get all datasets (last 5)
export const getDatasets = async () => {
  const response = await api.get('/datasets/');
  return response.data;
};

// Get specific dataset details
export const getDataset = async (datasetId) => {
  const response = await api.get(`/datasets/${datasetId}/`);
  return response.data;
};

// Get dataset summary
export const getDatasetSummary = async (datasetId) => {
  const response = await api.get(`/datasets/${datasetId}/summary/`);
  return response.data;
};

// Get chart data for dataset
export const getChartData = async (datasetId) => {
  const response = await api.get(`/datasets/${datasetId}/chart_data/`);
  return response.data;
};

// Get equipment items (optionally filtered by dataset)
export const getEquipmentItems = async (datasetId = null) => {
  const url = datasetId 
    ? `/equipment/?dataset=${datasetId}`
    : '/equipment/';
  const response = await api.get(url);
  return response.data;
};

// Delete a dataset
export const deleteDataset = async (datasetId) => {
  const response = await api.delete(`/datasets/${datasetId}/`);
  return response.data;
};

export default api;
