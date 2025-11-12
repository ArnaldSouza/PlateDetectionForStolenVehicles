# Sistema de Detecção de Placas para Veículos Roubados/Furtados

Um sistema completo de detecção automática de placas veiculares desenvolvido com inteligência artificial. O sistema utiliza modelos de deep learning (YOLOv8 e Faster R-CNN) para detectar placas em imagens e verificar automaticamente se o veículo está na lista de veículos irregulares.

## 🚀 Características Principais

- **Detecção Inteligente**: Utiliza YOLOv8 e Faster R-CNN para detecção precisa de placas
- **OCR Avançado**: Reconhecimento de caracteres com EasyOCR em português e inglês
- **Verificação Automática**: Consulta automática em base de dados de veículos irregulares
- **Interface Web Moderna**: Frontend React responsivo com upload drag-and-drop
- **API RESTful**: Backend Flask para processamento das imagens
- **Suporte a Múltiplos Formatos**: Aceita imagens PNG, JPG, JPEG e GIF
- **Processamento Local**: Funciona completamente offline após configuração

## 🏗️ Arquitetura do Sistema

### Frontend (React)
- Interface web responsiva para upload e visualização
- Componentes modulares para upload, preview e resultados
- Comunicação com API backend via HTTP

### Backend (Flask + IA)
- API REST para processamento de imagens
- Modelos de IA para detecção de placas
- Sistema de verificação contra base de dados irregular
- Processamento com OpenCV e PyTorch

### Modelos de IA
- **YOLOv8**: Detecção rápida e precisa de placas
- **Faster R-CNN**: Detecção robusta como fallback
- **EasyOCR**: Reconhecimento óptico de caracteres

## 🛠️ Tecnologias Utilizadas

### Frontend
- **React 18** - Framework frontend
- **React Dropzone** - Upload drag-and-drop
- **Styled Components** - Estilização moderna
- **Axios** - Comunicação com API

### Backend
- **Flask** - Framework web Python
- **PyTorch** - Framework de deep learning
- **YOLOv8 (Ultralytics)** - Detecção de objetos
- **Faster R-CNN** - Modelo de detecção
- **EasyOCR** - Reconhecimento de caracteres
- **OpenCV** - Processamento de imagens
- **Flask-CORS** - Comunicação cross-origin

## 📋 Pré-requisitos

- **Node.js 16+** para o frontend
- **Python 3.8+** para o backend
- **CUDA** (opcional, para aceleração GPU)
- **Modelos treinados** (yolo.pt e faster.pt na pasta `backend/modelos/`)

## 🔧 Instalação e Configuração

### 1. Clone o Repositório
```bash
git clone https://github.com/ArnaldSouza/PlateDetectionForStolenVehicles.git
cd PlateDetectionForStolenVehicles
```

### 2. Configurar Backend
```bash
cd backend

# Criar ambiente virtual (recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
# ou source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Adicionar modelos treinados na pasta modelos/
# - yolo.pt (modelo YOLOv8 treinado)
# - faster.pt (modelo Faster R-CNN treinado)
```

### 3. Configurar Frontend
```bash
cd ../  # voltar para raiz do projeto
npm install
```

### 4. Executar o Sistema

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
# Servidor rodará em http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
npm start
# Interface web em http://localhost:3000
```

## 🎯 Como Usar

1. **Acesse a aplicação** em `http://localhost:3000`
2. **Faça upload de uma imagem** arrastando ou clicando para selecionar
3. **Clique em "Analisar Imagem"** para iniciar o processamento
4. **Visualize os resultados:**
   - Número da placa detectada
   - Status (REGULAR/IRREGULAR)
   - Nível de confiança da detecção
   - Tipo de placa (Mercosul/Antiga)
   - Tempo de processamento

## 📊 Fluxo de Processamento

1. **Upload da Imagem**: Frontend envia imagem para API `/upload`
2. **Pré-processamento**: Validação de formato e tamanho
3. **Detecção de Placas**: 
   - Modelo YOLOv8 tenta detectar placas primeiro
   - Se falhar, usa Faster R-CNN como backup
4. **OCR**: EasyOCR extrai texto da placa detectada
5. **Validação**: Verifica formato da placa (Mercosul/Antiga)
6. **Consulta**: Verifica se placa está na lista de irregulares
7. **Resposta**: Retorna resultado completo para frontend

## 📂 Estrutura do Projeto

```
PlateDetectionForStolenVehicles/
├── backend/                          # API e IA
│   ├── app.py                       # Servidor Flask principal
│   ├── detector_placas.py           # Lógica de detecção de placas
│   ├── requirements.txt             # Dependências Python
│   ├── modelos/                     # Modelos de IA treinados
│   │   ├── yolo.pt                 # Modelo YOLOv8
│   │   └── faster.pt               # Modelo Faster R-CNN
│   └── uploads/                     # Pasta temporária para uploads
├── src/                             # Frontend React
│   ├── components/                  # Componentes React
│   │   ├── PlateDetectionApp.js    # Componente principal
│   │   ├── ImageUpload.js          # Upload de imagens
│   │   ├── ImagePreview.js         # Preview das imagens
│   │   ├── ProcessingStatus.js     # Status de processamento
│   │   ├── Results.js              # Exibição dos resultados
│   │   └── *.css                   # Estilos dos componentes
│   ├── services/                   # Serviços de comunicação
│   │   ├── localService.js         # Serviço para API local
│   │   └── mockService.js          # Dados de teste
│   ├── config/                     # Configurações
│   │   └── config.js               # Configurações da aplicação
│   ├── App.js                      # Componente raiz
│   └── index.js                    # Ponto de entrada
├── public/                         # Arquivos públicos
├── package.json                    # Dependências Node.js
└── README.md                       # Documentação
```

## 🔧 API Endpoints

### `POST /upload`
Processa imagem e detecta placas.

**Request:**
- `Content-Type: multipart/form-data`
- `file`: Arquivo de imagem (PNG, JPG, JPEG, GIF)

**Response (Sucesso):**
```json
{
  "detectado": true,
  "placa": "ABC1D23",
  "confianca": 0.9524,
  "score_final": 0.8876,
  "situacao": "REGULAR",
  "detalhes_situacao": "Documentação em ordem",
  "tipo_placa": "MERCOSUL",
  "tempo_processamento": 2.34,
  "total_placas_detectadas": 1
}
```

**Response (Erro):**
```json
{
  "erro": "Nenhuma placa detectada na imagem",
  "detectado": false
}
```

### `GET /health`
Verifica status da API e modelos.

**Response:**
```json
{
  "status": "online",
  "modelos_carregados": true
}
```

## ⚙️ Configurações

### Lista de Placas Irregulares
Edite a lista `PLACAS_IRREGULARES` em `backend/app.py`:

```python
PLACAS_IRREGULARES = [
    "IVZ9A33", "XYZ9W87", "DEF2E34", 
    "OIS0410", "EUZ01J5", "MNO5H67"
    # Adicione mais placas conforme necessário
]
```

### Configurações do Frontend
Arquivo `src/config/config.js`:

```javascript
export const CONFIG = {
  api: {
    baseURL: 'http://localhost:5000',
    timeout: 30000
  },
  upload: {
    maxSize: 10485760,  // 10MB
    allowedTypes: ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
  }
};
```

## 🧪 Testando o Sistema

### Teste de Saúde da API
```bash
curl http://localhost:5000/health
```

### Teste de Upload via cURL
```bash
curl -X POST \
  -F "file=@caminho/para/imagem.jpg" \
  http://localhost:5000/upload
```

### Imagens de Teste
- Use imagens com placas visíveis e bem iluminadas
- Resolução mínima recomendada: 640x480
- Formatos aceitos: PNG, JPG, JPEG, GIF

## 🔍 Detecção de Problemas

### Backend não inicia
- Verifique se Python 3.8+ está instalado
- Confirme instalação das dependências: `pip install -r requirements.txt`
- Verifique se os modelos estão na pasta `backend/modelos/`

### Frontend não conecta com Backend
- Confirme que backend está rodando na porta 5000
- Verifique configuração de CORS no Flask
- Teste endpoint de saúde: `http://localhost:5000/health`

### Baixa precisão na detecção
- Use imagens com boa qualidade e iluminação
- Certifique-se que a placa está visível na imagem
- Verifique se os modelos foram treinados adequadamente

## 🚀 Deploy em Produção

### Backend (Docker - Recomendado)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
EXPOSE 5000

CMD ["python", "app.py"]
```

### Frontend (Build para Produção)
```bash
npm run build
# Deploy pasta 'build' em servidor web (Nginx, Apache, etc.)
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob licença MIT. Consulte `LICENSE` para detalhes.

## 🆘 Suporte

Para dúvidas ou problemas:

1. Verifique os logs do backend no terminal
2. Teste a API com curl ou Postman
3. Confirme que os modelos estão carregados corretamente
4. Verifique a documentação dos erros mais comuns acima
5. Abra uma issue no GitHub com detalhes do erro

## 👥 Equipe

- **Desenvolvedor Principal**: Arnald Souza
- **Orientação Acadêmica**: [Nome do Orientador]
- **Instituição**: [Nome da Faculdade]

## 📞 Contato

Para dúvidas técnicas ou acadêmicas, entre em contato através:
- GitHub Issues: Para bugs e melhorias
- Email: [seu-email@exemplo.com]