// Serviço mock para desenvolvimento/teste
export const mockAwsService = {
  /**
   * Simula upload de imagem para S3
   */
  uploadImageToS3: async (file) => {
    // Simula delay de upload
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    return {
      success: true,
      key: `mock-images/${Date.now()}-${file.name}`,
      etag: '"mock-etag-12345"',
      location: `https://mock-bucket.s3.us-east-1.amazonaws.com/mock-images/${Date.now()}-${file.name}`,
    };
  },

  /**
   * Simula processamento de detecção de placa
   */
  processPlateDetection: async (s3Key) => {
    // Simula delay de processamento
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // Gera resultado mock baseado no nome do arquivo
    const mockPlates = ['ABC-1234', 'XYZ-5678', 'DEF-9012', 'GHI-3456'];
    const randomPlate = mockPlates[Math.floor(Math.random() * mockPlates.length)];
    const isRegular = Math.random() > 0.5; // 50% chance de ser regular
    const confidence = 0.85 + (Math.random() * 0.15); // 85-100% confiança
    
    return {
      plateNumber: randomPlate,
      isRegular: isRegular,
      confidence: confidence,
      detectionDetails: isRegular 
        ? 'Veículo regular - documentação em ordem' 
        : 'Veículo irregular - pendências encontradas',
      timestamp: new Date().toISOString(),
      rawResponse: {
        mockData: true,
        s3Key: s3Key,
        processingTime: '3.2s'
      },
    };
  },

  /**
   * Valida arquivo de imagem
   */
  validateImageFile: (file) => {
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
    const maxSize = 10 * 1024 * 1024; // 10MB

    if (!validTypes.includes(file.type)) {
      return {
        isValid: false,
        error: 'Formato de arquivo não suportado. Use JPG, PNG ou GIF.',
      };
    }

    if (file.size > maxSize) {
      return {
        isValid: false,
        error: 'Arquivo muito grande. O tamanho máximo é 10MB.',
      };
    }

    return {
      isValid: true,
      error: null,
    };
  },
};

// Exemplos de resultados mock para diferentes cenários
export const mockResults = {
  regular: {
    plateNumber: 'ABC-1234',
    isRegular: true,
    confidence: 0.95,
    detectionDetails: 'Veículo regular - documentação em ordem',
    timestamp: new Date().toISOString(),
  },
  
  irregular: {
    plateNumber: 'XYZ-5678',
    isRegular: false,
    confidence: 0.88,
    detectionDetails: 'Veículo irregular - pendências de IPVA encontradas',
    timestamp: new Date().toISOString(),
  },
  
  lowConfidence: {
    plateNumber: 'DEF-9012',
    isRegular: true,
    confidence: 0.72,
    detectionDetails: 'Placa detectada com baixa confiança - verifique a qualidade da imagem',
    timestamp: new Date().toISOString(),
  },
  
  noPlateDetected: {
    plateNumber: null,
    isRegular: false,
    confidence: 0.0,
    detectionDetails: 'Nenhuma placa foi detectada na imagem',
    timestamp: new Date().toISOString(),
  }
};