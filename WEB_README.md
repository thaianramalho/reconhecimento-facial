# 🌐 Interface Web - Reconhecimento Facial

Sistema web completo para reconhecimento facial com acesso à câmera do navegador.

## 📁 Estrutura Web

```
web/
├── index.php              # Página inicial
├── cadastro.php          # Cadastro de rostos via webcam
├── reconhecimento.php    # Reconhecimento em tempo real
├── lista.php             # Lista de pessoas cadastradas
├── api.php               # API REST para processamento
├── config.php            # Configurações
├── header.php            # Cabeçalho comum
├── footer.php            # Rodapé comum
├── css/
│   └── style.css         # Estilos da aplicação
├── js/
│   ├── cadastro.js       # Scripts de cadastro
│   └── reconhecimento.js # Scripts de reconhecimento
├── uploads/              # Uploads temporários
└── temp/                 # Arquivos temporários

web_api.py                # API Python para processamento facial
```

## 🚀 Como Executar

### Opção 1: Servidor PHP Embutido (Desenvolvimento)

```bash
cd web
php -S localhost:8000
```

Acesse: http://localhost:8000

### Opção 2: Apache/Nginx

1. **Configure o DocumentRoot para a pasta `web/`**

2. **Apache - Criar VirtualHost:**
```apache
<VirtualHost *:80>
    ServerName reconhecimento-facial.local
    DocumentRoot /caminho/para/reconhecimento-facial/web
    
    <Directory /caminho/para/reconhecimento-facial/web>
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

3. **Nginx - Configuração:**
```nginx
server {
    listen 80;
    server_name reconhecimento-facial.local;
    root /caminho/para/reconhecimento-facial/web;
    index index.php;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php-fpm.sock;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }
}
```

## 📋 Funcionalidades Web

### 🏠 Página Inicial
- Dashboard com visão geral do sistema
- Acesso rápido às funcionalidades
- Instruções de uso

### 📝 Cadastro
- Acesso à webcam do navegador
- Captura de foto em alta qualidade
- Processamento e validação em tempo real
- Feedback visual do cadastro

### 👁️ Reconhecimento
- Identificação em tempo real (atualização a cada 2 segundos)
- Retângulos visuais nos rostos detectados
- Exibição de nome e confiança
- Diferenciação visual (verde: conhecido, vermelho: desconhecido)

### 📋 Lista
- Visualização de todas as pessoas cadastradas
- Miniaturas das fotos
- Opção de remover cadastros

## 🔧 Requisitos

### Servidor
- PHP 7.4 ou superior
- Acesso a `shell_exec()` ou `exec()`
- Permissões de escrita em `uploads/` e `temp/`

### Python
- Ambiente virtual configurado em `venv/`
- Todas as dependências instaladas ([requirements.txt](requirements.txt))

### Navegador
- Suporte a getUserMedia API (Chrome, Firefox, Edge, Safari)
- HTTPS ou localhost (obrigatório para acesso à webcam)
- JavaScript habilitado

## 🔐 Segurança

### Importante para Produção

1. **HTTPS Obrigatório**
   - Navegadores exigem HTTPS para acessar webcam (exceto localhost)
   - Configure certificado SSL

2. **Validações**
   - Sanitização de nomes de arquivos
   - Validação de tipos de imagem
   - Limite de tamanho de uploads

3. **Permissões**
   ```bash
   chmod 755 web/
   chmod 777 web/uploads/ web/temp/
   ```

4. **`.htaccess` (Apache)**
   ```apache
   # Bloquear acesso direto a arquivos Python
   <Files "*.py">
       Order Allow,Deny
       Deny from all
   </Files>
   ```

## 🎨 Personalização

### Cores e Estilos
Edite [web/css/style.css](web/css/style.css) para customizar:
- Cores primárias e secundárias
- Layout e espaçamentos
- Animações e transições

### Tolerância do Reconhecimento
Em [web/js/reconhecimento.js](web/js/reconhecimento.js), ajuste o intervalo de reconhecimento:
```javascript
// Linha ~60
recognitionInterval = setInterval(recognizeFrame, 2000); // 2 segundos
```

Em [web_api.py](web_api.py), ajuste a tolerância padrão (0.6):
```python
# Linha ~200
tolerancia = float(sys.argv[3]) if len(sys.argv) > 3 else 0.6
```

## 🐛 Solução de Problemas

### Erro: "Permission denied" ao executar Python
```bash
chmod +x web_api.py
```

### Erro: Câmera não funciona
- Verifique se está usando HTTPS ou localhost
- Permita acesso à câmera no navegador
- Verifique se outra aba/aplicação não está usando a câmera

### Erro: "shell_exec() has been disabled"
- Verifique php.ini e remova `shell_exec` de `disable_functions`
- Reinicie o servidor web

### Imagens não aparecem na lista
- Verifique permissões da pasta `rostos_cadastrados/`
- Confirme que o caminho está correto em [lista.php](web/lista.php)

## 📱 Compatibilidade Mobile

O sistema é responsivo e funciona em dispositivos móveis:
- Tablets: Experiência completa
- Smartphones: Interface adaptada
- Orientação: Portrait e Landscape

## 🔄 Integração com Sistema CLI

A versão web compartilha os mesmos dados do sistema CLI:
- Mesmos arquivos de encoding ([dados/encodings.pkl](dados/encodings.pkl))
- Mesmas fotos ([rostos_cadastrados/](rostos_cadastrados/))
- Interoperabilidade total

## 📊 Monitoramento

Para debug, ative logs do PHP:
```php
// Em config.php
ini_set('display_errors', 1);
error_reporting(E_ALL);
```

## 🚀 Deploy em Produção

1. **Configure HTTPS**
2. **Desative debug** (remova display_errors)
3. **Configure backup** dos dados
4. **Monitore performance** (reconhecimento consome CPU)
5. **Limite taxa de requisições** para evitar sobrecarga

---

**Desenvolvido com PHP, JavaScript e Python** 🎯
