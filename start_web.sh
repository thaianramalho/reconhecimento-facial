#!/bin/bash
# Script para iniciar o servidor web

echo "🌐 Iniciando Servidor Web de Reconhecimento Facial"
echo "=================================================="
echo ""

# Verificar se está no diretório correto
if [ ! -f "web_api.py" ]; then
    echo "❌ Erro: Execute este script do diretório raiz do projeto"
    exit 1
fi

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Erro: Ambiente virtual não encontrado"
    echo "   Execute: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Verificar se o PHP está instalado
if ! command -v php &> /dev/null; then
    echo "❌ Erro: PHP não está instalado"
    echo "   Instale com: sudo apt install php"
    exit 1
fi

# Encontrar porta disponível (método mais confiável)
PORT=8000
while netstat -tuln 2>/dev/null | grep -q ":$PORT " || ss -tuln 2>/dev/null | grep -q ":$PORT "; do
    PORT=$((PORT + 1))
    if [ $PORT -gt 8100 ]; then
        echo "❌ Erro: Nenhuma porta disponível encontrada entre 8000 e 8100"
        exit 1
    fi
done

echo "✅ Ambiente virtual: OK"
echo "✅ PHP instalado: $(php -v | head -n 1)"
echo "✅ Porta disponível: $PORT"
echo ""
echo "🚀 Iniciando servidor em http://localhost:$PORT"
echo ""
echo "📋 Instruções:"
echo "   - Acesse http://localhost:$PORT no navegador"
echo "   - Permita o acesso à webcam quando solicitado"
echo "   - Pressione Ctrl+C para parar o servidor"
echo ""
echo "=================================================="
echo ""

cd web
php -S localhost:$PORT
