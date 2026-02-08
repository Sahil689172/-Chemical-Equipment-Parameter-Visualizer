import React from 'react';
import './Summary.css';

function Summary({ summary, loading }) {
  if (loading) {
    return (
      <div className="summary-container">
        <div className="loading-message">Loading summary...</div>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="summary-container">
        <div className="empty-message">No summary data available</div>
      </div>
    );
  }

  const summaryCards = [
    {
      label: 'Total Equipment',
      value: summary.total_count || 0,
      icon: '🖥️',
      color: 'card-blue',
      unit: '',
      change: '+12%',
      changeType: 'positive',
      subtitle: 'Active Monitoring'
    },
    {
      label: 'Avg Flowrate',
      value: summary.averages?.flowrate?.toFixed(1) || '0.0',
      icon: '💧',
      color: 'card-green',
      unit: ' m³/h',
      subtitle: 'Standardized Flow'
    },
    {
      label: 'Avg Pressure',
      value: summary.averages?.pressure?.toFixed(1) || '0.0',
      icon: '⚠️',
      color: 'card-purple',
      unit: ' Bar',
      change: '-1% vs Target',
      changeType: 'negative',
      subtitle: ''
    },
    {
      label: 'Avg Temperature',
      value: summary.averages?.temperature?.toFixed(1) || '0.0',
      icon: '🌡️',
      color: 'card-orange',
      unit: ' °C',
      subtitle: 'Within Safety Limit'
    }
  ];

  return (
    <div className="summary-container">
      <div className="summary-grid">
        {summaryCards.map((card, index) => (
          <div key={index} className={`summary-card ${card.color}`}>
            <div className="card-header">
              <div className="card-icon">{card.icon}</div>
              {card.change && (
                <span className={`card-change ${card.changeType}`}>
                  {card.change}
                </span>
              )}
            </div>
            <div className="card-content">
              <div className="summary-label">{card.label}</div>
              <div className="summary-value-wrapper">
                <span className="summary-value">{card.value}</span>
                <span className="summary-unit">{card.unit}</span>
              </div>
              {card.subtitle && (
                <div className="card-subtitle">{card.subtitle}</div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Summary;
