<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo APP_NAME; ?></title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>👁️ <?php echo APP_NAME; ?></h1>
            <p class="subtitle">Detecção e Identificação de Rostos</p>
        </header>

        <nav class="nav">
            <a href="index.php" class="nav-item active">
                <span class="icon">🏠</span>
                <span>Início</span>
            </a>
            <a href="cadastro.php" class="nav-item">
                <span class="icon">📝</span>
                <span>Cadastro</span>
            </a>
            <a href="reconhecimento.php" class="nav-item">
                <span class="icon">👁️</span>
                <span>Reconhecimento</span>
            </a>
            <a href="lista.php" class="nav-item">
                <span class="icon">📋</span>
                <span>Lista</span>
            </a>
        </nav>

        <main class="main">
