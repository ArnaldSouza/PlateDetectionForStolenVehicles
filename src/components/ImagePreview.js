import React from 'react';
import './ImagePreview.css';
import ImageWithBoundingBoxes from './ImageWithBoundingBoxes';

const ImagePreview = ({ imagePreview, boundingBoxes }) => {
  return (
    <div className="image-preview-container">
      <h3>Prévia da Imagem</h3>
      <div className="image-preview-wrapper">
        {boundingBoxes && boundingBoxes.length > 0 ? (
          <ImageWithBoundingBoxes
            imageUrl={imagePreview}
            boundingBoxes={boundingBoxes}
            className="preview-image"
          />
        ) : (
          <img 
            src={imagePreview} 
            alt="Prévia da imagem selecionada" 
            className="preview-image"
          />
        )}
      </div>
    </div>
  );
};

export default ImagePreview;