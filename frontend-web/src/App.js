import React, { useState, useEffect, useCallback } from 'react';
import Header from './components/Header';
import Login from './components/Login';
import Register from './components/Register';
import UploadForm from './components/UploadForm';
import DatasetHistory from './components/DatasetHistory';
import Summary from './components/Summary';
import ChartDisplay from './components/ChartDisplay';
import DataTable from './components/DataTable';
import { logout } from './services/api';
import {
  getDatasets,
  getDatasetSummary,
  getChartData,
  getEquipmentItems,
  deleteDataset,
} from './services/api';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [user, setUser] = useState(null);
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [summary, setSummary] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [equipmentItems, setEquipmentItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Check authentication on mount
  useEffect(() => {
    const token = localStorage.getItem('authToken');
    const userData = localStorage.getItem('user');
    if (token && userData) {
      setIsAuthenticated(true);
      setUser(JSON.parse(userData));
    }
  }, []);

  const loadDatasets = useCallback(async () => {
    try {
      setLoading(true);
      const data = await getDatasets();
      setDatasets(data);
      setError(null);
      
      // Auto-select first dataset if available
      if (data.length > 0 && !selectedDataset) {
        setSelectedDataset(data[0].id);
      }
    } catch (err) {
      setError('Failed to load datasets. Make sure the backend is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [selectedDataset]);

  // Load datasets on mount and when upload succeeds (only if authenticated)
  useEffect(() => {
    if (isAuthenticated) {
      loadDatasets();
    } else {
      setLoading(false);
    }
  }, [loadDatasets, isAuthenticated]);

  // Load selected dataset details (only if authenticated)
  useEffect(() => {
    if (isAuthenticated && selectedDataset) {
      loadDatasetDetails(selectedDataset);
    } else if (isAuthenticated && datasets.length > 0 && !selectedDataset) {
      // If no dataset selected, try to select the first one
      setSelectedDataset(datasets[0].id);
    }
  }, [selectedDataset, datasets, isAuthenticated]);

  const loadDatasetDetails = async (datasetId) => {
    try {
      setLoading(true);
      
      // Load all data in parallel
      const [summaryData, chart, items] = await Promise.all([
        getDatasetSummary(datasetId),
        getChartData(datasetId),
        getEquipmentItems(datasetId),
      ]);

      setSummary(summaryData);
      setChartData(chart);
      
      // Handle paginated response
      if (Array.isArray(items)) {
        setEquipmentItems(items);
      } else if (items.results) {
        setEquipmentItems(items.results);
      } else {
        setEquipmentItems([]);
      }
      
      setError(null);
    } catch (err) {
      setError('Failed to load dataset details.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadSuccess = (result) => {
    // Reload datasets after successful upload
    loadDatasets();
    
    // Auto-select the newly uploaded dataset
    if (result.dataset_id) {
      setSelectedDataset(result.dataset_id);
    }
  };

  const handleDatasetSelect = (datasetId) => {
    setSelectedDataset(datasetId);
  };

  const handleDatasetDelete = async (datasetId) => {
    try {
      await deleteDataset(datasetId);
      
      // If deleted dataset was selected, clear selection
      if (selectedDataset === datasetId) {
        setSelectedDataset(null);
        setSummary(null);
        setChartData(null);
        setEquipmentItems([]);
      }
      
      // Reload datasets list
      loadDatasets();
    } catch (err) {
      setError('Failed to delete dataset. Please try again.');
      console.error(err);
    }
  };

  const handleLoginSuccess = (userData) => {
    setIsAuthenticated(true);
    setUser(userData);
    setShowRegister(false);
  };

  const handleRegisterSuccess = (userData) => {
    setIsAuthenticated(true);
    setUser(userData);
    setShowRegister(false);
  };

  const handleLogout = async () => {
    try {
      await logout();
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      setIsAuthenticated(false);
      setUser(null);
      setDatasets([]);
      setSelectedDataset(null);
      setSummary(null);
      setChartData(null);
      setEquipmentItems([]);
    }
  };

  // Show login/register if not authenticated
  if (!isAuthenticated) {
    return (
      <div className="App">
        {showRegister ? (
          <Register
            onRegisterSuccess={handleRegisterSuccess}
            onSwitchToLogin={() => setShowRegister(false)}
          />
        ) : (
          <Login
            onLoginSuccess={handleLoginSuccess}
            onSwitchToRegister={() => setShowRegister(true)}
          />
        )}
      </div>
    );
  }

  return (
    <div className="App">
      <Header user={user} onLogout={handleLogout} />
      <main className="App-main">
        {error && <div className="error-banner">{error}</div>}
        
        <div className="main-layout">
          {/* Left Sidebar - Dataset History */}
          <aside className="sidebar">
            <DatasetHistory
              datasets={datasets}
              loading={loading}
              onDatasetSelect={handleDatasetSelect}
              selectedDataset={selectedDataset}
              onDatasetDelete={handleDatasetDelete}
            />
          </aside>
          
          {/* Main Content Area */}
          <div className="main-content">
            <UploadForm onUploadSuccess={handleUploadSuccess} />
            
            {selectedDataset && (
              <>
                <Summary summary={summary} loading={loading} />
                <ChartDisplay 
                  chartData={chartData} 
                  equipmentItems={equipmentItems}
                  loading={loading} 
                />
                <DataTable data={equipmentItems} loading={loading} />
              </>
            )}
            
            {!selectedDataset && !loading && (
              <div className="no-data-message">
                Select a dataset from the history to view details
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
