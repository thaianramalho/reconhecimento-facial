#!/usr/bin/env python3
"""
Sistema de Reconhecimento Facial
Menu principal para navegação entre cadastro e reconhecimento
"""

import sys
from cadastro import CadastroFacial
from reconhecimento import ReconhecimentoFacial


def exibir_banner():
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║      SISTEMA DE RECONHECIMENTO FACIAL                ║
    ║                                                       ║
    ║      Detecção e Identificação de Rostos              ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """
    print(banner)


def menu_principal():
    cadastro = CadastroFacial()
    reconhecimento = ReconhecimentoFacial()
    
    while True:
        exibir_banner()
        
        print("\n" + "="*55)
        print("MENU PRINCIPAL")
        print("="*55)
        print()
        print("  📝 CADASTRO")
        print("    1. Cadastrar nova pessoa")
        print("    2. Listar pessoas cadastradas")
        print("    3. Remover cadastro")
        print()
        print("  👁️  RECONHECIMENTO")
        print("    4. Iniciar reconhecimento em tempo real")
        print("    5. Reconhecer rostos em uma imagem")
        print()
        print("  ⚙️  CONFIGURAÇÕES")
        print("    6. Recarregar dados de cadastro")
        print()
        print("  🚪 SAIR")
        print("    0. Sair do sistema")
        print()
        print("="*55)
        
        opcao = input("\n➜ Escolha uma opção: ").strip()
        
        if opcao == '1':
            # Cadastrar nova pessoa
            print("\n" + "="*55)
            nome = input("Digite o nome da pessoa a cadastrar: ").strip()
            if nome:
                cadastro.cadastrar_pessoa(nome)
                input("\n✓ Pressione ENTER para continuar...")
            else:
                print("❌ Nome inválido!")
                input("Pressione ENTER para continuar...")
        
        elif opcao == '2':
            # Listar pessoas cadastradas
            cadastro.listar_cadastrados()
            input("Pressione ENTER para continuar...")
        
        elif opcao == '3':
            # Remover cadastro
            pessoas = cadastro.listar_cadastrados()
            if pessoas:
                nome = input("\nDigite o nome para remover: ").strip()
                if nome:
                    confirmar = input(f"⚠️  Confirma a remoção de '{nome}'? (s/N): ").strip().lower()
                    if confirmar == 's':
                        cadastro.remover_cadastro(nome)
                    else:
                        print("❌ Remoção cancelada.")
            input("\nPressione ENTER para continuar...")
        
        elif opcao == '4':
            # Reconhecimento em tempo real
            print("\n" + "="*55)
            print("Iniciando reconhecimento facial em tempo real...")
            print("="*55)
            reconhecimento.iniciar_reconhecimento()
            input("\nPressione ENTER para continuar...")
        
        elif opcao == '5':
            # Reconhecer em imagem
            print("\n" + "="*55)
            caminho = input("Digite o caminho da imagem: ").strip()
            if caminho:
                from pathlib import Path
                if Path(caminho).exists():
                    reconhecimento.reconhecer_imagem(caminho)
                else:
                    print("❌ Arquivo não encontrado!")
            input("\nPressione ENTER para continuar...")
        
        elif opcao == '6':
            # Recarregar dados
            print("\n🔄 Recarregando dados de cadastro...")
            cadastro = CadastroFacial()
            reconhecimento = ReconhecimentoFacial()
            print("✓ Dados recarregados!")
            input("\nPressione ENTER para continuar...")
        
        elif opcao == '0':
            # Sair
            print("\n" + "="*55)
            print("              👋 Até logo!")
            print("="*55)
            print()
            sys.exit(0)
        
        else:
            print("\n❌ Opção inválida!")
            input("Pressione ENTER para continuar...")


if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Sistema encerrado pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)
