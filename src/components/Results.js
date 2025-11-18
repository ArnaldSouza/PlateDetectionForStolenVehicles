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
    detalhes_situacao,
    cropPlaca,
    tipoPlaca,
    todasPlacas
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

        {/* Seção de placas - layout unificado para uma ou múltiplas */}
        {todasPlacas && todasPlacas.length > 0 ? (
          <div className="all-plates-section">
            <h5>
              {todasPlacas.length === 1 
                ? 'Placa Detectada' 
                : `Placas Detectadas (${todasPlacas.length})`
              }
            </h5>
            <div className={`plates-grid ${todasPlacas.length === 1 ? 'single-plate' : ''}`}>
              {todasPlacas.map((placa, index) => (
                <div key={index} className={`plate-card ${todasPlacas.length === 1 ? 'plate-card-single' : ''}`}>
                  <div className="plate-header">
                    <span className="plate-index">#{index + 1}</span>
                    <span className={`plate-status ${placa.situacao.toLowerCase()}`}>
                      {placa.situacao}
                    </span>
                  </div>
                  
                  <div className="plate-number">
                    {placa.texto}
                  </div>
                  
                                   
                  {placa.crop_placa && (
                    <div className="plate-crop-mini">
                      <img 
                        src={placa.crop_placa} 
                        alt={`Crop da placa ${placa.texto}`} 
                        className={`plate-crop-image-mini ${todasPlacas.length === 1 ? 'single' : ''}`}
                      />
                    </div>
                  )}
                  
                  <div className="plate-details-mini">                    
                    <div className="detail-mini">
                      <span>Situação:</span>
                      <span className={`situacao-mini ${placa.situacao.toLowerCase()}`}>
                        {placa.situacao}
                      </span>
                    </div>
                    <div className="detail-mini">
                      <span>Detalhes:</span>
                      <span className="detail-value-mini">
                        {placa.detalhes_situacao}
                      </span>
                    </div>
                    <div className="detail-mini">
                      <span>Modelo:</span>
                      <span className="detail-value-mini">
                        {placa.modelo_deteccao || 'N/A'}
                      </span>
                    </div>
                    <div className="detail-mini">
                      <span>Conf. Detecção:</span>
                      <span className="detail-value-mini">
                        {placa.confianca_deteccao ? (placa.confianca_deteccao * 100).toFixed(1) + '%' : 'N/A'}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : plateNumber && (
          /* Fallback para compatibilidade */
          <div className="plate-info">
            <h5>Placa Detectada</h5>
            <div className="plate-number">
              {plateNumber}
            </div>
            {tipoPlaca && (
              <div className="plate-type">
                Tipo: {tipoPlaca}
              </div>
            )}
          </div>
        )}

        {/* Mostrar crop da placa principal apenas no fallback */}
        {cropPlaca && !todasPlacas && (
          <div className="plate-crop-section">
            <h5>Região Detectada</h5>
            <div className="plate-crop-container">
              <img 
                src={cropPlaca} 
                alt="Crop da placa detectada" 
                className="plate-crop-image"
              />
              <div className="crop-info">
                <span className="crop-label">Área recortada da detecção</span>
              </div>
            </div>
          </div>
        )}       

        {/* Detalhes gerais - apenas timestamp para evitar duplicação */}
        <div className="detection-details">
          {/* Timestamp sempre visível */}
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