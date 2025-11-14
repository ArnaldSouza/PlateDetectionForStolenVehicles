import React, { useState, useCallback, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import './ImageUpload.css';

const ImageUpload = ({ onImageProcessed, onImageSelected, resetTrigger }) => {
  const [hasImage, setHasImage] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleReset = () => {
    setHasImage(false);
    setIsProcessing(false);
    setError(null);
    setUploadStatus('');
  };

  useEffect(() => {
    if (resetTrigger > 0) {
      handleReset();
    }
  }, [resetTrigger]);

  // Função que é chamada quando o usuário solta ou escolhe uma imagem
  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setError(null);
      setHasImage(true);

      if (onImageSelected) {
        onImageSelected(file);
      }

      enviarImagem(file);
    }
  }, [onImageSelected]);

  // Envia a imagem para o backend Flask
  const enviarImagem = async (file) => {
    setIsProcessing(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.erro || 'Erro ao processar imagem');
      }

      if (data.detectado) {
        if (onImageProcessed) {
          onImageProcessed(data);
        }
      } else {
        setError(data.erro || 'Nenhuma placa detectada');
      }

    } catch (error) {
      console.error('Erro ao enviar imagem:', error);
      setError(error.message || 'Erro ao processar imagem');
    } finally {
      setIsProcessing(false);
    }
  };

  // Configuração do Dropzone
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <div className="upload-wrapper">
      <div
        {...getRootProps()}
        className={`upload-container ${isDragActive ? 'drag-active' : ''} ${hasImage ? 'has-image' : ''}`}
      >
        <input {...getInputProps()} />
        <div className="upload-content">
          <div className="upload-icon">📸</div>

          {isDragActive ? (
            <div className="upload-text">
              <h3>Solte a imagem aqui...</h3>
            </div>
          ) : (
            <div className="upload-text">
              <h3>Clique ou arraste uma imagem aqui</h3>
              <p>Formatos suportados: JPG, JPEG, PNG, GIF</p>
              <p>Tamanho máximo: 10MB</p>
            </div>
          )}

          {hasImage && !isProcessing && (
            <div className="upload-success">
              <span className="success-icon">✅</span>
              <span>Imagem carregada com sucesso!</span>
            </div>
          )}

          {isProcessing && (
            <div className="upload-processing">
              <span className="processing-icon">⏳</span>
              <span>Processando imagem...</span>
            </div>
          )}
        </div>
      </div>

      {/* Exibição de erro */}
      {error && (
        <div className="error-message">
          <span className="error-icon">⚠️</span>
          {error}
        </div>
      )}     
      
    </div>
  );
};

export default ImageUpload;