from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import cv2
import base64
from werkzeug.utils import secure_filename

# Importar as funções do detector de placas
from detector_placas import carregar_modelos, processar_placas

app = Flask(__name__)
CORS(app)

# Pasta onde as imagens serão salvas temporariamente
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Extensões permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Carregar modelos uma vez ao iniciar a aplicação
print("🚀 Carregando modelos de detecção...")
model_yolo, model_faster = carregar_modelos()
print("✅ Modelos carregados com sucesso!")

# Lista de placas irregulares (substitua por sua lista real)
PLACAS_IRREGULARES = [
    "IVZ9A33", "XYZ9W87", "DEF2E34", 
    "OIS0410", "EUZ01J5", "ECO3057"
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def verificar_situacao_placa(placa_texto):
    """Verifica se a placa está regular ou irregular"""
    placa_limpa = placa_texto.upper().strip()
    
    # Verificar se está na lista de irregulares
    if placa_limpa in PLACAS_IRREGULARES:
        return "IRREGULAR", "Apreenda o veículo !!!"
    else:
        return "REGULAR", "Documentação em ordem"

def crop_para_base64(crop_imagem):
    """Converte o crop da placa para base64"""
    try:
        if crop_imagem is not None and crop_imagem.size > 0:
            _, buffer = cv2.imencode('.jpg', crop_imagem)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            return f"data:image/jpeg;base64,{img_base64}"
        return None
    except Exception as e:
        print(f"Erro ao converter crop para base64: {e}")
        return None

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'erro': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'erro': 'Nenhum arquivo selecionado'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Processar a imagem com o detector de placas
            resultado_deteccao = processar_placas(filepath, model_yolo, model_faster)
            
            if not resultado_deteccao or resultado_deteccao['total_placas'] == 0:
                return jsonify({
                    'erro': 'Nenhuma placa detectada na imagem',
                    'detectado': False
                }), 400
            
            # Processar todas as placas detectadas
            placas_processadas = []
            
            for placa_detectada in resultado_deteccao['placas']:
                # Verificar situação da placa
                situacao_placa, detalhes_placa = verificar_situacao_placa(placa_detectada['texto'])
                
                # Converter crop da placa para base64
                crop_base64 = crop_para_base64(placa_detectada['crop'])
                
                # Converter coordenadas para tipos Python nativos (evitar int64)
                coordenadas = placa_detectada['coordenadas']
                coordenadas_serializable = (
                    int(coordenadas[0]), 
                    int(coordenadas[1]), 
                    int(coordenadas[2]), 
                    int(coordenadas[3])
                )
                
                placa_info = {
                    'id': placa_detectada['placa_id'],
                    'texto': placa_detectada['texto'],
                    'confianca': round(float(placa_detectada['confianca']), 4),
                    'score_final': round(float(placa_detectada['score_final']), 4),
                    'situacao': situacao_placa,
                    'detalhes_situacao': detalhes_placa,
                    'tipo_placa': 'MERCOSUL' if placa_detectada['eh_mercosul'] else 'ANTIGO',
                    'crop_placa': crop_base64,
                    'coordenadas': coordenadas_serializable,
                    'modelo_deteccao': placa_detectada['modelo_deteccao'],  # Adiciona o modelo usado
                    'confianca_deteccao': round(float(placa_detectada['confianca_deteccao']), 4)  # Adiciona confiança da detecção
                }
                
                placas_processadas.append(placa_info)
            
            # Pegar a primeira placa (mais confiável) para compatibilidade com frontend atual
            placa_principal = placas_processadas[0] if placas_processadas else None
            
            # Montar resposta
            resultado = {
                'detectado': True,
                'placa': placa_principal['texto'] if placa_principal else '',
                'confianca': placa_principal['confianca'] if placa_principal else 0,
                'score_final': placa_principal['score_final'] if placa_principal else 0,
                'situacao': placa_principal['situacao'] if placa_principal else 'REGULAR',
                'detalhes_situacao': placa_principal['detalhes_situacao'] if placa_principal else '',
                'tipo_placa': placa_principal['tipo_placa'] if placa_principal else 'ANTIGO',
                'tempo_processamento': round(float(resultado_deteccao['tempo_processamento']), 2),
                'total_placas_detectadas': int(resultado_deteccao['total_placas']),
                'crop_placa': placa_principal['crop_placa'] if placa_principal else None,
                'coordenadas_deteccao': placa_principal['coordenadas'] if placa_principal else None,
                'todas_placas': placas_processadas  # Nova informação com todas as placas
            }
            
            # Limpar arquivo temporário
            if os.path.exists(filepath):
                os.remove(filepath)
                
            return jsonify(resultado), 200
            
        except Exception as e:
            # Limpar arquivo temporário em caso de erro
            if os.path.exists(filepath):
                os.remove(filepath)
                
            return jsonify({
                'erro': f'Erro ao processar imagem: {str(e)}',
                'detectado': False
            }), 500
    
    return jsonify({'erro': 'Formato de arquivo não permitido'}), 400

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar se a API está funcionando"""
    return jsonify({
        'status': 'online',
        'modelos_carregados': model_yolo is not None or model_faster is not None
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)