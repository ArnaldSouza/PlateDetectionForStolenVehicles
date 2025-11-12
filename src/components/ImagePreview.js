import React from 'react';
import './ImagePreview.css';

const ImagePreview = ({ imagePreview }) => {
  return (
    <div className="image-preview-container">
      <h3>Prévia da Imagem</h3>
      <div className="image-preview-wrapper">
        <img 
          src={imagePreview} 
          alt="Prévia da imagem selecionada" 
          className="preview-image"
        />
      </div>
    </div>
  );
};

export default ImagePreview;