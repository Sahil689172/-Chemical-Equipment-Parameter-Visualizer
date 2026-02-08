import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

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
