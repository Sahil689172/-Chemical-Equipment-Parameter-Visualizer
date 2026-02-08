#!/usr/bin/env python3
"""
Chemical Equipment Parameter Visualizer - Desktop Application
PyQt5-based desktop client for visualizing chemical equipment parameters
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QAction, QMessageBox, QStatusBar, QToolBar
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence
from services.api_client import APIClient
from ui.upload_widget import UploadWidget
from ui.table_widget import TableWidget
from ui.chart_widget import ChartWidget
from ui.history_widget import HistoryWidget


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.current_dataset_id = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background: #f7fafc;
            }
            QTabWidget::pane {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background: white;
            }
            QTabBar::tab {
                background: #edf2f7;
                color: #4a5568;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background: white;
                color: #2d3748;
                font-weight: bold;
            }
        """)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create status bar
        self.statusBar().showMessage("Ready")
        
        # Create central widget with tabs
        self.create_tabs()
        
        # Load initial data
        self.load_initial_data()
    
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        upload_action = QAction('Upload CSV...', self)
        upload_action.setShortcut(QKeySequence('Ctrl+U'))
        upload_action.triggered.connect(self.on_upload_action)
        file_menu.addAction(upload_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut(QKeySequence('Ctrl+Q'))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        refresh_action = QAction('Refresh', self)
        refresh_action.setShortcut(QKeySequence('F5'))
        refresh_action.triggered.connect(self.refresh_all)
        view_menu.addAction(refresh_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Create toolbar"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        upload_action = QAction('Upload', self)
        upload_action.triggered.connect(self.on_upload_action)
        toolbar.addAction(upload_action)
        
        toolbar.addSeparator()
        
        refresh_action = QAction('Refresh', self)
        refresh_action.triggered.connect(self.refresh_all)
        toolbar.addAction(refresh_action)
    
    def create_tabs(self):
        """Create tab widget with all tabs"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Upload tab
        self.upload_widget = UploadWidget(self.api_client)
        self.upload_widget.upload_success.connect(self.on_upload_success)
        self.tabs.addTab(self.upload_widget, "Upload")
        
        # History tab
        self.history_widget = HistoryWidget(self.api_client)
        self.history_widget.dataset_selected.connect(self.on_dataset_selected)
        self.history_widget.dataset_deleted.connect(self.on_dataset_deleted)
        self.tabs.addTab(self.history_widget, "History")
        
        # Table tab
        self.table_widget = TableWidget()
        self.tabs.addTab(self.table_widget, "Data Table")
        
        # Charts tab
        self.chart_widget = ChartWidget()
        self.tabs.addTab(self.chart_widget, "Charts")
        
        layout.addWidget(self.tabs)
    
    def load_initial_data(self):
        """Load initial data on startup"""
        # Load dataset history
        self.history_widget.load_datasets()
        
        # Test API connection
        if not self.api_client.test_connection():
            QMessageBox.warning(
                self,
                "Connection Warning",
                "Cannot connect to the backend API.\n"
                "Please make sure the Django server is running on http://localhost:8000\n\n"
                "You can still use the application, but API features will not work."
            )
    
    def on_upload_action(self):
        """Switch to upload tab"""
        self.tabs.setCurrentIndex(0)
    
    def on_upload_success(self, result: dict):
        """Handle successful upload"""
        dataset_id = result.get('dataset_id')
        if dataset_id:
            self.current_dataset_id = dataset_id
            self.load_dataset_data(dataset_id)
            self.history_widget.load_datasets()  # Refresh history
            self.tabs.setCurrentIndex(1)  # Switch to history tab
            self.statusBar().showMessage(f"Upload successful! Dataset ID: {dataset_id}", 5000)
    
    def on_dataset_selected(self, dataset_id: int):
        """Handle dataset selection from history"""
        self.current_dataset_id = dataset_id
        self.load_dataset_data(dataset_id)
        self.tabs.setCurrentIndex(2)  # Switch to table tab
        self.statusBar().showMessage(f"Loaded dataset {dataset_id}", 3000)
    
    def on_dataset_deleted(self, dataset_id: int):
        """Handle dataset deletion"""
        if self.current_dataset_id == dataset_id:
            self.current_dataset_id = None
            self.table_widget.clear_data()
            self.chart_widget.clear_charts()
        self.statusBar().showMessage("Dataset deleted", 3000)
    
    def load_dataset_data(self, dataset_id: int):
        """Load data for a specific dataset"""
        try:
            # Load equipment items
            equipment_items = self.api_client.get_equipment_items(dataset_id)
            self.table_widget.load_data(equipment_items)
            
            # Load chart data
            chart_data = self.api_client.get_chart_data(dataset_id)
            self.chart_widget.load_data(chart_data, equipment_items)
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to load dataset data:\n{str(e)}"
            )
    
    def refresh_all(self):
        """Refresh all data"""
        if self.current_dataset_id:
            self.load_dataset_data(self.current_dataset_id)
        self.history_widget.load_datasets()
        self.statusBar().showMessage("Data refreshed", 2000)
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Chemical Equipment Parameter Visualizer",
            "Chemical Equipment Parameter Visualizer v1.0\n\n"
            "A desktop application for visualizing chemical equipment parameters.\n\n"
            "Built with PyQt5 and Matplotlib."
        )


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for modern look
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
