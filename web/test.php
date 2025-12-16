<?php
require_once 'config.php';

header('Content-Type: application/json');

// Teste de configuração
$teste = [
    'php_version' => phpversion(),
    'base_path' => BASE_PATH,
    'python_bin' => PYTHON_BIN,
    'python_exists' => file_exists(PYTHON_BIN) ? 'sim' : 'não',
    'web_api_script' => WEB_API_SCRIPT,
    'script_exists' => file_exists(WEB_API_SCRIPT) ? 'sim' : 'não',
    'temp_path' => TEMP_PATH,
    'temp_writable' => is_writable(TEMP_PATH) ? 'sim' : 'não',
];

// Testar execução da API
$teste['api_test'] = executarAPI('listar');

echo json_encode($teste, JSON_PRETTY_PRINT);
