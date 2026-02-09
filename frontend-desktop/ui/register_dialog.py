"""
Register Dialog for user registration
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFormLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class RegisterDialog(QDialog):
    """Dialog for user registration"""
    
    register_success = pyqtSignal(dict)  # Emits user data on successful registration
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register")
        self.setModal(True)
        self.setFixedSize(450, 500)
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
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("📝 Register")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #ffffff; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Create a new account to get started.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #b0b0b0; font-size: 12px; margin-bottom: 20px;")
        layout.addWidget(subtitle)
        
        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        self.first_name_edit = QLineEdit()
        self.first_name_edit.setPlaceholderText("First name (optional)")
        form_layout.addRow("First Name:", self.first_name_edit)
        
        self.last_name_edit = QLineEdit()
        self.last_name_edit.setPlaceholderText("Last name (optional)")
        form_layout.addRow("Last Name:", self.last_name_edit)
        
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Choose a username")
        form_layout.addRow("Username *:", self.username_edit)
        
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Enter your email")
        form_layout.addRow("Email *:", self.email_edit)
        
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("At least 8 characters")
        self.password_edit.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Password *:", self.password_edit)
        
        self.password_confirm_edit = QLineEdit()
        self.password_confirm_edit.setPlaceholderText("Confirm your password")
        self.password_confirm_edit.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Confirm Password *:", self.password_confirm_edit)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.register_btn = QPushButton("Register")
        self.register_btn.clicked.connect(self.handle_register)
        button_layout.addWidget(self.register_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background: #666666;
            }
            QPushButton:hover {
                background: #555555;
            }
        """)
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def handle_register(self):
        """Handle registration attempt"""
        username = self.username_edit.text().strip()
        email = self.email_edit.text().strip()
        password = self.password_edit.text()
        password_confirm = self.password_confirm_edit.text()
        first_name = self.first_name_edit.text().strip()
        last_name = self.last_name_edit.text().strip()
        
        # Validation
        if not username:
            self.show_error("Username is required.")
            return
        
        if not email:
            self.show_error("Email is required.")
            return
        
        if not password:
            self.show_error("Password is required.")
            return
        
        if len(password) < 8:
            self.show_error("Password must be at least 8 characters long.")
            return
        
        if password != password_confirm:
            self.show_error("Passwords do not match.")
            return
        
        # Emit signal for parent to handle API call
        self.accept()
        self.register_success.emit({
            'username': username,
            'email': email,
            'password': password,
            'password_confirm': password_confirm,
            'first_name': first_name,
            'last_name': last_name
        })
    
    def show_error(self, message):
        """Show error message"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Registration Error")
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
    
    def get_registration_data(self):
        """Get entered registration data"""
        return {
            'username': self.username_edit.text().strip(),
            'email': self.email_edit.text().strip(),
            'password': self.password_edit.text(),
            'password_confirm': self.password_confirm_edit.text(),
            'first_name': self.first_name_edit.text().strip(),
            'last_name': self.last_name_edit.text().strip()
        }
