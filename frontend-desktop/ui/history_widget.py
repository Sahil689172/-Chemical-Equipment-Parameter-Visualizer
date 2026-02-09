"""
History Widget for displaying dataset history
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from datetime import datetime


class HistoryWidget(QWidget):
    """Widget for displaying dataset history"""
    
    dataset_selected = pyqtSignal(int)  # Signal emitted when dataset is selected
    dataset_deleted = pyqtSignal(int)  # Signal emitted when dataset is deleted
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.datasets = []
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Set dark background
        self.setStyleSheet("background-color: #0f0f0f;")
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("📚 Dataset History")
        title.setStyleSheet("""
            font-size: 22px; 
            font-weight: bold; 
            color: #ffffff;
            padding: 10px;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Delete button
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                padding: 6px 15px;
                background: #ff4444;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #cc0000;
            }
        """)
        delete_btn.clicked.connect(self.delete_selected_dataset)
        header_layout.addWidget(delete_btn)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                padding: 6px 15px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #5568d3;
            }
        """)
        refresh_btn.clicked.connect(self.load_datasets)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # List widget
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                border: 2px solid #666666;
                border-radius: 8px;
                background: #2a2a2a;
                color: #ffffff;
            }
            QListWidget::item {
                padding: 15px;
                border-bottom: 1px solid #4a4a4a;
                background: #353535;
                border-radius: 6px;
                margin: 3px;
                color: #ffffff;
            }
            QListWidget::item:selected {
                background: rgba(102, 126, 234, 0.7);
                color: #ffffff;
                border: 2px solid #667eea;
            }
            QListWidget::item:hover {
                background: rgba(102, 126, 234, 0.4);
                color: #ffffff;
            }
        """)
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        layout.addWidget(self.list_widget)
        
        # Info label
        self.info_label = QLabel("No datasets available")
        self.info_label.setStyleSheet("""
            color: #ffffff;
            padding: 15px;
            background: #353535;
            border: 2px solid #666666;
            border-radius: 8px;
            font-size: 13px;
        """)
        layout.addWidget(self.info_label)
        
        self.setLayout(layout)
    
    def load_datasets(self):
        """Load datasets from API"""
        try:
            self.datasets = self.api_client.get_datasets()
            self.update_list()
        except Exception as e:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Error")
            msg_box.setText("Failed to load datasets:")
            msg_box.setInformativeText(str(e))
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
    
    def update_list(self):
        """Update the list widget with current datasets"""
        self.list_widget.clear()
        
        if not self.datasets:
            self.info_label.setText("No datasets available. Upload a CSV file to get started.")
            return
        
        self.info_label.setText(f"Showing {len(self.datasets)} dataset(s)")
        
        for dataset in self.datasets:
            # Format upload date
            upload_date = dataset.get('uploaded_at', '')
            if upload_date:
                try:
                    dt = datetime.fromisoformat(upload_date.replace('Z', '+00:00'))
                    time_ago = self.format_time_ago(dt)
                except:
                    time_ago = upload_date
            else:
                time_ago = "Unknown"
            
            # Get item count from summary
            summary = dataset.get('summary', {})
            item_count = summary.get('total_equipment_count', 0)
            
            # Create list item with better formatting
            filename = dataset.get('filename', 'Unknown')
            item_text = f"📄 {filename}\n"
            item_text += f"   📊 {item_count} items  •  🕒 {time_ago}"
            
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, dataset.get('id'))
            item.setFont(QFont("Segoe UI", 11))
            self.list_widget.addItem(item)
    
    def format_time_ago(self, dt: datetime) -> str:
        """Format datetime as time ago string"""
        now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
        diff = now - dt
        
        if diff.days > 0:
            if diff.days == 1:
                return "1 day ago"
            elif diff.days < 7:
                return f"{diff.days} days ago"
            elif diff.days < 30:
                weeks = diff.days // 7
                return f"{weeks} week{'s' if weeks > 1 else ''} ago"
            else:
                months = diff.days // 30
                return f"{months} month{'s' if months > 1 else ''} ago"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    
    def on_item_double_clicked(self, item: QListWidgetItem):
        """Handle double-click on list item"""
        dataset_id = item.data(Qt.UserRole)
        if dataset_id:
            self.dataset_selected.emit(dataset_id)
    
    def delete_selected_dataset(self):
        """Delete the selected dataset"""
        current_item = self.list_widget.currentItem()
        if not current_item:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("No Selection")
            msg_box.setText("Please select a dataset to delete.")
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
        
        dataset_id = current_item.data(Qt.UserRole)
        if not dataset_id:
            return
        
        # Confirm deletion with styled dialog
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Confirm Delete")
        msg_box.setText("Are you sure you want to delete this dataset?")
        msg_box.setInformativeText("This action cannot be undone.")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
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
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background: #5568d3;
            }
            QMessageBox QPushButton[text="&Yes"] {
                background: #ff4444;
            }
            QMessageBox QPushButton[text="&Yes"]:hover {
                background: #cc0000;
            }
        """)
        reply = msg_box.exec_()
        
        if reply == QMessageBox.Yes:
            try:
                self.api_client.delete_dataset(dataset_id)
                self.dataset_deleted.emit(dataset_id)
                self.load_datasets()  # Refresh list
                
                # Success message
                success_box = QMessageBox(self)
                success_box.setIcon(QMessageBox.Information)
                success_box.setWindowTitle("Success")
                success_box.setText("Dataset deleted successfully.")
                success_box.setStyleSheet("""
                    QMessageBox {
                        background: #1a1a1a;
                        color: #ffffff;
                    }
                    QMessageBox QLabel {
                        color: #ffffff;
                        background: #1a1a1a;
                    }
                    QMessageBox QPushButton {
                        background: #48bb78;
                        color: #ffffff;
                        border: none;
                        border-radius: 6px;
                        padding: 8px 20px;
                        font-weight: bold;
                    }
                    QMessageBox QPushButton:hover {
                        background: #38a169;
                    }
                """)
                success_box.exec_()
            except Exception as e:
                error_box = QMessageBox(self)
                error_box.setIcon(QMessageBox.Critical)
                error_box.setWindowTitle("Error")
                error_box.setText("Failed to delete dataset:")
                error_box.setInformativeText(str(e))
                error_box.setStyleSheet("""
                    QMessageBox {
                        background: #1a1a1a;
                        color: #ffffff;
                    }
                    QMessageBox QLabel {
                        color: #ffffff;
                        background: #1a1a1a;
                    }
                    QMessageBox QPushButton {
                        background: #ff4444;
                        color: #ffffff;
                        border: none;
                        border-radius: 6px;
                        padding: 8px 20px;
                        font-weight: bold;
                    }
                    QMessageBox QPushButton:hover {
                        background: #cc0000;
                    }
                """)
                error_box.exec_()
