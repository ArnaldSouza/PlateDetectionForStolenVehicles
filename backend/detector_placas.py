import cv2
import numpy as np
import matplotlib.pyplot as plt
import easyocr
import re
import torch
import torchvision
import torchvision.transforms as transforms
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from ultralytics import YOLO
import time
import base64

# Adicionar função para converter imagem para base64
def imagem_para_base64(imagem):
    """Converte imagem OpenCV para string base64"""
    _, buffer = cv2.imencode('.jpg', imagem)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{img_base64}"

# Inicializar EasyOCR
reader = easyocr.Reader(['pt', 'en'], gpu=True)

# Carregar modelos
def carregar_modelos():
    model_yolo = None
    model_faster = None
    
    # Carregar YOLOv8
    try:
        model_yolo = YOLO('./modelos/yolo.pt')
        print("✅ YOLO carregado")
    except Exception as e:
        print(f"❌ Erro YOLOv8: {e}")
    
    # Carregar Faster R-CNN
    try:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        try:
            model_faster = torch.load('./modelos/faster.pt', map_location=device)
            if not hasattr(model_faster, 'eval'):
                model_faster_temp = fasterrcnn_resnet50_fpn(weights=None, num_classes=2)
                model_faster_temp.load_state_dict(model_faster)
                model_faster = model_faster_temp.to(device)
            model_faster.eval()
        except:
            checkpoint = torch.load('./modelos/faster.pt', map_location=device)
            model_faster = fasterrcnn_resnet50_fpn(weights=None, num_classes=2)
            
            if 'state_dict' in checkpoint:
                model_faster.load_state_dict(checkpoint['state_dict'])
            elif 'model_state_dict' in checkpoint:
                model_faster.load_state_dict(checkpoint['model_state_dict'])
            else:
                model_faster.load_state_dict(checkpoint)
                
            model_faster = model_faster.to(device)
            model_faster.eval()
        
        print("✅ Faster R-CNN carregado")
    except Exception as e:
        print(f"❌ Erro Faster R-CNN: {e}")
    
    return model_yolo, model_faster

# Detectar placas com fallback
def detectar_placas(imagem, model_yolo, model_faster):
    placas = []
    
    # Tentar YOLO primeiro
    if model_yolo is not None:
        resultados = model_yolo(imagem, conf=0.4, verbose=False)
        
        for r in resultados:
            if r.boxes is not None:
                for box in r.boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                    confianca = float(box.conf[0])
                    if confianca > 0.4:
                        placas.append((x1, y1, x2, y2, confianca))
        
        # Verificar confiança >= 80%
        placas_alta_confianca = [p for p in placas if p[4] >= 0.8]
        
        if placas_alta_confianca:
            placas = placas_alta_confianca
        else:
            placas = []  # Limpar para fallback
    
    
    # Fallback para Faster R-CNN
    if not placas and model_faster is not None:
        try:
            if isinstance(imagem, str):
                img = cv2.imread(imagem)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            else:
                img = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
            
            transform = transforms.Compose([
                transforms.ToPILImage(),
                transforms.ToTensor(),
            ])
            
            img_tensor = transform(img).unsqueeze(0)
            device = next(model_faster.parameters()).device
            img_tensor = img_tensor.to(device)
            
            with torch.no_grad():
                predictions = model_faster(img_tensor)
            
            if len(predictions) > 0:
                boxes = predictions[0]['boxes'].cpu().numpy()
                scores = predictions[0]['scores'].cpu().numpy()
                valid_indices = scores > 0.4
                
                for box, score in zip(boxes[valid_indices], scores[valid_indices]):
                    x1, y1, x2, y2 = box.astype(int)
                    placas.append((x1, y1, x2, y2, float(score)))
        except:
            pass
    
    placas.sort(key=lambda x: x[4], reverse=True)
    return placas

# Verificar se é placa Mercosul
def verificar_placa_mercosul(placa_crop):
    hsv = cv2.cvtColor(placa_crop, cv2.COLOR_BGR2HSV)
    
    azul_baixo1 = np.array([100, 60, 70])
    azul_alto1 = np.array([125, 255, 255])
    azul_baixo2 = np.array([110, 80, 60])
    azul_alto2 = np.array([130, 255, 255])
    
    mascara_azul1 = cv2.inRange(hsv, azul_baixo1, azul_alto1)
    mascara_azul2 = cv2.inRange(hsv, azul_baixo2, azul_alto2)
    mascara_azul = cv2.bitwise_or(mascara_azul1, mascara_azul2)
    
    kernel = np.ones((2, 2), np.uint8)
    mascara_azul = cv2.morphologyEx(mascara_azul, cv2.MORPH_OPEN, kernel)
    mascara_azul = cv2.morphologyEx(mascara_azul, cv2.MORPH_CLOSE, kernel)
    
    pixels_azuis = cv2.countNonZero(mascara_azul)
    total_pixels = placa_crop.shape[0] * placa_crop.shape[1]
    porcentagem_azul = (pixels_azuis / total_pixels) * 100
    
    eh_mercosul = False
    if porcentagem_azul > 8.0:
        eh_mercosul = True
    elif porcentagem_azul >= 5.0:
        contornos, _ = cv2.findContours(mascara_azul, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contornos) > 0:
            maior_contorno = max(contornos, key=cv2.contourArea)
            area_maior_azul = cv2.contourArea(maior_contorno)
            concentracao_azul = (area_maior_azul / pixels_azuis) if pixels_azuis > 0 else 0
            if concentracao_azul > 0.7:
                eh_mercosul = True
    
    return {
        'eh_mercosul': eh_mercosul,
        'porcentagem_azul': porcentagem_azul
    }

# Melhorar nitidez da placa
def melhorar_nitidez_placa(placa_crop):
    if len(placa_crop.shape) == 3:
        cinza = cv2.cvtColor(placa_crop, cv2.COLOR_BGR2HSV)
        cinza = cinza[:, :, 2]
    else:
        cinza = placa_crop.copy()
    
    # Normalização de iluminação
    background = cv2.GaussianBlur(cinza, (51, 51), 0)
    background = np.where(background == 0, 1, background)
    cinza = cv2.divide(cinza, background, scale=255)
    
    # Filtro bilateral
    cinza = cv2.bilateralFilter(cinza, 5, 50, 50)
    
    # Redimensionamento
    h, w = cinza.shape
    if h < 64:
        fator = 80 / h
        nova_w, nova_h = int(w * fator), int(h * fator)
        cinza = cv2.resize(cinza, (nova_w, nova_h), interpolation=cv2.INTER_CUBIC)
    elif h > 120:
        fator = 90 / h
        nova_w, nova_h = int(w * fator), int(h * fator)
        cinza = cv2.resize(cinza, (nova_w, nova_h), interpolation=cv2.INTER_AREA)
    
    # Aguçamento
    kernel_suave = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
    aguçada = cv2.filter2D(cinza, -1, kernel_suave)
    aguçada = np.clip(aguçada, 0, 255).astype(np.uint8)
    
    # Equalização adaptativa
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 2))
    equalizada = clahe.apply(aguçada)
    
    # Unsharp masking
    gaussian = cv2.GaussianBlur(equalizada, (3, 3), 1.0)
    unsharp = cv2.addWeighted(equalizada, 1.8, gaussian, -0.8, 0)
    unsharp = np.clip(unsharp, 0, 255).astype(np.uint8)
    
    return unsharp

# Validar formato da placa
def validar_formato_placa(texto, eh_mercosul=False):
    texto = texto.upper().strip()
    
    if eh_mercosul:
        padrao_mercosul = re.match(r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$', texto)
        if padrao_mercosul:
            return {'valido': True, 'score': 1.0, 'tipo': 'mercosul_brasileiro'}
        elif len(texto) == 7:
            letras_pos_corretas = sum(1 for i in [0, 1, 2, 4] if i < len(texto) and texto[i].isalpha())
            nums_pos_corretas = sum(1 for i in [3, 5, 6] if i < len(texto) and texto[i].isdigit())
            score = (letras_pos_corretas + nums_pos_corretas) / 7.0
            if score >= 0.7:
                return {'valido': True, 'score': score, 'tipo': 'similar_mercosul'}
    else:
        padrao_antigo = re.match(r'^[A-Z]{3}[0-9]{4}$', texto)
        if padrao_antigo:
            return {'valido': True, 'score': 1.0, 'tipo': 'brasileiro_antigo'}
        elif len(texto) == 7:
            letras_corretas = sum(1 for i in [0, 1, 2] if i < len(texto) and texto[i].isalpha())
            numeros_corretos = sum(1 for i in [3, 4, 5, 6] if i < len(texto) and texto[i].isdigit())
            score = (letras_corretas + numeros_corretos) / 7.0
            if score >= 0.7:
                return {'valido': True, 'score': score, 'tipo': 'similar_antigo'}
    
    return {'valido': False, 'score': 0.0, 'tipo': 'invalido'}



# Corrigir caracteres confusos
def corrigir_caracteres_confusos(texto, eh_mercosul=False):
    texto = texto.upper().strip()
    
    correcoes = {
        '0': ['O', 'D', 'Q', '6'], '1': ['I', 'L', 'T'], '2': ['Z'],
        '3': ['8','B'], '5': ['S'], '6': ['G','0'], '8': ['B','3'], 
        'O': ['0'], 'I': ['1'], 'L': ['1'], 'S': ['5'], 'Z': ['2'], 
        'B': ['8','3'], 'G': ['6'], 'D': ['0'], 'Q': ['0'], 'T': ['1']
    }
    
    texto_corrigido = list(texto)
    
    if len(texto) == 7:
        if eh_mercosul:
            posicoes_letras = [0, 1, 2, 4]
            posicoes_numeros = [3, 5, 6]
        else:
            posicoes_letras = [0, 1, 2]
            posicoes_numeros = [3, 4, 5, 6]
        
        for i, char in enumerate(texto_corrigido):
            if i in posicoes_letras and char.isdigit():
                for letra, nums in correcoes.items():
                    if char in nums and letra.isalpha():
                        texto_corrigido[i] = letra
                        break
            elif i in posicoes_numeros and char.isalpha():
                if char in correcoes:
                    possiveis = [c for c in correcoes[char] if c.isdigit()]
                    if possiveis:
                        texto_corrigido[i] = possiveis[0]
    
    return ''.join(texto_corrigido)

# Aplicar OCR com múltiplas configurações
def aplicar_ocr_completo(imagem, reader):
    resultados_todos = []
    
    # Configuração padrão
    try:
        res1 = reader.readtext(imagem, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                              paragraph=False, width_ths=0.7, height_ths=0.7)
        for bbox, texto, conf in res1:
            resultados_todos.append({'texto': texto.upper(), 'confianca': conf, 'bbox': bbox})
    except:
        pass
    
    # Configuração sensível
    try:
        res2 = reader.readtext(imagem, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                              paragraph=False, width_ths=0.4, height_ths=0.4, detail=1)
        for bbox, texto, conf in res2:
            resultados_todos.append({'texto': texto.upper(), 'confianca': conf, 'bbox': bbox})
    except:
        pass
    
    return resultados_todos

# Criar versões da imagem para OCR
def criar_versoes_ocr(imagem_nitida):
    versoes_ocr = {'nitida': imagem_nitida}
    
    # Threshold automático
    _, otsu = cv2.threshold(imagem_nitida, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    versoes_ocr['otsu'] = otsu
    
    # Threshold adaptativo
    adaptativo = cv2.adaptiveThreshold(imagem_nitida, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 3)
    versoes_ocr['adaptativo'] = adaptativo
    
    # Versão invertida
    versoes_ocr['invertido'] = 255 - otsu
    
    return versoes_ocr

# Processar OCR completo
def processar_ocr_completo(placa_crop, reader, eh_mercosul=False):
    placa_nitida = melhorar_nitidez_placa(placa_crop)
    versoes_ocr = criar_versoes_ocr(placa_nitida)
    todos_resultados = []
    
    for nome_versao, imagem in versoes_ocr.items():
        resultados_ocr = aplicar_ocr_completo(imagem, reader)
        
        for resultado in resultados_ocr:
            texto_original = resultado['texto']
            texto_limpo = re.sub(r'[^A-Z0-9]', '', texto_original)
            
            if len(texto_limpo) >= 6:
                texto_corrigido = corrigir_caracteres_confusos(texto_limpo, eh_mercosul)
                validacao = validar_formato_placa(texto_corrigido, eh_mercosul)
                score_final = resultado['confianca'] * 0.6 + validacao['score'] * 0.4
                
                if (eh_mercosul and 'mercosul' in validacao['tipo']) or (not eh_mercosul and 'antigo' in validacao['tipo']):
                    score_final += 0.1
                
                resultado_completo = {
                    'texto_final': texto_corrigido,
                    'foi_corrigido': texto_corrigido != texto_limpo,
                    'confianca_ocr': resultado['confianca'],
                    'score_final': max(0, min(1, score_final)),
                    'validacao': validacao
                }
                
                todos_resultados.append(resultado_completo)
    
    todos_resultados.sort(key=lambda x: x['score_final'], reverse=True)
    return todos_resultados

# Modificar a função processar_placas para incluir os crops nos resultados
def processar_placas(imagem_path, modelo_yolo=None, modelo_faster=None):
    inicio = time.time()
    
    # Carregar imagem
    img = cv2.imread(imagem_path)
    if img is None:
        print(f"❌ Erro ao carregar: {imagem_path}")
        return None
    
    # Detectar placas
    placas = detectar_placas(img, modelo_yolo, modelo_faster)
    if not placas:
        print("❌ Nenhuma placa detectada")
        return None
    
    print(f"🔍 {len(placas)} placa(s) detectada(s)")
    
    # Processar todas as placas
    resultados_placas = []
    
    for i, (x1, y1, x2, y2, conf_det) in enumerate(placas):
        # Crop da placa com padding
        padding = 5
        placa_crop = img[max(0, y1-padding):min(img.shape[0], y2+padding), 
                        max(0, x1-padding):min(img.shape[1], x2+padding)]
        
        if placa_crop.size == 0:
            continue
        
        # Verificar tipo da placa
        resultado_mercosul = verificar_placa_mercosul(placa_crop)
        eh_mercosul = resultado_mercosul['eh_mercosul']
        
        # Processar OCR
        ocr_resultados = processar_ocr_completo(placa_crop, reader, eh_mercosul)
        
        if not ocr_resultados:
            continue
        
        melhor_ocr = ocr_resultados[0]
        score_final = melhor_ocr['score_final'] * 0.8 + conf_det * 0.2
        
        resultado_placa = {
            'placa_id': i+1,
            'texto': melhor_ocr['texto_final'],
            'confianca': melhor_ocr['confianca_ocr'],
            'score_final': score_final,
            'eh_mercosul': eh_mercosul,
            'coordenadas': (x1, y1, x2, y2),
            'crop': placa_crop  # Mantém o crop na estrutura de dados
        }
        
        resultados_placas.append(resultado_placa)
        
        tipo = "Mercosul" if eh_mercosul else "Antigo"
        print(f"✅ Placa {i+1} ({tipo}): '{melhor_ocr['texto_final']}' (score: {score_final:.3f})")
    
    tempo_total = time.time() - inicio
    
    return {
        'total_placas': len(resultados_placas),
        'placas': resultados_placas,
        'tempo_processamento': tempo_total,
        'imagem_original': img  # Adicionar imagem original aos resultados
    }

# Visualizar resultados
def visualizar_resultados(resultado, imagem_path):
    if not resultado:
        print("❌ Nenhum resultado para mostrar")
        return
    
    img = cv2.imread(imagem_path)
    img_visualizacao = img.copy()
    
    # Desenhar detecções
    for placa in resultado['placas']:
        x1, y1, x2, y2 = placa['coordenadas']
        
        cv2.rectangle(img_visualizacao, (x1, y1), (x2, y2), (0, 0, 255), 3)
        cv2.putText(img_visualizacao, f"Placa {placa['placa_id']} ({placa['score_final']:.2f})", 
                   (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Mostrar resultado
    # Mostrar imagem original com retângulos vermelhos
    plt.figure(figsize=(15, 10))
    
    # Subplot 1: Imagem original com retângulos
    plt.subplot(2, 1, 1)
    plt.imshow(cv2.cvtColor(img_visualizacao, cv2.COLOR_BGR2RGB))
    plt.title(f"Imagem Original - {resultado['total_placas']} Placa(s) Detectada(s)")
    plt.axis('off')
    
    # Subplot 2: Crops das placas
    plt.subplot(2, 1, 2)
    
    # Mostrar crops das placas
    num_placas = len(resultado['placas'])
    if num_placas > 0:
        # Criar uma imagem concatenada com todos os crops
        crops_concatenados = []
        for placa in resultado['placas']:
            crop = placa['crop']
            # Redimensionar crop para altura padrão
            altura_padrao = 100
            fator = altura_padrao / crop.shape[0]
            nova_largura = int(crop.shape[1] * fator)
            crop_redimensionado = cv2.resize(crop, (nova_largura, altura_padrao))
            
            # Adicionar texto no crop
            crop_com_texto = crop_redimensionado.copy()
            tipo = "MERCOSUL" if placa['eh_mercosul'] else "ANTIGO"
            cv2.putText(crop_com_texto, f"P{placa['placa_id']}: {placa['texto']}", 
                       (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(crop_com_texto, tipo, 
                       (5, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            
            crops_concatenados.append(crop_com_texto)
        
        # Concatenar horizontalmente
        if len(crops_concatenados) > 1:
            imagem_crops = np.hstack(crops_concatenados)
        else:
            imagem_crops = crops_concatenados[0]
        
        plt.imshow(cv2.cvtColor(imagem_crops, cv2.COLOR_BGR2RGB))
        plt.title("Crops das Placas Detectadas")
        plt.axis('off')
    
    plt.tight_layout()
    plt.show()

# Função principal de uso
def main(imagem_path):
    print("🚀 Iniciando detector de placas...")
    
    # Carregar modelos
    model_yolo, model_faster = carregar_modelos()
    
    # Processar placas
    resultado = processar_placas(imagem_path, model_yolo, model_faster)
    
    if resultado:
        print(f"\n⏱️ Processamento concluído em {resultado['tempo_processamento']:.2f}s")
        visualizar_resultados(resultado, imagem_path)
        return resultado
    else:
        return None

# Exemplo de uso
if __name__ == "__main__":
    # Exemplo de uso simples
    imagem = "3mais.png"  # Altere para sua imagem
    resultado = main(imagem)
    
    if resultado:
        print(f"\n📋 RESUMO:")
        for placa in resultado['placas']:
            tipo = "Mercosul" if placa['eh_mercosul'] else "Antigo"
            print(f"  Placa {placa['placa_id']}: {placa['texto']} ({tipo})")