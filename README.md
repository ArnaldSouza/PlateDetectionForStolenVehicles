# Sistema de Detecção de Placas Veiculares

Um sistema web desenvolvido em React para detectar placas veiculares em imagens e verificar se o veículo está regular ou irregular. O sistema funciona 100% localmente com simulação de detecção de placas.

## 🚀 Características

- **Upload de Imagens**: Interface drag-and-drop para upload de imagens
- **Detecção Simulada**: Processamento local com resultados simulados
- **Verificação de Status**: Identifica se o veículo é regular ou irregular
- **Interface Responsiva**: Design moderno e responsivo
- **Feedback Visual**: Indicadores de status e progresso em tempo real
- **100% Local**: Não depende de serviços externos

## 🛠️ Tecnologias Utilizadas

- **React 18** - Framework frontend
- **React Dropzone** - Upload de arquivos drag-and-drop
- **Styled Components** - Estilização
- **JavaScript ES6+** - Lógica de processamento local

## 📋 Pré-requisitos

- Node.js 16+ instalado

## 🔧 Instalação

1. **Clone o repositório ou navegue até a pasta do projeto:**
   ```bash
   cd frontend_tcc-1
   ```

2. **Instale as dependências:**
   ```bash
   npm install
   ```
   REACT_APP_AWS_SECRET_ACCESS_KEY=sua_secret_key
   REACT_APP_S3_BUCKET_NAME=seu-bucket-s3
   REACT_APP_LAMBDA_API_ENDPOINT=https://sua-api.amazonaws.com/detect-plate
   ```

4. **Inicie o servidor de desenvolvimento:**
   ```bash
   npm start
   ```

5. **Acesse a aplicação:**
   Abra [http://localhost:3000](http://localhost:3000) no seu navegador.

## 🏗️ Configuração AWS

3. **Execute o projeto:**
   ```bash
   npm start
   ```

4. **Acesse a aplicação:**
   ```
   http://localhost:3000
   ```

## 🎯 Como Usar

1. **Faça upload de uma imagem** de um veículo usando drag-and-drop ou clicando para selecionar
2. **Clique em "Analisar Imagem"** para iniciar o processamento
3. **Aguarde o processamento** (simulação de 3 segundos)
4. **Veja os resultados** com a placa detectada e status do veículo

## 📂 Estrutura do Projeto

```
src/
├── components/
│   ├── PlateDetectionApp.js     # Componente principal
│   ├── ImageUpload.js           # Upload de imagens
│   ├── ImagePreview.js          # Preview das imagens
│   ├── ProcessingStatus.js      # Status de processamento
│   ├── Results.js               # Exibição dos resultados
│   └── *.css                    # Arquivos de estilo
├── services/
│   ├── localService.js          # Serviço de processamento local
│   └── mockService.js           # Dados simulados
├── config/
│   └── config.js                # Configurações da aplicação
└── App.js                       # Componente raiz
```

## 🔧 Configurações

As configurações estão centralizadas em `src/config/config.js`:

- **Upload Settings**: Tamanho máximo, tipos permitidos
- **Local Settings**: Tempo de simulação de processamento
- **Validation**: Regras de validação de arquivos

## 🎨 Simulação

O sistema simula a detecção de placas com:
- **Placas aleatórias**: ABC-1234, XYZ-5678, etc.
- **Status aleatório**: 70% chance de ser regular
- **Confiança**: Entre 80-100%
- **Delay realístico**: 3 segundos de processamento

## 📁 Estrutura do Projeto

```
src/
├── components/
│   ├── PlateDetectionApp.js    # Componente principal
│   ├── ImageUpload.js          # Componente de upload
│   ├── ImagePreview.js         # Prévia da imagem
│   ├── ProcessingStatus.js     # Status de processamento
│   ├── Results.js              # Exibição de resultados
│   └── *.css                   # Arquivos de estilo
├── services/
│   └── awsService.js           # Integração com AWS
├── App.js                      # Componente raiz
└── index.js                    # Ponto de entrada
```

## 🎨 Personalização

### Modificar Estilos

Os estilos estão organizados em arquivos CSS individuais para cada componente. Você pode personalizar:

- Cores do tema no arquivo CSS de cada componente
- Layout responsivo ajustando media queries
- Animações e transições

### Adicionar Funcionalidades

- **Histórico**: Adicione localStorage para manter histórico de análises
- **Múltiplas Imagens**: Modifique para processar várias imagens simultaneamente
- **Exportar Resultados**: Adicione funcionalidade para exportar relatórios

## 🔒 Segurança

- **Credenciais**: Nunca commite arquivos `.env` com credenciais reais
- **CORS**: Configure CORS adequadamente no S3
- **Validação**: O sistema valida tipo e tamanho dos arquivos
- **Timeout**: Configurado timeout de 30s para requisições

## 🚀 Deploy

### Build para Produção

```bash
npm run build
```

### Deploy em S3 (Hospedagem Estática)

```bash
# Fazer build
npm run build

# Fazer upload para S3
aws s3 sync build/ s3://seu-bucket-frontend --delete

# Configurar bucket para hospedagem estática
aws s3 website s3://seu-bucket-frontend --index-document index.html
```

## 🧪 Testes

```bash
# Executar testes
npm test

# Executar testes com coverage
npm test -- --coverage
```

## 📝 Scripts Disponíveis

- `npm start` - Inicia servidor de desenvolvimento
- `npm run build` - Cria build de produção
- `npm test` - Executa testes
- `npm run eject` - Ejeta configuração do Create React App

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Se encontrar problemas:

1. Verifique se todas as variáveis de ambiente estão configuradas
2. Confirme se as credenciais AWS estão corretas
3. Teste a conectividade com AWS
4. Verifique os logs do navegador para erros JavaScript
5. Confirme se a Lambda function está funcionando independentemente

## 📞 Contato

Para dúvidas ou sugestões, entre em contato através das issues do GitHub.