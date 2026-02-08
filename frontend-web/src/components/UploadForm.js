import React, { useState, useRef } from 'react';
import { uploadCSV } from '../services/api';
import './UploadForm.css';

function UploadForm({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const validateFile = (selectedFile) => {
    if (!selectedFile) return false;
    
    if (!selectedFile.name.endsWith('.csv')) {
      setError('Please select a CSV file');
      setFile(null);
      return false;
    }
    
    setFile(selectedFile);
    setError(null);
    setSuccess(null);
    return true;
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    validateFile(selectedFile);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      validateFile(droppedFile);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please select a file to upload');
      return;
    }

    setUploading(true);
    setError(null);
    setSuccess(null);

    try {
      const result = await uploadCSV(file);
      setSuccess(`Successfully uploaded ${result.message}`);
      
      // Notify parent component
      if (onUploadSuccess) {
        onUploadSuccess(result);
      }
    } catch (err) {
      let errorMessage = err.response?.data?.error || err.message || 'Failed to upload file. Please try again.';
      
      // Enhance error message with column information
      if (err.response?.data?.required_columns) {
        errorMessage += `\n\nRequired columns: ${err.response.data.required_columns.join(', ')}`;
      }
      if (err.response?.data?.found_columns) {
        errorMessage += `\n\nFound columns: ${err.response.data.found_columns.join(', ')}`;
      }
      
      setError(errorMessage);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-form-container">
      <form onSubmit={handleSubmit} className="upload-form">
        <div
          className={`drop-zone ${isDragging ? 'dragging' : ''} ${file ? 'has-file' : ''} ${success ? 'uploaded' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => !success && fileInputRef.current?.click()}
        >
          <input
            ref={fileInputRef}
            type="file"
            id="csv-file"
            accept=".csv"
            onChange={handleFileChange}
            disabled={uploading || success}
            className="file-input"
          />
          <div className="drop-zone-content">
            {uploading ? (
              <>
                <div className="upload-icon">⏳</div>
                <p className="drop-zone-text">Uploading...</p>
              </>
            ) : success ? (
              <>
                <div className="file-icon success-icon">✓</div>
                <p className="drop-zone-text success-text">File Uploaded Successfully</p>
                <p className="drop-zone-filename">{file?.name}</p>
                <p className="drop-zone-hint">is ready for analysis. Drag and drop to replace or click the button.</p>
                <div className="upload-actions">
                  <button 
                    type="button"
                    className="action-button primary"
                    onClick={(e) => {
                      e.stopPropagation();
                      // Trigger analysis - this will be handled by parent
                    }}
                  >
                    <span>📊</span>
                    Run New Analysis
                  </button>
                  <button 
                    type="button"
                    className="action-button secondary"
                    onClick={(e) => {
                      e.stopPropagation();
                      setFile(null);
                      setSuccess(null);
                      if (fileInputRef.current) fileInputRef.current.value = '';
                    }}
                  >
                    Clear File
                  </button>
                </div>
                <div className="csv-ready-badge">CSV READY</div>
              </>
            ) : file ? (
              <>
                <div className="file-icon">✓</div>
                <p className="drop-zone-text file-name">{file.name}</p>
                <p className="drop-zone-hint">Click to change file</p>
              </>
            ) : (
              <>
                <div className="upload-icon">📄</div>
                <p className="drop-zone-text">
                  Drag and drop your CSV file here
                </p>
                <p className="drop-zone-hint">or click to browse</p>
              </>
            )}
          </div>
        </div>
        
        {file && !uploading && !success && (
          <button 
            type="submit" 
            className="upload-button"
          >
            <span className="button-icon">⬆</span>
            Upload CSV
          </button>
        )}

        {error && (
          <div className="error-message">
            <span className="error-icon">⚠</span>
            {error}
          </div>
        )}
      </form>
    </div>
  );
}

export default UploadForm;
