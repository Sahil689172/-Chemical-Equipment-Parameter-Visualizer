import React, { useMemo } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Line, Pie, Doughnut, Scatter } from 'react-chartjs-2';
import './ChartDisplay.css';

// Register all Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

// Color palette
const colors = {
  blue: {
    bg: 'rgba(54, 162, 235, 0.6)',
    border: 'rgba(54, 162, 235, 1)',
  },
  green: {
    bg: 'rgba(75, 192, 192, 0.6)',
    border: 'rgba(75, 192, 192, 1)',
  },
  orange: {
    bg: 'rgba(255, 159, 64, 0.6)',
    border: 'rgba(255, 159, 64, 1)',
  },
  purple: {
    bg: 'rgba(153, 102, 255, 0.6)',
    border: 'rgba(153, 102, 255, 1)',
  },
  red: {
    bg: 'rgba(255, 99, 132, 0.6)',
    border: 'rgba(255, 99, 132, 1)',
  },
};

// Generate color array for pie chart
const generatePieColors = (count) => {
  const colorArray = [
    colors.blue.bg,
    colors.green.bg,
    colors.orange.bg,
    colors.purple.bg,
    colors.red.bg,
  ];
  const borderArray = [
    colors.blue.border,
    colors.green.border,
    colors.orange.border,
    colors.purple.border,
    colors.red.border,
  ];
  
  // Repeat colors if needed
  const bgColors = [];
  const borderColors = [];
  for (let i = 0; i < count; i++) {
    bgColors.push(colorArray[i % colorArray.length]);
    borderColors.push(borderArray[i % borderArray.length]);
  }
  return { bgColors, borderColors };
};

function ChartDisplay({ chartData, equipmentItems, loading }) {
  // Donut chart data - Equipment Type Distribution - MUST be before early returns
  const donutChartData = useMemo(() => {
    if (!equipmentItems || equipmentItems.length === 0) return null;
    
    // Count equipment by type
    const typeCount = {};
    equipmentItems.forEach(item => {
      typeCount[item.type] = (typeCount[item.type] || 0) + 1;
    });
    
    const labels = Object.keys(typeCount);
    const data = Object.values(typeCount);
    const { bgColors, borderColors } = generatePieColors(labels.length);
    
    return {
      labels: labels,
      datasets: [
        {
          label: 'Equipment Count',
          data: data,
          backgroundColor: bgColors,
          borderColor: borderColors,
          borderWidth: 2,
        },
      ],
    };
  }, [equipmentItems]);

  // Scatter chart data - Pressure vs Temperature - MUST be before early returns
  const scatterChartData = useMemo(() => {
    if (!equipmentItems || equipmentItems.length === 0) return null;
    
    const data = equipmentItems.map(item => ({
      x: item.pressure,
      y: item.temperature,
      label: item.equipment_name,
    }));
    
    return {
      datasets: [
        {
          label: 'Equipment Points',
          data: data,
          backgroundColor: colors.orange.bg,
          borderColor: colors.orange.border,
          borderWidth: 2,
          pointRadius: 6,
          pointHoverRadius: 8,
          pointBackgroundColor: colors.orange.border,
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
        },
      ],
    };
  }, [equipmentItems]);

  if (loading) {
    return (
      <div className="chart-container">
        <h2>Data Visualizations</h2>
        <div className="loading-message">Loading chart data...</div>
      </div>
    );
  }

  if (!chartData || !chartData.labels || chartData.labels.length === 0) {
    return (
      <div className="chart-container">
        <h2>Data Visualizations</h2>
        <div className="empty-message">No chart data available</div>
      </div>
    );
  }

  // Bar chart data - Average Flowrate by Equipment Type
  const barChartData = {
    labels: chartData.labels,
    datasets: [
      {
        label: 'Average Flowrate (L/min)',
        data: chartData.flowrate,
        backgroundColor: colors.blue.bg,
        borderColor: colors.blue.border,
        borderWidth: 2,
      },
    ],
  };

  // Bar chart data - Average Pressure by Equipment Type
  const pressureBarChartData = {
    labels: chartData.labels,
    datasets: [
      {
        label: 'Average Pressure (bar)',
        data: chartData.pressure,
        backgroundColor: colors.purple.bg,
        borderColor: colors.purple.border,
        borderWidth: 2,
      },
    ],
  };

  // Common chart options
  const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          padding: 15,
          font: {
            size: 12,
            weight: '500',
          },
          color: '#ffffff',
          usePointStyle: true,
        },
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.9)',
        padding: 12,
        titleFont: {
          size: 14,
          weight: 'bold',
        },
        titleColor: '#ffffff',
        bodyFont: {
          size: 12,
        },
        bodyColor: '#ffffff',
        borderColor: 'rgba(255, 255, 255, 0.2)',
        borderWidth: 1,
        cornerRadius: 8,
        displayColors: true,
      },
    },
  };

  // Bar chart options
  const barChartOptions = {
    ...commonOptions,
    plugins: {
      ...commonOptions.plugins,
      title: {
        display: false,
      },
      tooltip: {
        ...commonOptions.plugins.tooltip,
        callbacks: {
          label: function(context) {
            return `Flowrate: ${context.parsed.y.toFixed(2)} L/min`;
          },
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Flowrate (L/min)',
          font: {
            size: 12,
            weight: 'bold',
          },
          color: '#ffffff',
        },
        ticks: {
          color: '#b0b0b0',
          callback: function(value) {
            return value.toFixed(0);
          },
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
      },
      x: {
        title: {
          display: true,
          text: 'Equipment Type',
          font: {
            size: 12,
            weight: 'bold',
          },
          color: '#ffffff',
        },
        ticks: {
          color: '#b0b0b0',
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
      },
    },
  };

  // Pressure bar chart options
  const pressureBarChartOptions = {
    ...commonOptions,
    plugins: {
      ...commonOptions.plugins,
      title: {
        display: false,
      },
      tooltip: {
        ...commonOptions.plugins.tooltip,
        callbacks: {
          label: function(context) {
            return `Pressure: ${context.parsed.y.toFixed(2)} bar`;
          },
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Pressure (bar)',
          font: {
            size: 12,
            weight: 'bold',
          },
          color: '#ffffff',
        },
        ticks: {
          color: '#b0b0b0',
          callback: function(value) {
            return value.toFixed(1);
          },
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
      },
      x: {
        title: {
          display: true,
          text: 'Equipment Type',
          font: {
            size: 12,
            weight: 'bold',
          },
          color: '#ffffff',
        },
        ticks: {
          color: '#b0b0b0',
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
      },
    },
  };

  // Scatter chart options
  const scatterChartOptions = {
    ...commonOptions,
    plugins: {
      ...commonOptions.plugins,
      title: {
        display: false,
      },
      tooltip: {
        ...commonOptions.plugins.tooltip,
        callbacks: {
          title: function(context) {
            return context[0].raw.label || 'Equipment';
          },
          label: function(context) {
            return [
              `Pressure: ${context.parsed.x.toFixed(2)} bar`,
              `Temperature: ${context.parsed.y.toFixed(2)} °C`,
            ];
          },
        },
      },
    },
    scales: {
      x: {
        type: 'linear',
        position: 'bottom',
        title: {
          display: true,
          text: 'Pressure (bar)',
          font: {
            size: 12,
            weight: 'bold',
          },
          color: '#ffffff',
        },
        ticks: {
          color: '#b0b0b0',
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
      },
      y: {
        title: {
          display: true,
          text: 'Temperature (°C)',
          font: {
            size: 12,
            weight: 'bold',
          },
          color: '#ffffff',
        },
        ticks: {
          color: '#b0b0b0',
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
      },
    },
  };

  // Donut chart options
  const donutChartOptions = {
    ...commonOptions,
    cutout: '60%', // Makes it a donut chart
    plugins: {
      ...commonOptions.plugins,
      title: {
        display: false,
      },
      legend: {
        ...commonOptions.plugins.legend,
        position: 'right',
        labels: {
          ...commonOptions.plugins.legend.labels,
          padding: 20,
          font: {
            size: 11,
          },
          color: '#ffffff',
        },
      },
      tooltip: {
        ...commonOptions.plugins.tooltip,
        callbacks: {
          label: function(context) {
            const label = context.label || '';
            const value = context.parsed || 0;
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = ((value / total) * 100).toFixed(1);
            return `${label}: ${value} (${percentage}%)`;
          },
        },
      },
    },
  };

  return (
    <div className="chart-container">
      <div className="charts-grid">
        {/* Bar Chart - Flowrate Distribution */}
        <div className="chart-card">
          <h3 className="chart-title">Flowrate Distribution</h3>
          <div className="chart-wrapper">
            <Bar data={barChartData} options={barChartOptions} />
          </div>
        </div>

        {/* Donut Chart - Equipment Breakdown */}
        <div className="chart-card">
          <h3 className="chart-title">Equipment Breakdown</h3>
          {donutChartData ? (
            <div className="chart-wrapper donut-wrapper">
              <Doughnut data={donutChartData} options={donutChartOptions} />
            </div>
          ) : (
            <div className="chart-placeholder">
              <p>No equipment data available</p>
            </div>
          )}
        </div>

        {/* Bar Chart - Pressure Distribution */}
        <div className="chart-card">
          <h3 className="chart-title">Pressure Distribution</h3>
          <div className="chart-wrapper">
            <Bar data={pressureBarChartData} options={pressureBarChartOptions} />
          </div>
        </div>

        {/* Scatter Chart - Pressure vs Temperature */}
        <div className="chart-card">
          <h3 className="chart-title">Pressure vs Temperature</h3>
          {scatterChartData ? (
            <div className="chart-wrapper">
              <Scatter data={scatterChartData} options={scatterChartOptions} />
            </div>
          ) : (
            <div className="chart-placeholder">
              <p>No equipment data available</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ChartDisplay;
