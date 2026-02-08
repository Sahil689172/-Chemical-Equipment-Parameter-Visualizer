"""
Upload Widget for CSV file upload to backend API
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QLineEdit, QProgressBar, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from pathlib import Path
from services.api_client import APIClient


class UploadThread(QThread):
    """Thread for uploading CSV file to avoid blocking UI"""
    upload_progress = pyqtSignal(int)
    upload_complete = pyqtSignal(dict)
    upload_error = pyqtSignal(str)
    
    def __init__(self, api_client, file_path):
        super().__init__()
        self.api_client = api_client
        self.file_path = file_path
    
    def run(self):
        try:
            self.upload_progress.emit(50)
            result = self.api_client.upload_csv(self.file_path)
            self.upload_progress.emit(100)
            self.upload_complete.emit(result)
        except Exception as e:
            self.upload_error.emit(str(e))


class UploadWidget(QWidget):
    """Widget for uploading CSV files"""
    
    upload_success = pyqtSignal(dict)  # Signal emitted on successful upload
    
    def __init__(self, api_client: APIClient, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.selected_file = None
        self.upload_thread = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Upload Equipment Data")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2d3748;")
        layout.addWidget(title)
        
        # File selection section
        file_layout = QHBoxLayout()
        
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("No file selected...")
        self.file_path_edit.setReadOnly(True)
        self.file_path_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #cbd5e0;
                border-radius: 6px;
                background: white;
            }
        """)
        file_layout.addWidget(self.file_path_edit)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #5568d3;
            }
        """)
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        
        layout.addLayout(file_layout)
        
        # Upload button
        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.setStyleSheet("""
            QPushButton {
                padding: 12px;
                background: #48bb78;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #38a169;
            }
            QPushButton:disabled {
                background: #a0aec0;
            }
        """)
        self.upload_btn.setEnabled(False)
        self.upload_btn.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #cbd5e0;
                border-radius: 6px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background: #667eea;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #718096; padding: 5px;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def browse_file(self):
        """Open file dialog to select CSV file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            str(Path.home()),
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            self.selected_file = file_path
            self.file_path_edit.setText(file_path)
            self.upload_btn.setEnabled(True)
            self.status_label.setText("")
            self.status_label.setStyleSheet("color: #718096; padding: 5px;")
    
    def upload_file(self):
        """Upload the selected CSV file to the backend"""
        if not self.selected_file:
            QMessageBox.warning(self, "No File", "Please select a CSV file first.")
            return
        
        # Test connection first
        if not self.api_client.test_connection():
            QMessageBox.critical(
                self,
                "Connection Error",
                "Cannot connect to the backend API.\n"
                "Please make sure the Django server is running on http://localhost:8000"
            )
            return
        
        # Disable upload button and show progress
        self.upload_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Uploading...")
        self.status_label.setStyleSheet("color: #667eea; padding: 5px; font-weight: bold;")
        
        # Create and start upload thread
        self.upload_thread = UploadThread(self.api_client, self.selected_file)
        self.upload_thread.upload_progress.connect(self.update_progress)
        self.upload_thread.upload_complete.connect(self.on_upload_success)
        self.upload_thread.upload_error.connect(self.on_upload_error)
        self.upload_thread.start()
    
    def update_progress(self, value: int):
        """Update progress bar"""
        self.progress_bar.setValue(value)
    
    def on_upload_success(self, result: dict):
        """Handle successful upload"""
        self.progress_bar.setValue(100)
        self.progress_bar.setVisible(False)
        self.upload_btn.setEnabled(True)
        
        message = f"Successfully uploaded {result.get('message', 'file')}"
        self.status_label.setText(message)
        self.status_label.setStyleSheet("color: #48bb78; padding: 5px; font-weight: bold;")
        
        # Show success message
        QMessageBox.information(
            self,
            "Upload Successful",
            f"File uploaded successfully!\n\n"
            f"Dataset ID: {result.get('dataset_id')}\n"
            f"Items processed: {result.get('summary', {}).get('total_equipment_count', 0)}"
        )
        
        # Emit signal for parent to handle
        self.upload_success.emit(result)
        
        # Reset file selection
        self.selected_file = None
        self.file_path_edit.clear()
        self.upload_btn.setEnabled(False)
    
    def on_upload_error(self, error_msg: str):
        """Handle upload error"""
        self.progress_bar.setVisible(False)
        self.upload_btn.setEnabled(True)
        
        self.status_label.setText("Upload failed")
        self.status_label.setStyleSheet("color: #c53030; padding: 5px; font-weight: bold;")
        
        QMessageBox.critical(
            self,
            "Upload Error",
            f"Failed to upload file:\n\n{error_msg}"
        )
