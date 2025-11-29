Aqui está a versão atualizada **com os novos desenvolvedores**, **links revisados** e **formatação aprimorada** em **Markdown**, mantendo estilo profissional, limpo e coerente.

---

# Sistema de Detecção de Placas para Veículos Roubados/Furtados

Um sistema completo de detecção automática de placas veiculares desenvolvido com inteligência artificial. O sistema utiliza modelos de deep learning (YOLOv8 e Faster R-CNN) para detectar placas em imagens e verificar automaticamente se o veículo está na lista de veículos irregulares.

---

## 🚀 Características Principais

* **Detecção Inteligente**: Uso de YOLOv8 e Faster R-CNN para alta precisão
* **OCR Avançado**: Reconhecimento de caracteres via EasyOCR (PT/EN)
* **Verificação Automática**: Consulta direta à base local de placas irregulares
* **Interface Web Moderna**: Frontend React com upload drag-and-drop
* **API RESTful**: Backend em Flask robusto e modular
* **Processamento Offline**: Totalmente funcional sem internet
* **Suporte a Diversos Formatos**: PNG, JPG, JPEG e GIF

---

## 🏗️ Arquitetura do Sistema

### **Frontend (React)**

* Interface responsiva
* Upload drag-and-drop
* Exibição dos resultados e status do processamento

### **Backend (Flask + IA)**

* Detecção de placas via IA
* OCR e validação das placas
* Verificação contra base de dados local
* Endpoints REST padronizados

### **Modelos Utilizados**

* **YOLOv8** — rapidez e precisão
* **Faster R-CNN** — fallback robusto
* **EasyOCR** — leitura de caracteres

---

## 🛠️ Tecnologias Utilizadas

### **Frontend**

* React 18
* React Dropzone
* Styled Components
* Axios

### **Backend**

* Flask
* PyTorch
* YOLOv8
* Faster R-CNN
* EasyOCR
* OpenCV
* Flask-CORS

---

## 📋 Pré-requisitos

* Node.js 16+
* Python 3.8+
* CUDA (opcional)
* Modelos treinados em `backend/modelos/`

---

## 🔧 Instalação e Configuração

### **1. Clonar Repositório**

```bash
git clone https://github.com/ArnaldSouza/PlateDetectionForStolenVehicles.git
cd PlateDetectionForStolenVehicles
```

### **2. Backend**

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# ou: source venv/bin/activate
pip install -r requirements.txt
```

Coloque os modelos em `backend/modelos/`:

* `yolo.pt`
* `faster.pt`

### **3. Frontend**

```bash
cd ../
npm install
```

### **4. Execução**

**Backend**

```bash
cd backend
python app.py
```

**Frontend**

```bash
npm start
```

---

## 🎯 Como Usar

1. Abra: **[http://localhost:3000](http://localhost:3000)**
2. Faça upload de uma imagem
3. Clique em **Analisar Imagem**
4. Veja:

   * Placa detectada
   * Confiança
   * Status (REGULAR/IRREGULAR)
   * Tipo de placa
   * Tempo total

---

## 📊 Fluxo de Processamento

1. Upload da imagem
2. Pré-processamento
3. Detecção (YOLOv8 → fallback Faster R-CNN)
4. OCR com EasyOCR
5. Validação e normalização
6. Verificação contra lista de irregulares
7. Retorno ao frontend

---

## 📂 Estrutura do Projeto

```
PlateDetectionForStolenVehicles/
├── backend/
│   ├── app.py
│   ├── detector_placas.py
│   ├── requirements.txt
│   ├── modelos/
│   │   ├── yolo.pt
│   │   └── faster.pt
│   └── uploads/
├── src/
│   ├── components/
│   ├── services/
│   ├── config/
│   ├── App.js
│   └── index.js
├── public/
├── package.json
└── README.md
```

---

## 🔧 API Endpoints

### **POST /upload**

Processa imagem enviada e retorna os dados detectados.

**Sucesso**

```json
{
  "detectado": true,
  "placa": "ABC1D23",
  "confianca": 0.9524,
  "situacao": "REGULAR",
  "tipo_placa": "MERCOSUL",
  "tempo_processamento": 2.34
}
```

**Erro**

```json
{
  "detectado": false,
  "erro": "Nenhuma placa detectada na imagem"
}
```

### **GET /health**

```json
{
  "status": "online",
  "modelos_carregados": true
}
```

---

## ⚙️ Configurações

### **Lista de Placas Irregulares**

`backend/app.py`:

```python
PLACAS_IRREGULARES = [
    "IVZ9A33", "XYZ9W87", "DEF2E34", 
    "OIS0410", "EUZ01J5", "MNO5H67"
]
```

### **Configurações do Frontend**

`src/config/config.js`:

```javascript
export const CONFIG = {
  api: { baseURL: 'http://localhost:5000', timeout: 30000 },
  upload: {
    maxSize: 10485760,
    allowedTypes: ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
  }
};
```

---

## 🧪 Testes

### Testar API

```bash
curl http://localhost:5000/health
```

### Enviar imagem

```bash
curl -X POST -F "file=@imagem.jpg" http://localhost:5000/upload
```

---

## 🤝 Contribuição

1. Faça um fork
2. Crie uma branch:

   ```bash
   git checkout -b feature/nova-funcionalidade
   ```
3. Commit
4. Push
5. Abra PR

---

## 📄 Licença

Licença **MIT** – consulte o arquivo `LICENSE`.

---

## 👥 Equipe

### **Desenvolvedores Principais**

* **Arnald Souza** — [LinkedIn](https://www.linkedin.com/in/arnaldsouza/)
* **Bruno Targa** — [LinkedIn](https://www.linkedin.com/in/brunotarga/)
* **Victor Nunes** — [LinkedIn](https://www.linkedin.com/in/victorpioli/)

### **Orientação Acadêmica**

* **Allan Marum** — [LinkedIn](https://www.linkedin.com/in/allanmarum/)

### **Instituição**

* **Centro Universitário Facens**

---

## 📞 Contato

* **Email:** [arnald.souza472@gmail.com](mailto:arnald.souza472@gmail.com)
* **GitHub Issues:** utilize para bugs ou sugestões
