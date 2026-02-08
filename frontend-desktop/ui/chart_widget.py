"""
Chart Widget with Matplotlib for data visualization
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np


class ChartWidget(QWidget):
    """Widget for displaying charts using Matplotlib"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chart_data = None
        self.equipment_items = []
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Data Visualizations")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2d3748;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        refresh_btn = QPushButton("Refresh Charts")
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
        refresh_btn.clicked.connect(self.refresh_charts)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Create figure with subplots
        self.figure = Figure(figsize=(12, 10))
        self.canvas = FigureCanvas(self.figure)
        
        # Create toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        
        # Add canvas
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
        
        # Set matplotlib style
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def load_data(self, chart_data: dict, equipment_items: list = None):
        """Load chart data and equipment items"""
        self.chart_data = chart_data
        self.equipment_items = equipment_items or []
        self.refresh_charts()
    
    def refresh_charts(self):
        """Refresh all charts with current data"""
        if not self.chart_data:
            return
        
        self.figure.clear()
        
        # Create 3 subplots in a grid (2 rows, 2 cols - pie chart takes 2 spaces)
        gs = self.figure.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # 1. Bar Chart - Average Flowrate by Equipment Type
        ax1 = self.figure.add_subplot(gs[0, 0])
        if self.chart_data.get('labels') and self.chart_data.get('flowrate'):
            labels = self.chart_data['labels']
            flowrates = self.chart_data['flowrate']
            
            colors_bar = ['#4A90E2', '#50C878', '#FF6B6B', '#9F7AEA', '#ED8936']
            bars = ax1.bar(labels, flowrates, color=colors_bar[:len(labels)], edgecolor='white', linewidth=1.5)
            ax1.set_title('Average Flowrate by Equipment Type', fontsize=14, fontweight='bold', pad=15)
            ax1.set_xlabel('Equipment Type', fontsize=11, fontweight='bold')
            ax1.set_ylabel('Flowrate (L/min)', fontsize=11, fontweight='bold')
            ax1.grid(True, alpha=0.3, linestyle='--')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}',
                        ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # 2. Scatter Plot - Pressure vs Temperature
        ax2 = self.figure.add_subplot(gs[0, 1])
        if self.equipment_items:
            pressures = [float(item.get('pressure', 0)) for item in self.equipment_items]
            temperatures = [float(item.get('temperature', 0)) for item in self.equipment_items]
            
            scatter = ax2.scatter(pressures, temperatures, c='#4A90E2', s=100, alpha=0.6, edgecolors='white', linewidth=1.5)
            ax2.set_title('Pressure vs Temperature', fontsize=14, fontweight='bold', pad=15)
            ax2.set_xlabel('Pressure (bar)', fontsize=11, fontweight='bold')
            ax2.set_ylabel('Temperature (°C)', fontsize=11, fontweight='bold')
            ax2.grid(True, alpha=0.3, linestyle='--')
        
        # 3. Pie Chart - Equipment Type Distribution
        ax3 = self.figure.add_subplot(gs[1, :])
        if self.equipment_items:
            # Count equipment by type
            type_count = {}
            for item in self.equipment_items:
                eq_type = item.get('type', 'Unknown')
                type_count[eq_type] = type_count.get(eq_type, 0) + 1
            
            if type_count:
                labels_pie = list(type_count.keys())
                sizes = list(type_count.values())
                colors_pie = ['#4A90E2', '#50C878', '#FF6B6B', '#9F7AEA', '#ED8936', '#F6AD55', '#68D391']
                
                wedges, texts, autotexts = ax3.pie(
                    sizes, labels=labels_pie, colors=colors_pie[:len(labels_pie)],
                    autopct='%1.1f%%', startangle=90,
                    textprops={'fontsize': 10, 'fontweight': 'bold'},
                    wedgeprops={'edgecolor': 'white', 'linewidth': 2}
                )
                ax3.set_title('Equipment Type Distribution', fontsize=14, fontweight='bold', pad=15)
        
        # Refresh canvas
        self.canvas.draw()
    
    def clear_charts(self):
        """Clear all charts"""
        self.figure.clear()
        self.canvas.draw()
        self.chart_data = None
        self.equipment_items = []
