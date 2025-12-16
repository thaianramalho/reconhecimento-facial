# 👁️ Sistema de Reconhecimento Facial

Sistema completo de reconhecimento facial com cadastro de pessoas e identificação em tempo real usando Python, OpenCV e face_recognition.

**🌐 Agora com Interface Web!** Acesse via navegador com suporte à câmera. [Ver documentação web →](WEB_README.md)

## 📋 Funcionalidades

### 🖥️ Versão CLI (Terminal)
- Captura de rostos via webcam
- Reconhecimento em tempo real
- Reconhecimento em imagens estáticas
- Interface de texto interativa

### 🌐 Versão Web (Navegador)
- Interface moderna e responsiva
- Acesso à webcam do navegador
- Reconhecimento em tempo real na web
- Cadastro via interface gráfica
- Gerenciamento visual de pessoas
- **[Ver documentação completa →](WEB_README.md)**

### 📝 Cadastro
- Captura de rostos via webcam
- Armazenamento de encodings faciais
- Listagem de pessoas cadastradas
- Remoção de cadastros

### 👁️ Reconhecimento
- Detecção e identificação em tempo real
- Reconhecimento em imagens estáticas
- Exibição de confiança da identificação
- Contador de FPS
- Interface visual com retângulos e nomes

## 🚀 Instalação

### Pré-requisitos

1. **Python 3.7 ou superior**
2. **CMake** (necessário para compilar dlib)
3. **Webcam** conectada ao computador

### Instalação no Linux (Ubuntu/Debian)

```bash
# Instalar dependências do sistema
sudo apt update
sudo apt install python3-pip python3-venv cmake build-essential

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências Python
pip install -r requirements.txt
```

### Instalação no Linux (Fedora/RHEL)

```bash
# Instalar dependências do sistema
sudo dnf install python3-pip cmake gcc gcc-c++

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências Python
pip install -r requirements.txt
```

### Instalação no macOS

```bash
# Instalar Homebrew (se não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar dependências
brew install cmake

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências Python
pip install -r requirements.txt
```

### Instalação no Windows

1. Instale o [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Instale o [CMake](https://cmake.org/download/)
3. Crie e ative o ambiente virtual:

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (PowerShell)
venv\Scripts\Activate.ps1

# Ativar ambiente virtual (CMD)
venv\Scripts\activate.bat

# Instalar dependências
pip install -r requirements.txt
```

## 💻 Como Usar

### 🌐 Versão Web (Recomendado)

**Iniciar servidor web:**
```bash
./start_web.sh
```

Ou manualmente:
```bash
cd web
php -S localhost:8000
```

**Acesse no navegador:** http://localhost:8000

**Recursos da versão web:**
- ✅ Interface gráfica moderna
- ✅ Acesso à webcam do navegador  
- ✅ Reconhecimento em tempo real
- ✅ Gerenciamento visual
- ✅ Responsivo (funciona em tablets e smartphones)

📖 **[Documentação completa da versão web →](WEB_README.md)**

---

### 🖥️ Versão CLI (Terminal)

### Ativar o Ambiente Virtual

Sempre que for usar o sistema, primeiro ative o ambiente virtual:

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```bash
venv\Scripts\activate.bat
```

### Executar o Sistema

```bash
python main.py
```

### Menu Principal

O sistema possui um menu interativo com as seguintes opções:

#### 📝 CADASTRO
1. **Cadastrar nova pessoa** - Captura foto via webcam e salva o encoding facial
2. **Listar pessoas cadastradas** - Mostra todas as pessoas no banco de dados
3. **Remover cadastro** - Remove uma pessoa do sistema

#### 👁️ RECONHECIMENTO
4. **Iniciar reconhecimento em tempo real** - Usa a webcam para identificar rostos
5. **Reconhecer rostos em uma imagem** - Identifica rostos em uma foto

#### ⚙️ CONFIGURAÇÕES
6. **Recarregar dados de cadastro** - Atualiza o sistema com novos cadastros

## 📖 Guia de Uso

### 1. Cadastrar uma Pessoa

1. Ative o ambiente virtual (se ainda não ativou)
2. Execute o sistema: `python main.py`
3. Escolha a opção **1** (Cadastrar nova pessoa)
3. Digite o nome da pessoa
4. Posicione o rosto na frente da câmera
5. Pressione **ESPAÇO** para capturar a foto
6. O sistema processará e salvará o encoding facial

**Dicas:**
- Mantenha boa iluminação
- Olhe diretamente para a câmera
- Evite acessórios que cubram o rosto

### 2. Reconhecer Rostos em Tempo Real

1. Escolha a opção **4** (Iniciar reconhecimento em tempo real)
2. O sistema abrirá a câmera e começará a identificar rostos
3. Rostos conhecidos aparecerão com nome e percentual de confiança em **verde**
4. Rostos desconhecidos aparecerão em **vermelho**
5. Pressione **Q** ou **ESC** para sair

### 3. Reconhecer Rostos em Imagem

1. Escolha a opção **5** (Reconhecer rostos em uma imagem)
2. Digite o caminho completo da imagem
3. O sistema identificará todos os rostos na imagem
4. Pressione qualquer tecla para fechar a visualização

## 📁 Estrutura do Projeto

```
reconhecimento-facial/
│
├── main.py                  # Menu principal do sistema
├── cadastro.py             # Módulo de cadastro facial
├── reconhecimento.py       # Módulo de reconhecimento facial
├── requirements.txt        # Dependências do projeto
├── .gitignore             # Arquivos ignorados pelo git
│
├── venv/                   # Ambiente virtual Python (criado na instalação)
│
├── dados/                  # Dados do sistema
│   └── encodings.pkl      # Encodings faciais (criado automaticamente)
│
└── rostos_cadastrados/    # Fotos das pessoas cadastradas
    ├── pessoa1.jpg
    ├── pessoa2.jpg
    └── ...
```

## 🔧 Módulos Independentes

Cada módulo pode ser executado de forma independente:

### Módulo de Cadastro

```bash
source venv/bin/activate  # Ativar ambiente virtual primeiro
python cadastro.py
```

### Módulo de Reconhecimento

```bash
source venv/bin/activate  # Ativar ambiente virtual primeiro
python reconhecimento.py
```

## ⚙️ Configurações Avançadas

### Ajustar Tolerância do Reconhecimento

A tolerância padrão é `0.6`. Valores menores tornam o reconhecimento mais rigoroso:

- **0.4 a 0.5**: Muito rigoroso (menos falsos positivos)
- **0.6**: Padrão (equilibrado)
- **0.7 a 0.8**: Mais permissivo (mais falsos positivos)

Para ajustar, edite o arquivo [reconhecimento.py](reconhecimento.py) na função `iniciar_reconhecimento()`.

### Desabilitar FPS

Para ocultar o contador de FPS, defina `mostrar_fps=False` ao chamar `iniciar_reconhecimento()`.

## 🐛 Solução de Problemas

### Erro: "Câmera não encontrada"
- Verifique se a webcam está conectada
- Tente outro índice de câmera alterando `cv2.VideoCapture(0)` para `cv2.VideoCapture(1)` ou `cv2.VideoCapture(2)`

### Erro na instalação do face_recognition
- No Linux, instale: `sudo apt install cmake build-essential`
- No Windows, instale o Visual Studio Build Tools
- No macOS, instale: `brew install cmake`

### Reconhecimento impreciso
- Ajuste a tolerância (valores menores = mais preciso)
- Cadastre a pessoa em diferentes ângulos
- Melhore a iluminação

### Performance baixa
- O sistema já processa frames alternados para otimização
- Reduza a resolução da câmera se necessário
- Feche outros programas que usam a CPU

## 📦 Dependências

- **opencv-python**: Processamento de imagens e vídeo
- **face-recognition**: Detecção e reconhecimento facial
- **numpy**: Operações numéricas
- **Pillow**: Manipulação de imagens

## 📝 Licença

Este projeto é de código aberto e está disponível para uso pessoal e educacional.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

## 📧 Suporte

Se encontrar problemas ou tiver dúvidas:
1. Verifique a seção de Solução de Problemas
2. Leia a documentação das bibliotecas utilizadas
3. Abra uma issue no repositório

## 🎯 Próximas Funcionalidades

- [ ] Interface gráfica (GUI) com Tkinter ou PyQt
- [ ] Exportação de relatórios de reconhecimento
- [ ] Suporte a múltiplas câmeras
- [ ] Histórico de detecções
- [ ] API REST para integração
- [ ] Reconhecimento em vídeos
- [ ] Modo de treinamento aprimorado

---

**Desenvolvido com ❤️ usando Python, OpenCV e face_recognition**
