# 🎯 Guia Rápido - Sistema de Reconhecimento Facial

## 🌐 VERSÃO WEB (RECOMENDADO)

### Iniciar Servidor
```bash
./start_web.sh
```

### Acessar
Abra o navegador em: **http://localhost:8000**

### Funcionalidades
1. **Cadastro** - Tire foto com a webcam e cadastre pessoas
2. **Reconhecimento** - Identifique rostos em tempo real
3. **Lista** - Veja e gerencie pessoas cadastradas

---

## 🖥️ VERSÃO CLI (TERMINAL)

### Executar
```bash
source venv/bin/activate
python main.py
```

ou

```bash
./run.sh
```

---

## 📱 REQUISITOS DO NAVEGADOR

- ✅ Chrome, Firefox, Edge ou Safari
- ✅ Webcam conectada
- ✅ Permissão de acesso à câmera
- ✅ HTTPS ou localhost

---

## 🔧 COMANDOS ÚTEIS

### Instalar Dependências
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Testar API Python
```bash
source venv/bin/activate
python web_api.py listar
```

### Parar Servidor Web
Pressione `Ctrl+C` no terminal

---

## 📚 DOCUMENTAÇÃO

- **[README.md](README.md)** - Documentação completa do sistema
- **[WEB_README.md](WEB_README.md)** - Documentação da versão web
- **[QUICKSTART.md](QUICKSTART.md)** - Início rápido CLI

---

## 🎥 FLUXO DE USO WEB

1. Abra http://localhost:8000
2. Clique em "Cadastro"
3. Permita acesso à câmera
4. Clique em "Iniciar Câmera"
5. Clique em "Capturar Foto"
6. Digite o nome e clique em "Cadastrar"
7. Vá para "Reconhecimento"
8. Clique em "Iniciar Reconhecimento"
9. Rostos conhecidos aparecerão em verde!

---

## ⚠️ SOLUÇÃO DE PROBLEMAS

### Câmera não funciona na web
- Use HTTPS ou localhost
- Permita acesso no navegador
- Feche outras abas usando a câmera

### Erro ao processar imagem
- Verifique se o ambiente virtual está ativo
- Confirme que as dependências estão instaladas
- Veja permissões das pastas `web/uploads` e `web/temp`

### Porta em uso
```bash
# O script start_web.sh encontra automaticamente uma porta livre
./start_web.sh
```

---

**🚀 Projeto pronto para uso!**
