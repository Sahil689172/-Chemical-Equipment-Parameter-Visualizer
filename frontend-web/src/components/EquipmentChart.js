import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import './EquipmentChart.css';

function EquipmentChart({ data }) {
  const chartData = data.map(item => ({
    name: item.name,
    Flowrate: item.flowrate,
    Pressure: item.pressure,
    Temperature: item.temperature
  }));

  return (
    <div className="equipment-chart-container">
      <h2>Equipment Parameters Visualization</h2>
      <div className="chart-wrapper">
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="name" 
              angle={-45} 
              textAnchor="end" 
              height={100}
              interval={0}
            />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="Flowrate" fill="#8884d8" />
            <Bar dataKey="Pressure" fill="#82ca9d" />
            <Bar dataKey="Temperature" fill="#ffc658" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default EquipmentChart;
