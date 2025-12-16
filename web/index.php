<?php
require_once 'config.php';
include 'header.php';
?>

<div class="welcome-section">
    <div class="welcome-icon">🎯</div>
    <h2>Bem-vindo ao Sistema de Reconhecimento Facial</h2>
    <p class="welcome-text">
        Sistema completo para cadastro e identificação de rostos usando 
        inteligência artificial e visão computacional.
    </p>
</div>

<div class="features-grid">
    <div class="feature-card">
        <div class="feature-icon">📝</div>
        <h3>Cadastro</h3>
        <p>Cadastre novos rostos usando a webcam do seu navegador de forma simples e rápida.</p>
        <a href="cadastro.php" class="btn btn-primary">Cadastrar Rosto</a>
    </div>

    <div class="feature-card">
        <div class="feature-icon">👁️</div>
        <h3>Reconhecimento</h3>
        <p>Identifique rostos em tempo real com a webcam e veja quem está cadastrado no sistema.</p>
        <a href="reconhecimento.php" class="btn btn-primary">Reconhecer Rostos</a>
    </div>

    <div class="feature-card">
        <div class="feature-icon">📋</div>
        <h3>Lista de Cadastros</h3>
        <p>Visualize todas as pessoas cadastradas no sistema e gerencie os cadastros.</p>
        <a href="lista.php" class="btn btn-primary">Ver Lista</a>
    </div>
</div>

<div class="info-section">
    <h3>ℹ️ Como Funciona</h3>
    <div class="steps">
        <div class="step">
            <div class="step-number">1</div>
            <div class="step-content">
                <h4>Cadastre</h4>
                <p>Tire uma foto usando a webcam e informe o nome da pessoa</p>
            </div>
        </div>
        <div class="step">
            <div class="step-number">2</div>
            <div class="step-content">
                <h4>Sistema Aprende</h4>
                <p>O sistema analisa e armazena as características faciais únicas</p>
            </div>
        </div>
        <div class="step">
            <div class="step-number">3</div>
            <div class="step-content">
                <h4>Reconheça</h4>
                <p>Identifique pessoas cadastradas em tempo real com alta precisão</p>
            </div>
        </div>
    </div>
</div>

<?php include 'footer.php'; ?>
