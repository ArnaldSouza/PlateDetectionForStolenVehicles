// Serviço local para detecção de placas (sem AWS)
import { CONFIG } from '../config/config';

/**
 * Simula processamento local de imagem
 * @param {File} file - Arquivo de imagem
 * @returns {Promise<Object>} - Resposta com os dados da detecção
 */
export const processLocalImage = async (file) => {
  // Simula delay de processamento
  await new Promise(resolve => setTimeout(resolve, CONFIG.local.mockDelay));
  
  // Gera resultado mock baseado no nome do arquivo
  const mockPlates = ['ABC-1234', 'XYZ-5678', 'DEF-9012', 'GHI-3456', 'JKL-7890'];
  const randomPlate = mockPlates[Math.floor(Math.random() * mockPlates.length)];
  const isRegular = Math.random() > 0.3; // 70% chance de ser regular
  const confidence = 0.80 + (Math.random() * 0.20); // 80-100% confiança
  
  return {
    plateNumber: randomPlate,
    isRegular: isRegular,
    confidence: confidence,
    detectionDetails: isRegular 
      ? 'Veículo regular - documentação em ordem' 
      : 'Veículo irregular - pendências encontradas',
    timestamp: new Date().toISOString(),
    processingInfo: {
      mode: 'local',
      fileName: file.name,
      fileSize: file.size,
      processingTime: `${CONFIG.local.mockDelay / 1000}s`
    },
  };
};

/**
 * Valida arquivo de imagem
 * @param {File} file - Arquivo para validar
 * @returns {Object} - Resultado da validação
 */
export const validateImageFile = (file) => {
  const errors = [];
  
  // Verificar tipo de arquivo
  if (!CONFIG.upload.allowedTypes.includes(file.type)) {
    errors.push(`Tipo de arquivo não suportado: ${file.type}`);
  }
  
  // Verificar extensão
  const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
  if (!CONFIG.upload.allowedExtensions.includes(fileExtension)) {
    errors.push(`Extensão não suportada: ${fileExtension}`);
  }
  
  // Verificar tamanho
  if (file.size > CONFIG.upload.maxFileSize) {
    const maxSizeMB = CONFIG.upload.maxFileSize / (1024 * 1024);
    errors.push(`Arquivo muito grande. Máximo: ${maxSizeMB}MB`);
  }
  
  return {
    isValid: errors.length === 0,
    errors,
    fileInfo: {
      name: file.name,
      size: file.size,
      type: file.type,
    },
  };
};