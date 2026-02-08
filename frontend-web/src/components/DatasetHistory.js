import React from 'react';
import './DatasetHistory.css';

function DatasetHistory({ datasets, loading, onDatasetSelect, selectedDataset, onDatasetDelete }) {
  const formatTimeAgo = (date) => {
    const now = new Date();
    const diff = now - date;
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor(diff / (1000 * 60));
    
    if (days === 0) {
      if (hours === 0) {
        if (minutes < 1) return 'Just now';
        return `${minutes} min ago`;
      }
      const timeStr = date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
      return `Today, ${timeStr}`;
    } else if (days === 1) {
      const timeStr = date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
      return `Yesterday, ${timeStr}`;
    } else if (days < 7) {
      return `${days} days ago`;
    } else {
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    }
  };

  if (loading) {
    return (
      <div className="dataset-history-container">
        <div className="history-header">
          <h2>DATASET HISTORY</h2>
          <span className="history-count">Last 5</span>
        </div>
        <div className="loading-message">Loading dataset history...</div>
      </div>
    );
  }

  if (!datasets || datasets.length === 0) {
    return (
      <div className="dataset-history-container">
        <div className="history-header">
          <h2>DATASET HISTORY</h2>
          <span className="history-count">Last 5</span>
        </div>
        <div className="empty-message">No datasets available. Upload a CSV file to get started.</div>
      </div>
    );
  }

  return (
    <div className="dataset-history-container">
      <div className="history-header">
        <h2>DATASET HISTORY</h2>
        <span className="history-count">Last 5</span>
      </div>
      <div className="dataset-list">
        {datasets.map((dataset) => (
          <div
            key={dataset.id}
            className={`dataset-card ${selectedDataset === dataset.id ? 'selected' : ''}`}
          >
            <div 
              className="dataset-content"
              onClick={() => onDatasetSelect && onDatasetSelect(dataset.id)}
            >
              <div className="dataset-filename">{dataset.filename}</div>
              <div className="dataset-meta">
                <span className="dataset-items">
                  {dataset.summary?.total_equipment_count || 0} items
                </span>
                <span className="dataset-date">
                  {formatTimeAgo(new Date(dataset.uploaded_at))}
                </span>
              </div>
            </div>
            <button
              className="delete-button"
              onClick={(e) => {
                e.stopPropagation();
                if (window.confirm(`Are you sure you want to delete "${dataset.filename}"?`)) {
                  onDatasetDelete && onDatasetDelete(dataset.id);
                }
              }}
              title="Delete dataset"
            >
              🗑️
            </button>
          </div>
        ))}
      </div>
      <button className="view-all-button">
        <span>🔄</span>
        View All History
      </button>
    </div>
  );
}

export default DatasetHistory;
