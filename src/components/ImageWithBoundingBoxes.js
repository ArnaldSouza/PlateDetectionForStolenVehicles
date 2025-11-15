import React, { useRef, useEffect } from 'react';

const ImageWithBoundingBoxes = ({ imageUrl, boundingBoxes, className }) => {
  const canvasRef = useRef(null);
  const imageRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const image = imageRef.current;
    
    if (!canvas || !image || !boundingBoxes || boundingBoxes.length === 0) return;

    const drawBoundingBoxes = () => {
      const ctx = canvas.getContext('2d');
      const rect = image.getBoundingClientRect();
      
      // Ajustar canvas para o tamanho da imagem exibida
      canvas.width = image.clientWidth;
      canvas.height = image.clientHeight;
      
      // Calcular escala entre imagem original e exibida
      const scaleX = image.clientWidth / image.naturalWidth;
      const scaleY = image.clientHeight / image.naturalHeight;
      
      // Limpar canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Desenhar retângulos para cada placa
      boundingBoxes.forEach((coords, index) => {
        if (coords && coords.length === 4) {
          const [x1, y1, x2, y2] = coords;
          
          // Aplicar escala às coordenadas
          const scaledX1 = x1 * scaleX;
          const scaledY1 = y1 * scaleY;
          const scaledX2 = x2 * scaleX;
          const scaledY2 = y2 * scaleY;
          
          // Configurar estilo do retângulo
          ctx.strokeStyle = '#ff0000'; // Vermelho
          ctx.lineWidth = 3;
          ctx.setLineDash([]);
          
          // Desenhar retângulo
          ctx.strokeRect(
            scaledX1, 
            scaledY1, 
            scaledX2 - scaledX1, 
            scaledY2 - scaledY1
          );
          
          // Fundo branco para o texto
          const boxWidth = 30;
          const boxHeight = 25;
          ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
          ctx.fillRect(scaledX1, scaledY1 - boxHeight, boxWidth, boxHeight);
          
          // Adicionar número da placa centralizado
          ctx.fillStyle = '#ff0000';
          ctx.font = 'bold 16px Arial';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          
          // Calcular posição central do quadrado
          const centerX = scaledX1 + boxWidth / 2;
          const centerY = scaledY1 - boxHeight / 2;
          
          ctx.fillText(`${index + 1}`, centerX, centerY);
          
          // Resetar alinhamento para não afetar outros desenhos
          ctx.textAlign = 'start';
          ctx.textBaseline = 'alphabetic';
        }
      });
    };

    // Aguardar imagem carregar
    if (image.complete && image.naturalHeight !== 0) {
      drawBoundingBoxes();
    } else {
      image.onload = drawBoundingBoxes;
    }

    // Redesenhar quando a janela redimensionar
    const handleResize = () => {
      setTimeout(drawBoundingBoxes, 100);
    };
    
    window.addEventListener('resize', handleResize);
    
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, [imageUrl, boundingBoxes]);

  return (
    <div style={{ position: 'relative', display: 'inline-block' }}>
      <img
        ref={imageRef}
        src={imageUrl}
        alt="Imagem com detecções"
        className={className}
        style={{ display: 'block' }}
      />
      <canvas
        ref={canvasRef}
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          pointerEvents: 'none',
          zIndex: 1
        }}
      />
    </div>
  );
};

export default ImageWithBoundingBoxes;