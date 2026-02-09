"""
Login Dialog for user authentication
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFormLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class LoginDialog(QDialog):
    """Dialog for user login"""
    
    login_success = pyqtSignal(dict)  # Emits user data on successful login
    registration_complete = pyqtSignal(dict)  # Emits user data on successful registration
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.setModal(True)
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            QDialog {
                background: #1a1a1a;
            }
            QLabel {
                color: #ffffff;
                font-size: 13px;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #555555;
                border-radius: 6px;
                background: #252525;
                color: #ffffff;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background: #2a2a2a;
            }
            QPushButton {
                padding: 10px 20px;
                background: #667eea;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background: #5568d3;
            }
            QPushButton:pressed {
                background: #4458c2;
            }
        """)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("🔐 Login")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #ffffff; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Welcome back! Please login to continue.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #b0b0b0; font-size: 12px; margin-bottom: 20px;")
        layout.addWidget(subtitle)
        
        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Enter your username")
        form_layout.addRow("Username:", self.username_edit)
        
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Enter your password")
        self.password_edit.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Password:", self.password_edit)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.handle_login)
        button_layout.addWidget(self.login_btn)
        
        self.register_btn = QPushButton("Register")
        self.register_btn.setStyleSheet("""
            QPushButton {
                background: #48bb78;
            }
            QPushButton:hover {
                background: #38a169;
            }
        """)
        self.register_btn.clicked.connect(self.show_register)
        button_layout.addWidget(self.register_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def handle_login(self):
        """Handle login attempt"""
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        if not username or not password:
            self.show_error("Please enter both username and password.")
            return
        
        # Emit signal for parent to handle API call
        self.login_success.emit({
            'username': username,
            'password': password
        })
    
    def show_register(self):
        """Show register dialog"""
        from .register_dialog import RegisterDialog
        register_dialog = RegisterDialog(self)
        register_dialog.register_success.connect(self.handle_register_success)
        register_dialog.exec_()
    
    def handle_register_success(self, user_data):
        """Handle successful registration"""
        # Emit signal to parent (MainWindow) to handle registration
        self.registration_complete.emit(user_data)
        # Close login dialog
        self.accept()
    
    def show_error(self, message):
        """Show error message"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Login Error")
        msg_box.setText(message)
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
    
    def get_credentials(self):
        """Get entered credentials"""
        return {
            'username': self.username_edit.text().strip(),
            'password': self.password_edit.text()
        }
