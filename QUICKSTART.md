# 🚀 Início Rápido

## Instalação (Ubuntu/Debian)

```bash
# 1. Instalar dependências do sistema
sudo apt update
sudo apt install python3-venv cmake build-essential

# 2. Criar ambiente virtual
python3 -m venv venv

# 3. Ativar ambiente virtual
source venv/bin/activate

# 4. Instalar dependências Python (pode levar alguns minutos)
pip install -r requirements.txt
```

## Executar o Sistema

### Opção 1: Script automático
```bash
./run.sh
```

### Opção 2: Manual
```bash
source venv/bin/activate
python main.py
```

## Uso Básico

1. **Cadastrar pessoa**: Menu → Opção 1
   - Digite o nome
   - Posicione o rosto na câmera
   - Pressione ESPAÇO para capturar

2. **Reconhecer em tempo real**: Menu → Opção 4
   - A câmera abrirá automaticamente
   - Rostos conhecidos aparecem em verde
   - Pressione Q ou ESC para sair

## Desativar Ambiente Virtual

```bash
deactivate
```

## Solução de Problemas

### Erro: "CMake is not installed"
```bash
sudo apt install cmake
```

### Erro: "externally-managed-environment"
Use sempre o ambiente virtual (`source venv/bin/activate`)

### Câmera não funciona
Verifique permissões e se a câmera está sendo usada por outro programa
