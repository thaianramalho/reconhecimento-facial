// Reconhecimento Facial em Tempo Real
let video = document.getElementById('video');
let canvas = document.getElementById('canvas');
let overlay = document.getElementById('overlay');
let startBtn = document.getElementById('startRecognition');
let stopBtn = document.getElementById('stopRecognition');
let statusDiv = document.getElementById('status');
let totalCadastradosDiv = document.getElementById('totalCadastrados');
let lastDetectionDiv = document.getElementById('lastDetection');
let detectionResultsDiv = document.getElementById('detectionResults');

let stream = null;
let recognitionInterval = null;
let isRecognizing = false;

// Carregar total de cadastrados
async function loadTotalCadastrados() {
    try {
        const response = await fetch('api.php?action=listar');
        const data = await response.json();
        
        if (data.success) {
            totalCadastradosDiv.textContent = data.total;
        }
    } catch (error) {
        console.error('Erro ao carregar total:', error);
    }
}

// Iniciar reconhecimento
startBtn.addEventListener('click', async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                width: { ideal: 1280 },
                height: { ideal: 720 }
            } 
        });
        
        video.srcObject = stream;
        video.style.display = 'block';
        
        startBtn.style.display = 'none';
        stopBtn.style.display = 'inline-block';
        
        statusDiv.textContent = 'Ativo';
        statusDiv.style.color = '#4CAF50';
        
        isRecognizing = true;
        
        console.log('Reconhecimento iniciado');
        
        // Aguardar vídeo carregar
        video.onloadedmetadata = () => {
            console.log('Vídeo carregado, iniciando intervalo de reconhecimento');
            // Iniciar reconhecimento a cada 2 segundos
            recognitionInterval = setInterval(() => {
                console.log('Executando reconhecimento...');
                recognizeFrame();
            }, 2000);
            
            // Executar primeiro reconhecimento imediatamente
            recognizeFrame();
        };
        
    } catch (error) {
        alert('Erro ao acessar a câmera: ' + error.message);
        statusDiv.textContent = 'Erro';
        statusDiv.style.color = '#f44336';
    }
});

// Parar reconhecimento
stopBtn.addEventListener('click', () => {
    stopRecognition();
});

function stopRecognition() {
    isRecognizing = false;
    
    if (recognitionInterval) {
        clearInterval(recognitionInterval);
        recognitionInterval = null;
    }
    
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    
    video.style.display = 'none';
    startBtn.style.display = 'inline-block';
    stopBtn.style.display = 'none';
    
    statusDiv.textContent = 'Parado';
    statusDiv.style.color = '#666';
    
    overlay.innerHTML = '';
    detectionResultsDiv.innerHTML = '';
}

// Reconhecer frame atual
async function recognizeFrame() {
    if (!isRecognizing || !video.videoWidth) {
        return;
    }
    
    try {
        // Capturar frame do vídeo
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        let context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        const imageData = canvas.toDataURL('image/png');
        
        statusDiv.textContent = 'Processando...';
        statusDiv.style.color = '#ff9800';
        
        const response = await fetch('api.php?action=reconhecer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            statusDiv.textContent = 'Ativo';
            statusDiv.style.color = '#4CAF50';
            
            if (data.rostos && data.rostos.length > 0) {
                displayResults(data.rostos);
            } else {
                detectionResultsDiv.innerHTML = '<p style="text-align:center; color:#666;">Nenhum rosto detectado</p>';
                lastDetectionDiv.textContent = 'Nenhuma';
                overlay.innerHTML = '';
            }
        } else {
            console.error('Erro na resposta:', data.message);
            statusDiv.textContent = 'Erro';
            statusDiv.style.color = '#f44336';
            detectionResultsDiv.innerHTML = `<p style="text-align:center; color:#f44336;">Erro: ${data.message}</p>`;
        }
        
    } catch (error) {
        console.error('Erro no reconhecimento:', error);
        statusDiv.textContent = 'Erro';
        statusDiv.style.color = '#f44336';
        detectionResultsDiv.innerHTML = `<p style="text-align:center; color:#f44336;">Erro: ${error.message}</p>`;
    }
}

// Exibir resultados
function displayResults(rostos) {
    // Limpar overlay
    overlay.innerHTML = '';
    
    // Criar HTML dos resultados
    let resultsHTML = '';
    
    rostos.forEach(rosto => {
        const isKnown = rosto.nome !== 'Desconhecido';
        const color = isKnown ? '#4CAF50' : '#f44336';
        const bgColor = isKnown ? '#d4edda' : '#f8d7da';
        
        resultsHTML += `
            <div class="detection-item" style="background: ${bgColor};">
                <div>
                    <div class="detection-name" style="color: ${color};">
                        ${rosto.nome}
                    </div>
                    ${isKnown ? `<small>Confiança: ${rosto.confianca.toFixed(1)}%</small>` : ''}
                </div>
            </div>
        `;
        
        // Desenhar retângulo no overlay (proporcional ao vídeo)
        const videoRect = video.getBoundingClientRect();
        const scaleX = videoRect.width / canvas.width;
        const scaleY = videoRect.height / canvas.height;
        
        const rectDiv = document.createElement('div');
        rectDiv.style.position = 'absolute';
        rectDiv.style.border = `3px solid ${color}`;
        rectDiv.style.left = (rosto.posicao.left * scaleX) + 'px';
        rectDiv.style.top = (rosto.posicao.top * scaleY) + 'px';
        rectDiv.style.width = ((rosto.posicao.right - rosto.posicao.left) * scaleX) + 'px';
        rectDiv.style.height = ((rosto.posicao.bottom - rosto.posicao.top) * scaleY) + 'px';
        rectDiv.style.boxSizing = 'border-box';
        
        // Label
        const labelDiv = document.createElement('div');
        labelDiv.style.position = 'absolute';
        labelDiv.style.bottom = '-25px';
        labelDiv.style.left = '0';
        labelDiv.style.background = color;
        labelDiv.style.color = 'white';
        labelDiv.style.padding = '2px 8px';
        labelDiv.style.fontSize = '12px';
        labelDiv.style.fontWeight = 'bold';
        labelDiv.style.whiteSpace = 'nowrap';
        labelDiv.textContent = isKnown ? `${rosto.nome} (${rosto.confianca.toFixed(0)}%)` : rosto.nome;
        
        rectDiv.appendChild(labelDiv);
        overlay.appendChild(rectDiv);
    });
    
    detectionResultsDiv.innerHTML = resultsHTML;
    
    // Atualizar última detecção
    const knownFaces = rostos.filter(r => r.nome !== 'Desconhecido');
    if (knownFaces.length > 0) {
        lastDetectionDiv.textContent = knownFaces.map(r => r.nome).join(', ');
    } else {
        lastDetectionDiv.textContent = 'Rostos desconhecidos';
    }
}

// Limpar recursos ao sair
window.addEventListener('beforeunload', () => {
    stopRecognition();
});

// Carregar informações iniciais
loadTotalCadastrados();
