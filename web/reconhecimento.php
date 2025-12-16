<?php
require_once 'config.php';
include 'header.php';
?>

<div class="page-header">
    <h2>👁️ Reconhecimento Facial em Tempo Real</h2>
    <p>Identifique rostos cadastrados usando a webcam</p>
</div>

<div class="camera-section">
    <div class="camera-container camera-large">
        <video id="video" autoplay playsinline></video>
        <canvas id="canvas" style="display: none;"></canvas>
        <div id="overlay" class="face-overlay"></div>
    </div>
    
    <div class="camera-controls">
        <button id="startRecognition" class="btn btn-primary btn-large">
            <span class="icon">▶️</span> Iniciar Reconhecimento
        </button>
        <button id="stopRecognition" class="btn btn-danger btn-large" style="display: none;">
            <span class="icon">⏹️</span> Parar Reconhecimento
        </button>
    </div>
</div>

<div class="recognition-info">
    <div class="info-card">
        <div class="info-icon">👥</div>
        <div class="info-content">
            <div class="info-label">Pessoas Cadastradas</div>
            <div id="totalCadastrados" class="info-value">-</div>
        </div>
    </div>
    
    <div class="info-card">
        <div class="info-icon">📊</div>
        <div class="info-content">
            <div class="info-label">Status</div>
            <div id="status" class="info-value">Aguardando...</div>
        </div>
    </div>
    
    <div class="info-card">
        <div class="info-icon">🎯</div>
        <div class="info-content">
            <div class="info-label">Última Detecção</div>
            <div id="lastDetection" class="info-value">Nenhuma</div>
        </div>
    </div>
</div>

<div id="detectionResults" class="detection-results"></div>

<div class="instructions">
    <h3>📋 Instruções:</h3>
    <ul>
        <li>Clique em "Iniciar Reconhecimento" e permita o acesso à webcam</li>
        <li>O sistema analisará automaticamente a cada 2 segundos</li>
        <li>Rostos conhecidos aparecerão com nome e confiança</li>
        <li>Rostos desconhecidos serão marcados como "Desconhecido"</li>
        <li>Clique em "Parar Reconhecimento" para encerrar</li>
    </ul>
</div>

<script src="js/reconhecimento.js"></script>

<?php include 'footer.php'; ?>
