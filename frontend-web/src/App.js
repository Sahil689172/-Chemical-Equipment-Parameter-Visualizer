import React, { useState, useEffect, useCallback } from 'react';
import Header from './components/Header';
import UploadForm from './components/UploadForm';
import DatasetHistory from './components/DatasetHistory';
import Summary from './components/Summary';
import ChartDisplay from './components/ChartDisplay';
import DataTable from './components/DataTable';
import {
  getDatasets,
  getDatasetSummary,
  getChartData,
  getEquipmentItems,
  deleteDataset,
} from './services/api';
import './App.css';

function App() {
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [summary, setSummary] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [equipmentItems, setEquipmentItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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

  // Load datasets on mount and when upload succeeds
  useEffect(() => {
    loadDatasets();
  }, [loadDatasets]);

  // Load selected dataset details
  useEffect(() => {
    if (selectedDataset) {
      loadDatasetDetails(selectedDataset);
    } else {
      // If no dataset selected, try to select the first one
      if (datasets.length > 0 && !selectedDataset) {
        setSelectedDataset(datasets[0].id);
      }
    }
  }, [selectedDataset, datasets]);

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

  return (
    <div className="App">
      <Header />
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
