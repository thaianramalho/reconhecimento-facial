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

// Iniciar câmera
startCameraBtn.addEventListener('click', async () => {
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
        alert('Erro ao acessar a câmera: ' + error.message);
    }
});

// Capturar foto
captureBtn.addEventListener('click', () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    let context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    capturedImage = canvas.toDataURL('image/png');
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
