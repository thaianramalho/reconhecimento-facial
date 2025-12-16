<?php
require_once 'config.php';

// Listar pessoas cadastradas
$resultado = executarAPI('listar');

include 'header.php';
?>

<div class="page-header">
    <h2>📋 Pessoas Cadastradas</h2>
    <p>Gerenciamento de rostos cadastrados no sistema</p>
</div>

<?php if ($resultado && $resultado['success']): ?>
    <div class="stats-card">
        <div class="stat-item">
            <div class="stat-icon">👥</div>
            <div class="stat-content">
                <div class="stat-value"><?php echo $resultado['total']; ?></div>
                <div class="stat-label">Pessoas Cadastradas</div>
            </div>
        </div>
    </div>

    <?php if ($resultado['total'] > 0): ?>
        <div class="pessoas-grid">
            <?php foreach ($resultado['pessoas'] as $pessoa): ?>
                <div class="pessoa-card">
                    <div class="pessoa-image">
                        <?php 
                        $imagePath = '../rostos_cadastrados/' . $pessoa . '.jpg';
                        if (file_exists($imagePath)): 
                        ?>
                            <img src="<?php echo $imagePath; ?>" alt="<?php echo htmlspecialchars($pessoa); ?>">
                        <?php else: ?>
                            <div class="no-image">👤</div>
                        <?php endif; ?>
                    </div>
                    <div class="pessoa-info">
                        <h3><?php echo htmlspecialchars($pessoa); ?></h3>
                        <div class="pessoa-actions">
                            <button class="btn btn-danger btn-small" 
                                    onclick="removerPessoa('<?php echo htmlspecialchars($pessoa); ?>')">
                                <span class="icon">🗑️</span> Remover
                            </button>
                        </div>
                    </div>
                </div>
            <?php endforeach; ?>
        </div>
    <?php else: ?>
        <div class="empty-state">
            <div class="empty-icon">📭</div>
            <h3>Nenhuma pessoa cadastrada</h3>
            <p>Comece cadastrando pessoas usando a página de cadastro</p>
            <a href="cadastro.php" class="btn btn-primary">
                <span class="icon">📝</span> Cadastrar Agora
            </a>
        </div>
    <?php endif; ?>
<?php else: ?>
    <div class="alert alert-error">
        ❌ Erro ao carregar lista de pessoas
    </div>
<?php endif; ?>

<script>
function removerPessoa(nome) {
    if (!confirm(`Deseja realmente remover ${nome}?`)) {
        return;
    }
    
    fetch('api.php?action=remover', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nome: nome })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert('Erro: ' + data.message);
        }
    })
    .catch(error => {
        alert('Erro ao remover pessoa: ' + error);
    });
}
</script>

<?php include 'footer.php'; ?>
