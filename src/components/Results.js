import React from 'react';
import './Results.css';

const Results = ({ results }) => {
  const {
    plateNumber,
    isRegular,
    detectionDetails,
    timestamp,   
    scoreFinal,
    situacao,
    detalhes_situacao
  } = results;

  return (
    <div className="results-container">
      <h3>Resultado da Análise</h3>
      
      <div className="result-card">
        <div className={`status-indicator ${isRegular ? 'regular' : 'irregular'}`}>
          <div className="status-icon">
            {isRegular ? '✅' : '❌'}
          </div>
          <div className="status-text">
            <h4>{isRegular ? 'VEÍCULO REGULAR' : 'VEÍCULO ROUBADO'}</h4>
            <p>{detectionDetails}</p>
          </div>
        </div>

        {plateNumber && (
          <div className="plate-info">
            <h5>Placa Detectada</h5>
            <div className="plate-number">
              {plateNumber}
            </div>            
          </div>
        )}

        <div className="detection-details">
          <div className="detail-item">
            <span className="detail-label">Confiança Total:</span>
            <span className="detail-value">
              {scoreFinal ? `${(scoreFinal * 100).toFixed(1)}%` : 'N/A'}
            </span>
          </div>  

          <div className="detail-item">
            <span className="detail-label">Situação:</span>
            <span className={`situacao ${situacao ? situacao.toLowerCase() : ''}`}>
              {situacao || 'N/A'}
            </span>
          </div>

           <div className="detail-item">
            <span className="detail-label">Detalhes:</span>
            <span className="detail-value">{detalhes_situacao || 'N/A'}</span>
          </div>

          {timestamp && (
            <div className="detail-item">
              <span className="detail-label">Processado em:</span>
              <span className="detail-value">
                {new Date(timestamp).toLocaleString('pt-BR')}
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Results;