<?php
require_once 'config.php';

header('Content-Type: application/json');

$action = $_GET['action'] ?? '';

try {
    switch ($action) {
        case 'reconhecer':
            if ($_SERVER['REQUEST_METHOD'] === 'POST') {
                $data = json_decode(file_get_contents('php://input'), true);
                
                if (!isset($data['image'])) {
                    echo json_encode(['success' => false, 'message' => 'Imagem não fornecida']);
                    exit;
                }
                
                // Decodificar imagem base64
                $imageData = $data['image'];
                $imageData = str_replace('data:image/png;base64,', '', $imageData);
                $imageData = str_replace(' ', '+', $imageData);
                $imageData = base64_decode($imageData);
                
                if ($imageData === false) {
                    echo json_encode(['success' => false, 'message' => 'Erro ao decodificar imagem']);
                    exit;
                }
                
                // Salvar imagem temporária
                $tempFile = TEMP_PATH . '/' . uniqid() . '.png';
                
                if (!file_put_contents($tempFile, $imageData)) {
                    echo json_encode(['success' => false, 'message' => 'Erro ao salvar imagem']);
                    exit;
                }
                
                // Executar API Python
                $resultado = executarAPI("reconhecer \"$tempFile\"");
                
                // Remover arquivo temporário
                if (file_exists($tempFile)) {
                    unlink($tempFile);
                }
                
                echo json_encode($resultado);
            }
            break;
        
        case 'listar':
            $resultado = executarAPI('listar');
            echo json_encode($resultado);
            break;
        
        case 'remover':
            if ($_SERVER['REQUEST_METHOD'] === 'POST') {
                $data = json_decode(file_get_contents('php://input'), true);
                
                if (!isset($data['nome'])) {
                    echo json_encode(['success' => false, 'message' => 'Nome não fornecido']);
                    exit;
                }
                
                $nome = sanitizeFilename($data['nome']);
                
                if (empty($nome)) {
                    echo json_encode(['success' => false, 'message' => 'Nome inválido']);
                    exit;
                }
                
                $resultado = executarAPI("remover \"$nome\"");
                echo json_encode($resultado);
            }
            break;
        
        default:
            echo json_encode(['success' => false, 'message' => 'Ação inválida']);
            break;
    }
} catch (Exception $e) {
    echo json_encode(['success' => false, 'message' => 'Erro: ' . $e->getMessage()]);
}
