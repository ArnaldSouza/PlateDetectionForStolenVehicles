from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import cv2
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
    "OIS0410", "EUZ01J5", "MNO5H67"
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
            
            # Pegar a primeira placa detectada (mais confiável)
            placa_detectada = resultado_deteccao['placas'][0]
            
            # Verificar situação da placa
            situacao, detalhes = verificar_situacao_placa(placa_detectada['texto'])
            
            # Montar resposta
            resultado = {
                'detectado': True,
                'placa': placa_detectada['texto'],
                'confianca': round(placa_detectada['confianca'], 4),
                'score_final': round(placa_detectada['score_final'], 4),
                'situacao': situacao,
                'detalhes_situacao': detalhes,
                'tipo_placa': 'MERCOSUL' if placa_detectada['eh_mercosul'] else 'ANTIGO',
                'tempo_processamento': round(resultado_deteccao['tempo_processamento'], 2),
                'total_placas_detectadas': resultado_deteccao['total_placas']
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