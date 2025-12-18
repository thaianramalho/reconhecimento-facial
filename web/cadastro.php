<?php
require_once 'config.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    header('Content-Type: application/json');
    
    $response = ['success' => false, 'message' => ''];
    
    try {
        if (!isset($_POST['image']) || !isset($_POST['nome'])) {
            $response['message'] = 'Dados incompletos';
            echo json_encode($response);
            exit;
        }
        
        $nome = sanitizeFilename($_POST['nome']);
        
        if (empty($nome)) {
            $response['message'] = 'Nome inválido';
            echo json_encode($response);
            exit;
        }
        
        // Decodificar imagem base64 (suporta PNG e JPEG)
        $imageData = $_POST['image'];
        $imageData = str_replace('data:image/png;base64,', '', $imageData);
        $imageData = str_replace('data:image/jpeg;base64,', '', $imageData);
        $imageData = str_replace('data:image/jpg;base64,', '', $imageData);
        $imageData = str_replace(' ', '+', $imageData);
        $imageData = base64_decode($imageData);
        
        if ($imageData === false) {
            $response['message'] = 'Erro ao decodificar imagem';
            echo json_encode($response);
            exit;
        }
        
        // Salvar imagem temporária (usar JPG pois JavaScript envia JPEG)
        $tempFile = TEMP_PATH . '/' . uniqid() . '.jpg';
        
        if (!file_put_contents($tempFile, $imageData)) {
            $response['message'] = 'Erro ao salvar imagem temporária';
            echo json_encode($response);
            exit;
        }
        
        // Executar API Python
        $resultado = executarAPI("cadastrar \"$tempFile\" \"$nome\"");
        
        // Remover arquivo temporário
        if (file_exists($tempFile)) {
            unlink($tempFile);
        }
        
        echo json_encode($resultado);
        exit;
        
    } catch (Exception $e) {
        $response['message'] = 'Erro no servidor: ' . $e->getMessage();
        echo json_encode($response);
        exit;
    }
}

include 'header.php';
?>

<div class="page-header">
    <h2>📝 Cadastro de Rosto</h2>
    <p>Capture sua foto usando a webcam e cadastre-se no sistema</p>
</div>

<div class="camera-section">
    <div class="camera-container">
        <video id="video" autoplay playsinline></video>
        <canvas id="canvas" style="display: none;"></canvas>
        <div id="preview" class="preview-container" style="display: none;">
            <img id="preview-image" alt="Preview">
        </div>
    </div>
    
    <div class="camera-controls">
        <button id="startCamera" class="btn btn-primary">
            <span class="icon">📷</span> Iniciar Câmera
        </button>
        <button id="capture" class="btn btn-success" style="display: none;">
            <span class="icon">📸</span> Capturar Foto
        </button>
        <button id="retake" class="btn btn-warning" style="display: none;">
            <span class="icon">🔄</span> Tirar Outra
        </button>
    </div>
</div>

<div class="form-section">
    <form id="cadastroForm" style="display: none;">
        <div class="form-group">
            <label for="nome">Nome da Pessoa:</label>
            <input type="text" id="nome" name="nome" class="form-control" required 
                   placeholder="Digite o nome completo">
        </div>
        
        <button type="submit" class="btn btn-primary btn-large">
            <span class="icon">✅</span> Cadastrar Rosto
        </button>
    </form>
</div>

<div id="result" class="result-container"></div>

<div class="instructions">
    <h3>📋 Instruções:</h3>
    <ul>
        <li>Clique em "Iniciar Câmera" e permita o acesso à webcam</li>
        <li>Posicione seu rosto centralizado na câmera</li>
        <li>Clique em "Capturar Foto" quando estiver pronto</li>
        <li>Digite seu nome e clique em "Cadastrar Rosto"</li>
        <li>Aguarde o processamento (pode levar alguns segundos)</li>
    </ul>
</div>

<script src="js/cadastro.js"></script>

<?php include 'footer.php'; ?>
