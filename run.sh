#!/bin/bash
# Script de inicialização do Sistema de Reconhecimento Facial

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "Execute primeiro: python3 -m venv venv"
    echo "Depois instale as dependências: source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Ativar ambiente virtual e executar o sistema
source venv/bin/activate
python main.py
