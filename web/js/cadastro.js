// Cadastro de Rosto
let video = document.getElementById('video');
let canvas = document.getElementById('canvas');
let preview = document.getElementById('preview');
let previewImage = document.getElementById('preview-image');
let startCameraBtn = document.getElementById('startCamera');
let captureBtn = document.getElementById('capture');
let retakeBtn = document.getElementById('retake');
let cadastroForm = document.getElementById('cadastroForm');
let resultDiv = document.getElementById('result');

let stream = null;
let capturedImage = null;

// Verificar suporte do navegador
function checkBrowserSupport() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert('Seu navegador não suporta acesso à câmera.\n\nPor favor, use:\n- Chrome 53+\n- Firefox 36+\n- Safari 11+\n- Edge 12+\n\nOu verifique se está acessando via HTTPS ou localhost.');
        startCameraBtn.disabled = true;
        return false;
    }
    return true;
}

// Verificar suporte ao carregar a página
if (!checkBrowserSupport()) {
    resultDiv.innerHTML = '<strong>⚠️ Atenção!</strong><br>Seu navegador não suporta acesso à câmera ou a página não está sendo servida via HTTPS/localhost.';
    resultDiv.className = 'result-container error';
    resultDiv.style.display = 'block';
}

// Iniciar câmera
startCameraBtn.addEventListener('click', async () => {
    if (!checkBrowserSupport()) {
        return;
    }
    
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                width: { ideal: 1280 },
                height: { ideal: 720 }
            } 
        });
        
        video.srcObject = stream;
        video.style.display = 'block';
        preview.style.display = 'none';
        
        startCameraBtn.style.display = 'none';
        captureBtn.style.display = 'inline-block';
        
        resultDiv.innerHTML = '';
        resultDiv.className = 'result-container';
    } catch (error) {
        let errorMsg = 'Erro ao acessar a câmera: ' + error.message;
        
        if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
            errorMsg = 'Permissão negada! Por favor, permita o acesso à câmera nas configurações do navegador.';
        } else if (error.name === 'NotFoundError' || error.name === 'DevicesNotFoundError') {
            errorMsg = 'Nenhuma câmera encontrada! Verifique se há uma câmera conectada ao dispositivo.';
        } else if (error.name === 'NotReadableError' || error.name === 'TrackStartError') {
            errorMsg = 'Câmera em uso! Feche outros programas que possam estar usando a câmera.';
        }
        
        alert(errorMsg);
        resultDiv.innerHTML = '<strong>❌ Erro!</strong><br>' + errorMsg;
        resultDiv.className = 'result-container error';
        resultDiv.style.display = 'block';
    }
});

// Capturar foto
captureBtn.addEventListener('click', () => {
    // Reduzir resolução para evitar erro 413 (Payload Too Large)
    const maxWidth = 800;
    const maxHeight = 600;
    
    let width = video.videoWidth;
    let height = video.videoHeight;
    
    // Calcular proporção mantendo aspecto
    if (width > maxWidth) {
        height = (height * maxWidth) / width;
        width = maxWidth;
    }
    if (height > maxHeight) {
        width = (width * maxHeight) / height;
        height = maxHeight;
    }
    
    canvas.width = width;
    canvas.height = height;
    
    let context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, width, height);
    
    // Comprimir imagem com qualidade 0.7 para reduzir tamanho
    capturedImage = canvas.toDataURL('image/jpeg', 0.7);
    previewImage.src = capturedImage;
    
    video.style.display = 'none';
    preview.style.display = 'block';
    
    captureBtn.style.display = 'none';
    retakeBtn.style.display = 'inline-block';
    cadastroForm.style.display = 'block';
    
    // Parar câmera
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
});

// Tirar outra foto
retakeBtn.addEventListener('click', async () => {
    if (!checkBrowserSupport()) {
        return;
    }
    
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                width: { ideal: 1280 },
                height: { ideal: 720 }
            } 
        });
        
        video.srcObject = stream;
        video.style.display = 'block';
        preview.style.display = 'none';
        
        captureBtn.style.display = 'inline-block';
        retakeBtn.style.display = 'none';
        cadastroForm.style.display = 'none';
        
        capturedImage = null;
        resultDiv.innerHTML = '';
        resultDiv.className = 'result-container';
    } catch (error) {
        alert('Erro ao acessar a câmera: ' + error.message);
    }
});

// Enviar cadastro
cadastroForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const nome = document.getElementById('nome').value.trim();
    
    if (!nome) {
        alert('Por favor, digite um nome');
        return;
    }
    
    if (!capturedImage) {
        alert('Por favor, capture uma foto primeiro');
        return;
    }
    
    // Mostrar loading
    resultDiv.innerHTML = '<div class="loading"></div> Processando...';
    resultDiv.className = 'result-container';
    resultDiv.style.display = 'block';
    
    const formData = new FormData();
    formData.append('image', capturedImage);
    formData.append('nome', nome);
    
    try {
        const response = await fetch('cadastro.php', {
            method: 'POST',
            body: formData
        });
        
        // Verificar se a resposta é válida
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            const text = await response.text();
            throw new Error(`Resposta não é JSON. Recebido: ${text.substring(0, 200)}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            resultDiv.innerHTML = `
                <strong>✅ Sucesso!</strong><br>
                ${data.message}<br>
                <small>Total de pessoas cadastradas: ${data.total_cadastrados}</small>
            `;
            resultDiv.className = 'result-container success';
            
            // Limpar formulário
            document.getElementById('nome').value = '';
            cadastroForm.style.display = 'none';
            
            // Resetar botões
            setTimeout(() => {
                preview.style.display = 'none';
                retakeBtn.style.display = 'none';
                startCameraBtn.style.display = 'inline-block';
                resultDiv.style.display = 'none';
            }, 3000);
        } else {
            let errorMsg = `<strong>❌ Erro!</strong><br>${data.message}`;
            if (data.debug) {
                errorMsg += `<br><small>Debug: ${data.debug}</small>`;
            }
            resultDiv.innerHTML = errorMsg;
            resultDiv.className = 'result-container error';
        }
    } catch (error) {
        resultDiv.innerHTML = `<strong>❌ Erro!</strong><br>Erro ao enviar dados: ${error.message}`;
        resultDiv.className = 'result-container error';
    }
});

// Limpar recursos ao sair
window.addEventListener('beforeunload', () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
});
