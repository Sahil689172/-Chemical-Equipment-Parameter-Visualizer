"""
Table Widget for displaying equipment data
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QLabel, QHBoxLayout, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class TableWidget(QWidget):
    """Widget for displaying equipment data in a table"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.equipment_data = []
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Equipment Data")
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
        
        # Style the table
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background: white;
                gridline-color: #e2e8f0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background: #e6fffa;
                color: #2d3748;
            }
            QHeaderView::section {
                background: #667eea;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)
        
        # Configure table behavior
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.table)
        
        # Statistics label
        self.stats_label = QLabel("No data loaded")
        self.stats_label.setStyleSheet("""
            color: #718096;
            padding: 10px;
            background: #f7fafc;
            border-radius: 6px;
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
            
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(eq_type))
            self.table.setItem(row, 2, QTableWidgetItem(f"{flowrate:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{pressure:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{temperature:.2f}"))
        
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
