<?php
/**
 * Configurações da Aplicação Web
 */

// Caminhos
define('BASE_PATH', dirname(__DIR__));
define('WEB_PATH', __DIR__);
define('UPLOADS_PATH', WEB_PATH . '/uploads');
define('TEMP_PATH', WEB_PATH . '/temp');

// Python
define('PYTHON_BIN', BASE_PATH . '/venv/bin/python');
define('WEB_API_SCRIPT', BASE_PATH . '/web_api.py');

// Configurações da aplicação
define('APP_NAME', 'Sistema de Reconhecimento Facial');
define('APP_VERSION', '1.0.0');

// Criar diretórios necessários
if (!file_exists(UPLOADS_PATH)) {
    mkdir(UPLOADS_PATH, 0755, true);
}
if (!file_exists(TEMP_PATH)) {
    mkdir(TEMP_PATH, 0755, true);
}

/**
 * Executa a API Python
 */
function executarAPI($comando) {
    $cmd = PYTHON_BIN . ' ' . WEB_API_SCRIPT . ' ' . $comando . ' 2>&1';
    $output = shell_exec($cmd);
    
    // Extrair apenas a linha JSON (última linha que começa com {)
    $lines = explode("\n", trim($output));
    $jsonLine = '';
    
    // Procurar pela linha que contém JSON válido
    foreach (array_reverse($lines) as $line) {
        $line = trim($line);
        if (!empty($line) && ($line[0] === '{' || $line[0] === '[')) {
            $jsonLine = $line;
            break;
        }
    }
    
    if (empty($jsonLine)) {
        error_log("Nenhum JSON encontrado. Output: " . $output);
        return [
            'success' => false,
            'message' => 'Erro ao processar resposta do servidor'
        ];
    }
    
    $resultado = json_decode($jsonLine, true);
    
    if ($resultado === null) {
        error_log("Erro ao decodificar JSON: " . $jsonLine);
        return [
            'success' => false,
            'message' => 'Erro ao processar resposta do servidor'
        ];
    }
    
    return $resultado;
}

/**
 * Retorna JSON response
 */
function jsonResponse($data) {
    header('Content-Type: application/json');
    echo json_encode($data);
    exit;
}

/**
 * Limpa nome de arquivo
 */
function sanitizeFilename($filename) {
    $filename = preg_replace('/[^a-zA-Z0-9_-]/', '', $filename);
    return substr($filename, 0, 255);
}
