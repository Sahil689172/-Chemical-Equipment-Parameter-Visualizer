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
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Set dark background
        self.setStyleSheet("background-color: #0f0f0f;")
        
        # Title
        title = QLabel("📤 Upload Equipment Data")
        title.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #ffffff;
            padding: 10px;
        """)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Select a CSV file to upload and analyze equipment parameters")
        subtitle.setStyleSheet("""
            font-size: 12px; 
            color: #cccccc;
            padding-bottom: 20px;
        """)
        layout.addWidget(subtitle)
        
        # File selection section
        file_layout = QHBoxLayout()
        
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("No file selected... Click Browse to select a CSV file")
        self.file_path_edit.setReadOnly(True)
        self.file_path_edit.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #777777;
                border-radius: 8px;
                background: #353535;
                color: #ffffff;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background: #404040;
            }
        """)
        file_layout.addWidget(self.file_path_edit)
        
        browse_btn = QPushButton("📁 Browse...")
        browse_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 25px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background: #5568d3;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background: #4458c2;
            }
        """)
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        
        layout.addLayout(file_layout)
        
        # Upload button
        self.upload_btn = QPushButton("⬆ Upload CSV")
        self.upload_btn.setStyleSheet("""
            QPushButton {
                padding: 15px;
                background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: linear-gradient(135deg, #38a169 0%, #2f855a 100%);
            }
            QPushButton:disabled {
                background: #444444;
                color: #888888;
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
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Uploading... %p%")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #444444;
                border-radius: 8px;
                text-align: center;
                height: 30px;
                background: #1a1a1a;
                color: #ffffff;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("""
            color: #cccccc; 
            padding: 10px;
            font-size: 13px;
        """)
        layout.addWidget(self.status_label)
        
        # Info box
        info_box = QLabel("📋 CSV Format: Equipment Name, Type, Flowrate, Pressure, Temperature")
        info_box.setStyleSheet("""
            background: #2a2a2a;
            border-left: 4px solid #667eea;
            padding: 12px;
            border-radius: 6px;
            color: #ffffff;
            font-size: 12px;
        """)
        layout.addWidget(info_box)
        
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
            self.status_label.setStyleSheet("""
                color: #b0b0b0; 
                padding: 10px;
                font-size: 13px;
            """)
    
    def upload_file(self):
        """Upload the selected CSV file to the backend"""
        if not self.selected_file:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("No File")
            msg_box.setText("Please select a CSV file first.")
            msg_box.setStyleSheet("""
                QMessageBox {
                    background: #1a1a1a;
                    color: #ffffff;
                }
                QMessageBox QLabel {
                    color: #ffffff;
                    background: #1a1a1a;
                }
                QMessageBox QPushButton {
                    background: #667eea;
                    color: #ffffff;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 20px;
                    font-weight: bold;
                }
                QMessageBox QPushButton:hover {
                    background: #5568d3;
                }
            """)
            msg_box.exec_()
            return
        
        # Test connection first
        if not self.api_client.test_connection():
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("Connection Error")
            msg_box.setText("Cannot connect to the backend API.")
            msg_box.setInformativeText("Please make sure the Django server is running on http://localhost:8000")
            msg_box.setStyleSheet("""
                QMessageBox {
                    background: #1a1a1a;
                    color: #ffffff;
                }
                QMessageBox QLabel {
                    color: #ffffff;
                    background: #1a1a1a;
                }
                QMessageBox QPushButton {
                    background: #667eea;
                    color: #ffffff;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 20px;
                    font-weight: bold;
                }
                QMessageBox QPushButton:hover {
                    background: #5568d3;
                }
            """)
            msg_box.exec_()
            return
        
        # Disable upload button and show progress
        self.upload_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("⏳ Uploading...")
        self.status_label.setStyleSheet("""
            color: #667eea; 
            padding: 10px;
            font-weight: bold;
            font-size: 14px;
        """)
        
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
        
        message = f"✅ Successfully uploaded {result.get('message', 'file')}"
        self.status_label.setText(message)
        self.status_label.setStyleSheet("""
            color: #48bb78; 
            padding: 10px;
            font-weight: bold;
            font-size: 14px;
        """)
        
        # Show success message with dark theme styling
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Upload Successful")
        msg_box.setText("File uploaded successfully!")
        msg_box.setInformativeText(
            f"Dataset ID: {result.get('dataset_id')}\n"
            f"Items processed: {result.get('summary', {}).get('total_equipment_count', 0)}"
        )
        msg_box.setStyleSheet("""
            QMessageBox {
                background: #1a1a1a;
                color: #ffffff;
            }
            QMessageBox QLabel {
                color: #ffffff;
                background: #1a1a1a;
                font-size: 13px;
            }
            QMessageBox QPushButton {
                background: #667eea;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background: #5568d3;
            }
        """)
        msg_box.exec_()
        
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
        
        self.status_label.setText("❌ Upload failed")
        self.status_label.setStyleSheet("""
            color: #ff4444; 
            padding: 10px;
            font-weight: bold;
            font-size: 14px;
        """)
        
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Upload Error")
        msg_box.setText("Failed to upload file:")
        msg_box.setInformativeText(error_msg)
        msg_box.setStyleSheet("""
            QMessageBox {
                background: #1a1a1a;
                color: #ffffff;
            }
            QMessageBox QLabel {
                color: #ffffff;
                background: #1a1a1a;
                font-size: 13px;
            }
            QMessageBox QPushButton {
                background: #ff4444;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background: #cc0000;
            }
        """)
        msg_box.exec_()
