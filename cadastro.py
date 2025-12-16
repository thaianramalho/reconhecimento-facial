"""
Módulo de Cadastro Facial
Captura imagens da webcam e salva com nome do usuário
"""

import cv2
import os
import face_recognition
import pickle
from pathlib import Path


class CadastroFacial:
    def __init__(self):
        self.pasta_rostos = Path("rostos_cadastrados")
        self.pasta_dados = Path("dados")
        self.arquivo_encodings = self.pasta_dados / "encodings.pkl"
        
        # Criar pastas se não existirem
        self.pasta_rostos.mkdir(exist_ok=True)
        self.pasta_dados.mkdir(exist_ok=True)
    
    def carregar_encodings(self):
        """Carrega os encodings salvos ou retorna dicionário vazio"""
        if self.arquivo_encodings.exists():
            with open(self.arquivo_encodings, 'rb') as f:
                return pickle.load(f)
        return {}
    
    def salvar_encodings(self, encodings):
        """Salva os encodings em arquivo"""
        with open(self.arquivo_encodings, 'wb') as f:
            pickle.dump(encodings, f)
    
    def cadastrar_pessoa(self, nome):
        """
        Captura foto da pessoa e salva seu encoding facial
        
        Args:
            nome: Nome da pessoa a ser cadastrada
        """
        print(f"\n{'='*50}")
        print(f"CADASTRANDO: {nome}")
        print(f"{'='*50}")
        print("\nInstruções:")
        print("- Posicione seu rosto na frente da câmera")
        print("- Pressione ESPAÇO para capturar a foto")
        print("- Pressione ESC para cancelar")
        print(f"{'='*50}\n")
        
        # Inicializar webcam
        video_capture = cv2.VideoCapture(0)
        
        if not video_capture.isOpened():
            print("❌ Erro: Não foi possível acessar a câmera!")
            return False
        
        foto_capturada = False
        imagem_face = None
        
        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("❌ Erro ao capturar frame da câmera")
                break
            
            # Detectar rostos no frame
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            
            # Desenhar retângulos nos rostos detectados
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, "Rosto detectado", (left, top - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Mostrar informações na tela
            cv2.putText(frame, f"Cadastrando: {nome}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "ESPACO: Capturar | ESC: Cancelar", (10, frame.shape[0] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            cv2.imshow('Cadastro Facial', frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            # ESPAÇO para capturar
            if key == 32:  # Código da tecla ESPAÇO
                if len(face_locations) > 0:
                    imagem_face = rgb_frame
                    foto_capturada = True
                    print("✓ Foto capturada com sucesso!")
                    break
                else:
                    print("⚠️  Nenhum rosto detectado. Tente novamente.")
            
            # ESC para cancelar
            elif key == 27:  # Código da tecla ESC
                print("❌ Cadastro cancelado pelo usuário")
                break
        
        video_capture.release()
        cv2.destroyAllWindows()
        
        if not foto_capturada:
            return False
        
        # Processar e salvar o encoding facial
        print("\n🔍 Processando imagem facial...")
        
        face_locations = face_recognition.face_locations(imagem_face)
        
        if len(face_locations) == 0:
            print("❌ Erro: Nenhum rosto encontrado na imagem capturada")
            return False
        
        if len(face_locations) > 1:
            print("⚠️  Aviso: Múltiplos rostos detectados. Usando o primeiro.")
        
        # Gerar encoding do rosto
        face_encodings = face_recognition.face_encodings(imagem_face, face_locations)
        
        if len(face_encodings) == 0:
            print("❌ Erro: Não foi possível gerar encoding facial")
            return False
        
        face_encoding = face_encodings[0]
        
        # Salvar imagem
        imagem_bgr = cv2.cvtColor(imagem_face, cv2.COLOR_RGB2BGR)
        caminho_imagem = self.pasta_rostos / f"{nome}.jpg"
        cv2.imwrite(str(caminho_imagem), imagem_bgr)
        print(f"✓ Imagem salva em: {caminho_imagem}")
        
        # Carregar encodings existentes e adicionar novo
        encodings = self.carregar_encodings()
        encodings[nome] = face_encoding
        self.salvar_encodings(encodings)
        print(f"✓ Encoding facial salvo para {nome}")
        
        print(f"\n{'='*50}")
        print(f"✅ CADASTRO CONCLUÍDO COM SUCESSO!")
        print(f"{'='*50}\n")
        
        return True
    
    def listar_cadastrados(self):
        """Lista todas as pessoas cadastradas"""
        encodings = self.carregar_encodings()
        
        if not encodings:
            print("\n📋 Nenhuma pessoa cadastrada ainda.\n")
            return []
        
        print(f"\n{'='*50}")
        print(f"PESSOAS CADASTRADAS ({len(encodings)})")
        print(f"{'='*50}")
        
        for i, nome in enumerate(sorted(encodings.keys()), 1):
            print(f"{i}. {nome}")
        
        print(f"{'='*50}\n")
        
        return list(encodings.keys())
    
    def remover_cadastro(self, nome):
        """Remove um cadastro existente"""
        encodings = self.carregar_encodings()
        
        if nome not in encodings:
            print(f"❌ Erro: {nome} não está cadastrado")
            return False
        
        # Remover encoding
        del encodings[nome]
        self.salvar_encodings(encodings)
        
        # Remover imagem se existir
        caminho_imagem = self.pasta_rostos / f"{nome}.jpg"
        if caminho_imagem.exists():
            caminho_imagem.unlink()
        
        print(f"✅ Cadastro de {nome} removido com sucesso!")
        return True


def main():
    """Função principal para testar o módulo"""
    cadastro = CadastroFacial()
    
    while True:
        print("\n" + "="*50)
        print("MENU DE CADASTRO")
        print("="*50)
        print("1. Cadastrar nova pessoa")
        print("2. Listar pessoas cadastradas")
        print("3. Remover cadastro")
        print("0. Sair")
        print("="*50)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '1':
            nome = input("\nDigite o nome da pessoa: ").strip()
            if nome:
                cadastro.cadastrar_pessoa(nome)
            else:
                print("❌ Nome inválido!")
        
        elif opcao == '2':
            cadastro.listar_cadastrados()
        
        elif opcao == '3':
            pessoas = cadastro.listar_cadastrados()
            if pessoas:
                nome = input("\nDigite o nome para remover: ").strip()
                if nome:
                    cadastro.remover_cadastro(nome)
        
        elif opcao == '0':
            print("\n👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida!")


if __name__ == "__main__":
    main()
