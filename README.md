# Stolen Vehicle Plate Detection — Fullstack Application

Full-stack application for automatic license plate detection and stolen vehicle identification, built on top of the research published in our [Computer Engineering Final Project](https://github.com/ArnaldSouza/plate-detection-stolen-vehicles).

---

## Overview

The system runs a cascaded detection pipeline: YOLOv11 handles fast initial detection, Faster R-CNN refines low-confidence results, and EasyOCR extracts the plate characters. Results are cross-checked against a local database of flagged vehicles and returned to a React frontend in real time.

**Research results (from the academic paper):**

| Model | Precision | Recall | mAP@0.5 |
|---|---|---|---|
| YOLOv11-nano | 94.4% | 95.6% | 99.2% |
| Faster R-CNN (ResNet50-FPN) | 82.0% | 99.9% | 90.1% |
| Global pipeline accuracy | — | — | 86.0% |

Inference speed: ~41 fps on GPU (NVIDIA Tesla T4)

---

## Stack

**Backend** · Python · Flask · PyTorch · YOLOv11 · Faster R-CNN · EasyOCR · OpenCV

**Frontend** · React 18 · Axios · React Dropzone

---

## Pipeline

```
Image upload
    └── YOLOv11          → fast plate detection
        └── Faster R-CNN → refinement on low-confidence detections
            └── OpenCV   → preprocessing (grayscale, blur, threshold)
                └── EasyOCR → character extraction
                    └── DB lookup → REGULAR / IRREGULAR
```

---

## Getting started

### Requirements

- Python 3.8+
- Node.js 16+
- CUDA (optional, for GPU inference)
- Trained models in `backend/modelos/`: `yolo.pt` and `faster.pt`

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend

```bash
npm install
npm start
```

Open [http://localhost:3000](http://localhost:3000)

---

## API

### POST /upload

```json
{
  "detectado": true,
  "placa": "ABC1D23",
  "confianca": 0.95,
  "situacao": "IRREGULAR",
  "tipo_placa": "MERCOSUL",
  "tempo_processamento": 2.34
}
```

### GET /health

```json
{ "status": "online", "modelos_carregados": true }
```

---

## Project structure

```
PlateDetectionForStolenVehicles/
├── backend/
│   ├── app.py
│   ├── detector_placas.py
│   ├── requirements.txt
│   └── modelos/
│       ├── yolo.pt
│       └── faster.pt
├── src/
│   ├── components/
│   ├── services/
│   └── App.js
└── README.md
```

---

## Authors

- Arnald Souza · [LinkedIn](https://www.linkedin.com/in/arnaldsouza/) · [GitHub](https://github.com/ArnaldSouza)
- Bruno Gabriel de Oliveira Targa · [LinkedIn](https://www.linkedin.com/in/brunotarga/)
- Victor Soares Nunes Pires de Oliveira · [LinkedIn](https://www.linkedin.com/in/victorpioli/)

Advisor: Prof. Allan Marconato Marum · Centro Universitário Facens
