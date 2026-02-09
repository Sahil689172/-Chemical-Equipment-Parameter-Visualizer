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
from ui.login_dialog import LoginDialog
from ui.register_dialog import RegisterDialog


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.current_dataset_id = None
        self.user = None
        
        # Check authentication
        if not self.api_client.is_authenticated():
            # Don't show main window until authenticated
            self.hide()
            self.show_login()
        else:
            self.init_ui()
            self.show()
    
    def init_ui(self):
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(100, 100, 1600, 1000)
        
        # Set application style with dark theme
        self.setStyleSheet("""
            QMainWindow {
                background: #000000;
            }
            QMenuBar {
                background: #1a1a1a;
                color: #ffffff;
                border-bottom: 1px solid #333333;
            }
            QMenuBar::item {
                padding: 8px 15px;
                background: transparent;
            }
            QMenuBar::item:selected {
                background: #333333;
            }
            QMenu {
                background: #1a1a1a;
                color: #ffffff;
                border: 1px solid #333333;
            }
            QMenu::item:selected {
                background: #667eea;
            }
            QToolBar {
                background: #1a1a1a;
                border: none;
                spacing: 5px;
            }
            QToolBar QToolButton {
                background: #0f0f0f;
                color: #ffffff;
                border: 1px solid #333333;
                border-radius: 6px;
                padding: 8px 15px;
            }
            QToolBar QToolButton:hover {
                background: #667eea;
                border-color: #667eea;
            }
            QStatusBar {
                background: #1a1a1a;
                color: #ffffff;
                border-top: 1px solid #333333;
            }
            QTabWidget::pane {
                border: 2px solid #666666;
                border-radius: 8px;
                background: #1a1a1a;
            }
            QTabBar::tab {
                background: #2a2a2a;
                color: #cccccc;
                padding: 12px 25px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border: 2px solid #555555;
            }
            QTabBar::tab:selected {
                background: #1a1a1a;
                color: #ffffff;
                font-weight: bold;
                border-bottom: 3px solid #667eea;
                border-color: #888888;
            }
            QTabBar::tab:hover {
                background: #404040;
                color: #ffffff;
            }
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
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create status bar with connection indicator
        self.statusBar().showMessage("Ready")
        self.statusBar().setStyleSheet("""
            QStatusBar {
                color: #ffffff;
            }
        """)
        
        # Create central widget with tabs
        self.create_tabs()
        
        # Load initial data
        self.load_initial_data()
    
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        # Logout action
        logout_action = QAction('Logout', self)
        logout_action.setShortcut('Ctrl+L')
        logout_action.triggered.connect(self.handle_logout)
        file_menu.addAction(logout_action)
        file_menu.addSeparator()
        
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
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addToolBar(toolbar)
        
        upload_action = QAction('📤 Upload CSV', self)
        upload_action.setToolTip('Upload a new CSV file (Ctrl+U)')
        upload_action.triggered.connect(self.on_upload_action)
        toolbar.addAction(upload_action)
        
        toolbar.addSeparator()
        
        refresh_action = QAction('🔄 Refresh', self)
        refresh_action.setToolTip('Refresh all data (F5)')
        refresh_action.triggered.connect(self.refresh_all)
        toolbar.addAction(refresh_action)
        
        toolbar.addSeparator()
        
        charts_action = QAction('📊 View Charts', self)
        charts_action.setToolTip('Switch to Charts tab')
        charts_action.triggered.connect(lambda: self.tabs.setCurrentIndex(3))
        toolbar.addAction(charts_action)
    
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
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Connection Warning")
            msg_box.setText("Cannot connect to the backend API.")
            msg_box.setInformativeText(
                "Please make sure the Django server is running on http://localhost:8000\n\n"
                "You can still use the application, but API features will not work."
            )
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
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("Error")
            msg_box.setText("Failed to load dataset data:")
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
            msg_box.exec_()
    
    def refresh_all(self):
        """Refresh all data"""
        if self.current_dataset_id:
            self.load_dataset_data(self.current_dataset_id)
        self.history_widget.load_datasets()
        self.statusBar().showMessage("Data refreshed", 2000)
    
    def show_login(self):
        """Show login dialog"""
        login_dialog = LoginDialog(self)
        login_dialog.login_success.connect(self.handle_login)
        login_dialog.registration_complete.connect(self.handle_register)
        login_dialog.exec_()
    
    def handle_login(self, credentials):
        """Handle login from dialog signal"""
        try:
            response = self.api_client.login(credentials['username'], credentials['password'])
            self.user = response.get('user')
            if not hasattr(self, 'tabs') or self.tabs is None:
                self.init_ui()
            self.show()
        except Exception as e:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("Login Error")
            msg_box.setText("Login failed:")
            error_msg = str(e)
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                try:
                    import json
                    error_data = json.loads(e.response.text)
                    if isinstance(error_data, dict):
                        error_msg = '\n'.join([f"{k}: {', '.join(v) if isinstance(v, list) else v}" for k, v in error_data.items()])
                except:
                    pass
            msg_box.setInformativeText(error_msg)
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
            msg_box.exec_()
            self.show_login()  # Show login again
    
    def handle_register(self, user_data):
        """Handle registration from dialog"""
        try:
            response = self.api_client.register(user_data)
            self.user = response.get('user')
            if not hasattr(self, 'tabs') or self.tabs is None:
                self.init_ui()
            self.show()
            
            # Show success message
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("Registration Successful")
            msg_box.setText("Registration successful!")
            msg_box.setInformativeText(f"Welcome, {self.user.get('username', 'User')}!")
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
            msg_box.exec_()
        except Exception as e:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("Registration Error")
            msg_box.setText("Registration failed:")
            error_msg = str(e)
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                try:
                    import json
                    error_data = json.loads(e.response.text)
                    if isinstance(error_data, dict):
                        error_msg = '\n'.join([f"{k}: {', '.join(v) if isinstance(v, list) else v}" for k, v in error_data.items()])
                except:
                    pass
            msg_box.setInformativeText(error_msg)
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
            msg_box.exec_()
            self.show_login()  # Show login again on error
    
    def handle_logout(self):
        """Handle logout"""
        self.api_client.logout()
        self.user = None
        self.current_dataset_id = None
        self.close()
        self.show_login()
    
    def show_about(self):
        """Show about dialog"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("About Chemical Equipment Parameter Visualizer")
        msg_box.setText("Chemical Equipment Parameter Visualizer v1.0")
        msg_box.setInformativeText(
            "A desktop application for visualizing chemical equipment parameters.\n\n"
            "Built with PyQt5 and Matplotlib."
        )
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


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for modern look
    
    window = MainWindow()
    # Window will show login dialog if not authenticated
    # If authenticated, show main window
    if window.api_client.is_authenticated():
        window.show()
    # Otherwise login dialog will be shown in __init__
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
