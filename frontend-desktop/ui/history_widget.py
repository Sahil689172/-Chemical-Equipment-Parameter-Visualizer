"""
History Widget for displaying dataset history
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
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
        layout.setSpacing(10)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Dataset History")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2d3748;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
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
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background: white;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #e2e8f0;
            }
            QListWidget::item:selected {
                background: #e6fffa;
                color: #2d3748;
            }
            QListWidget::item:hover {
                background: #f7fafc;
            }
        """)
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        layout.addWidget(self.list_widget)
        
        # Info label
        self.info_label = QLabel("No datasets available")
        self.info_label.setStyleSheet("""
            color: #718096;
            padding: 10px;
            background: #f7fafc;
            border-radius: 6px;
        """)
        layout.addWidget(self.info_label)
        
        self.setLayout(layout)
    
    def load_datasets(self):
        """Load datasets from API"""
        try:
            self.datasets = self.api_client.get_datasets()
            self.update_list()
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Failed to load datasets:\n{str(e)}"
            )
    
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
            
            # Create list item
            item_text = f"{dataset.get('filename', 'Unknown')}\n"
            item_text += f"{item_count} items • {time_ago}"
            
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, dataset.get('id'))
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
            QMessageBox.warning(self, "No Selection", "Please select a dataset to delete.")
            return
        
        dataset_id = current_item.data(Qt.UserRole)
        if not dataset_id:
            return
        
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete this dataset?\n\n"
            f"This action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.api_client.delete_dataset(dataset_id)
                self.dataset_deleted.emit(dataset_id)
                self.load_datasets()  # Refresh list
                QMessageBox.information(self, "Success", "Dataset deleted successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete dataset:\n{str(e)}")
