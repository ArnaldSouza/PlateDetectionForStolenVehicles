import React from 'react';
import './ProcessingStatus.css';

const ProcessingStatus = ({ status }) => {
  return (
    <div className="processing-status-container">
      <div className="processing-content">
        <div className="loading-spinner">
          <div className="spinner"></div>
        </div>
        <div className="status-text">
          <h3>Processando...</h3>
          <p>{status}</p>
        </div>
      </div>
    </div>
  );
};

export default ProcessingStatus;