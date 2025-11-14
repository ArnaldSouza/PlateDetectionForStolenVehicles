import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import ImageUpload from './ImageUpload';
import ImagePreview from './ImagePreview';
import ProcessingStatus from './ProcessingStatus';
import Results from './Results';
import './PlateDetectionApp.css';

const PlateDetectionApp = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingStatus, setProcessingStatus] = useState('');
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [resetImageUpload, setResetImageUpload] = useState(0);
  
  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setSelectedImage(file);
      setImagePreview(URL.createObjectURL(file));
      setResults(null);
      setError(null);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif']
    },
    maxFiles: 1
  });

  const handleImageProcessed = (data) => {
    // Converter a resposta da API para o formato esperado pelo componente Results
    const formattedResults = {
      plateNumber: data.placa,
      isRegular: data.situacao === 'REGULAR',
      confidence: data.confianca,
      detectionDetails: data.detalhes_situacao,
      timestamp: new Date().toISOString(),
      scoreFinal: data.score_final,
      situacao: data.situacao,
      detalhes_situacao: data.detalhes_situacao
    };

    setResults(formattedResults);
    setProcessingStatus('Processamento concluído!');
  };

  // Adicione esta nova função para quando a imagem for selecionada
  const handleImageSelected = (file) => {
    setSelectedImage(file);

    // Criar URL para prévia da imagem
    const previewUrl = URL.createObjectURL(file);
    setImagePreview(previewUrl);

    setError(null);
    setResults(null);
  };

  const handleReset = () => {
    setSelectedImage(null);

    if (imagePreview) {
      URL.revokeObjectURL(imagePreview);
    }

    setImagePreview(null);
    setResults(null);
    setError(null);
    setProcessingStatus('');
    setIsProcessing(false);
    setResetImageUpload(prev => prev + 1);
  };

  return (
    <div className="plate-detection-app">
      <header className="app-header">
        <h1>Sistema de Detecção de Placas Veiculares</h1>
        <p>Faça o upload da imagem para verificar a situação do carro</p>
      </header>

      <main className="app-main">
        <div className="upload-section">
          <ImageUpload
            onImageProcessed={handleImageProcessed}
            onImageSelected={handleImageSelected}
            resetTrigger={resetImageUpload}
          />
        </div>

        

        {error && (
          <div className="error-section">
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          </div>
        )}

        {results && (
          <div className="results-section">
            <Results results={results} />
            <button
              className="reset-button"
              onClick={handleReset}
            >
              Analisar Nova Imagem
            </button>
          </div>
        )}

        {imagePreview && (
          <div className="preview-section">
            <ImagePreview imagePreview={imagePreview} />
          </div>
        )}
      </main>
    </div>
  );
};

export default PlateDetectionApp;