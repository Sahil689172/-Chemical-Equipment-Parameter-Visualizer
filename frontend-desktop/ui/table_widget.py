"""
Table Widget for displaying equipment data
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QLabel, QHBoxLayout, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor


class TableWidget(QWidget):
    """Widget for displaying equipment data in a table"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.equipment_data = []
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Set dark background - different from table background
        self.setStyleSheet("background-color: #000000;")
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("📊 Equipment Data")
        title.setStyleSheet("""
            font-size: 22px; 
            font-weight: bold; 
            color: #ffffff;
            padding: 10px;
        """)
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
        refresh_btn.clicked.connect(self.refresh_table)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Equipment Name",
            "Type",
            "Flowrate (L/min)",
            "Pressure (bar)",
            "Temperature (°C)"
        ])
        
        # Style the table with dark theme - ensuring maximum contrast
        self.table.setStyleSheet("""
            QTableWidget {
                border: 3px solid #888888;
                border-radius: 8px;
                background: #1a1a1a;
                gridline-color: #666666;
                color: #ffffff;
                selection-background-color: rgba(102, 126, 234, 0.8);
                alternate-background-color: #2d2d2d;
            }
            QTableWidget::item {
                padding: 12px;
                border-bottom: 2px solid #555555;
                background: #1a1a1a;
                color: #ffffff;
            }
            QTableWidget::item:alternate {
                background: #2d2d2d;
                color: #ffffff;
            }
            QTableWidget::item:selected {
                background: rgba(102, 126, 234, 0.9);
                color: #ffffff;
            }
            QTableWidget::item:hover {
                background: rgba(102, 126, 234, 0.5);
                color: #ffffff;
            }
            QHeaderView::section {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #ffffff;
                padding: 14px;
                border: 2px solid #aaaaaa;
                font-weight: bold;
                font-size: 13px;
            }
        """)
        
        # Configure table behavior
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        
        # Force white text color for all table items
        self.table.setStyleSheet(self.table.styleSheet() + """
            QTableWidget::item {
                color: #ffffff !important;
            }
        """)
        
        layout.addWidget(self.table)
        
        # Statistics label
        self.stats_label = QLabel("No data loaded")
        self.stats_label.setStyleSheet("""
            color: #ffffff;
            padding: 15px;
            background: #2d2d2d;
            border: 3px solid #888888;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
        """)
        layout.addWidget(self.stats_label)
        
        self.setLayout(layout)
    
    def load_data(self, equipment_items: list):
        """Load equipment data into the table"""
        self.equipment_data = equipment_items
        self.refresh_table()
    
    def refresh_table(self):
        """Refresh the table with current data"""
        self.table.setRowCount(len(self.equipment_data))
        
        for row, item in enumerate(self.equipment_data):
            # Handle different data formats
            name = str(item.get('equipment_name', item.get('name', '')))
            eq_type = str(item.get('type', item.get('equipment_type', '')))
            flowrate = float(item.get('flowrate', 0))
            pressure = float(item.get('pressure', 0))
            temperature = float(item.get('temperature', 0))
            
            # Create items with explicit bright white text color for maximum contrast
            # Use RGB values for pure white to ensure maximum visibility
            white_color = QColor(255, 255, 255)
            
            item0 = QTableWidgetItem(name)
            item0.setForeground(white_color)
            self.table.setItem(row, 0, item0)
            
            item1 = QTableWidgetItem(eq_type)
            item1.setForeground(white_color)
            self.table.setItem(row, 1, item1)
            
            item2 = QTableWidgetItem(f"{flowrate:.2f}")
            item2.setForeground(white_color)
            self.table.setItem(row, 2, item2)
            
            item3 = QTableWidgetItem(f"{pressure:.2f}")
            item3.setForeground(white_color)
            self.table.setItem(row, 3, item3)
            
            item4 = QTableWidgetItem(f"{temperature:.2f}")
            item4.setForeground(white_color)
            self.table.setItem(row, 4, item4)
        
        # Update statistics
        if self.equipment_data:
            avg_flowrate = sum(float(item.get('flowrate', 0)) for item in self.equipment_data) / len(self.equipment_data)
            avg_pressure = sum(float(item.get('pressure', 0)) for item in self.equipment_data) / len(self.equipment_data)
            avg_temp = sum(float(item.get('temperature', 0)) for item in self.equipment_data) / len(self.equipment_data)
            
            self.stats_label.setText(
                f"Total Items: {len(self.equipment_data)} | "
                f"Avg Flowrate: {avg_flowrate:.2f} L/min | "
                f"Avg Pressure: {avg_pressure:.2f} bar | "
                f"Avg Temperature: {avg_temp:.2f} °C"
            )
        else:
            self.stats_label.setText("No data loaded")
    
    def clear_data(self):
        """Clear the table"""
        self.table.setRowCount(0)
        self.equipment_data = []
        self.stats_label.setText("No data loaded")
