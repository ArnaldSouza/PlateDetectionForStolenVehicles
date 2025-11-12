// Configurações para desenvolvimento local
export const CONFIG = {
  // Modo de desenvolvimento
  isDevelopment: process.env.NODE_ENV === 'development',
  
  // Upload Settings
  upload: {
    maxFileSize: 10 * 1024 * 1024, // 10MB
    allowedTypes: ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'],
    allowedExtensions: ['.jpg', '.jpeg', '.png', '.gif'],
  },
  
  // Configurações locais
  local: {
    mockDelay: 3000, // 3 segundos para simular processamento
  }
};

// Função para validar configuração
export const validateConfig = () => {
  return {
    isValid: true,
    errors: [],
    isDemoMode: true, // Sempre em modo local agora
  };
};