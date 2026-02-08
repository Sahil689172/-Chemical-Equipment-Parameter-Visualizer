import React from 'react';
import './EquipmentList.css';

function EquipmentList({ equipment }) {
  return (
    <div className="equipment-list-container">
      <h2>Equipment List</h2>
      <div className="equipment-table-wrapper">
        <table className="equipment-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Flowrate (L/min)</th>
              <th>Pressure (bar)</th>
              <th>Temperature (°C)</th>
            </tr>
          </thead>
          <tbody>
            {equipment.map((item) => (
              <tr key={item.id}>
                <td>{item.name}</td>
                <td>{item.equipment_type}</td>
                <td>{item.flowrate.toFixed(2)}</td>
                <td>{item.pressure.toFixed(2)}</td>
                <td>{item.temperature.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default EquipmentList;
