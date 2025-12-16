"""
Módulo de Reconhecimento Facial
Detecta e identifica rostos em tempo real usando a webcam
"""

import cv2
import face_recognition
import pickle
import numpy as np
from pathlib import Path
from datetime import datetime


class ReconhecimentoFacial:
    def __init__(self):
        self.pasta_dados = Path("dados")
        self.arquivo_encodings = self.pasta_dados / "encodings.pkl"
        self.encodings_conhecidos = {}
        self.nomes_conhecidos = []
        self.carregar_dados()
    
    def carregar_dados(self):
        """Carrega os encodings faciais cadastrados"""
        if not self.arquivo_encodings.exists():
            print("⚠️  Aviso: Nenhum dado de cadastro encontrado.")
            print("   Por favor, cadastre pessoas primeiro usando o módulo de cadastro.")
            return False
        
        with open(self.arquivo_encodings, 'rb') as f:
            self.encodings_conhecidos = pickle.load(f)
        
        self.nomes_conhecidos = list(self.encodings_conhecidos.keys())
        
        if not self.nomes_conhecidos:
            print("⚠️  Aviso: Nenhuma pessoa cadastrada no sistema.")
            return False
        
        print(f"✓ Carregados {len(self.nomes_conhecidos)} rostos cadastrados")
        return True
    
    def iniciar_reconhecimento(self, mostrar_fps=True, tolerancia=0.6):
        """
        Inicia o reconhecimento facial em tempo real
        
        Args:
            mostrar_fps: Se True, mostra o FPS na tela
            tolerancia: Tolerância para reconhecimento (menor = mais rigoroso)
        """
        if not self.nomes_conhecidos:
            print("❌ Erro: Nenhuma pessoa cadastrada. Execute o cadastro primeiro.")
            return
        
        print(f"\n{'='*50}")
        print("SISTEMA DE RECONHECIMENTO FACIAL")
        print(f"{'='*50}")
        print(f"Pessoas cadastradas: {len(self.nomes_conhecidos)}")
        print(f"Tolerância: {tolerancia}")
        print("\nInstruções:")
        print("- Pressione Q ou ESC para sair")
        print("- Pressione R para recarregar cadastros")
        print(f"{'='*50}\n")
        
        # Inicializar webcam
        video_capture = cv2.VideoCapture(0)
        
        if not video_capture.isOpened():
            print("❌ Erro: Não foi possível acessar a câmera!")
            return
        
        # Variáveis para otimização
        process_this_frame = True
        fps_counter = 0
        fps_start_time = datetime.now()
        fps = 0
        
        # Histórico de detecções para estabilidade
        deteccoes_recentes = {}
        
        print("✓ Câmera iniciada. Sistema de reconhecimento ativo!\n")
        
        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("❌ Erro ao capturar frame da câmera")
                break
            
            # Processar apenas frames alternados para melhor performance
            if process_this_frame:
                # Redimensionar frame para processar mais rápido
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                
                # Encontrar rostos e seus encodings
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                
                face_names = []
                face_distances = []
                
                for face_encoding in face_encodings:
                    # Comparar com rostos conhecidos
                    matches = []
                    distances = []
                    
                    for nome, known_encoding in self.encodings_conhecidos.items():
                        distance = face_recognition.face_distance([known_encoding], face_encoding)[0]
                        distances.append(distance)
                        matches.append(distance <= tolerancia)
                    
                    name = "Desconhecido"
                    confidence = 0
                    
                    if True in matches:
                        # Encontrar o melhor match
                        best_match_index = np.argmin(distances)
                        if matches[best_match_index]:
                            name = self.nomes_conhecidos[best_match_index]
                            # Converter distância em confiança (0-100%)
                            confidence = (1 - distances[best_match_index]) * 100
                    
                    face_names.append(name)
                    face_distances.append(confidence)
            
            process_this_frame = not process_this_frame
            
            # Desenhar resultados no frame
            for (top, right, bottom, left), name, confidence in zip(face_locations, face_names, face_distances):
                # Escalar de volta para tamanho original
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                # Definir cor do retângulo
                if name == "Desconhecido":
                    cor = (0, 0, 255)  # Vermelho
                else:
                    cor = (0, 255, 0)  # Verde
                
                # Desenhar retângulo ao redor do rosto
                cv2.rectangle(frame, (left, top), (right, bottom), cor, 2)
                
                # Desenhar retângulo para o nome
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), cor, cv2.FILLED)
                
                # Escrever nome e confiança
                font = cv2.FONT_HERSHEY_DUPLEX
                if name == "Desconhecido":
                    texto = name
                else:
                    texto = f"{name} ({confidence:.0f}%)"
                
                cv2.putText(frame, texto, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)
            
            # Calcular e mostrar FPS
            if mostrar_fps:
                fps_counter += 1
                if (datetime.now() - fps_start_time).total_seconds() >= 1.0:
                    fps = fps_counter
                    fps_counter = 0
                    fps_start_time = datetime.now()
                
                cv2.putText(frame, f"FPS: {fps}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            # Mostrar informações na tela
            cv2.putText(frame, f"Cadastrados: {len(self.nomes_conhecidos)}", (10, frame.shape[0] - 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, "Q/ESC: Sair | R: Recarregar", (10, frame.shape[0] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Mostrar frame
            cv2.imshow('Reconhecimento Facial', frame)
            
            # Controles de teclado
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q') or key == 27:  # Q ou ESC
                print("\n👋 Encerrando reconhecimento facial...")
                break
            
            elif key == ord('r'):  # R para recarregar
                print("\n🔄 Recarregando cadastros...")
                self.carregar_dados()
        
        video_capture.release()
        cv2.destroyAllWindows()
        print("✓ Sistema encerrado.\n")
    
    def reconhecer_imagem(self, caminho_imagem, tolerancia=0.6):
        """
        Reconhece rostos em uma imagem estática
        
        Args:
            caminho_imagem: Caminho para a imagem
            tolerancia: Tolerância para reconhecimento
        """
        if not self.nomes_conhecidos:
            print("❌ Erro: Nenhuma pessoa cadastrada.")
            return
        
        # Carregar imagem
        imagem = face_recognition.load_image_file(caminho_imagem)
        
        # Encontrar rostos
        face_locations = face_recognition.face_locations(imagem)
        face_encodings = face_recognition.face_encodings(imagem, face_locations)
        
        print(f"\n🔍 Encontrados {len(face_locations)} rosto(s) na imagem\n")
        
        # Converter para BGR para usar com OpenCV
        imagem_bgr = cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR)
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Comparar com rostos conhecidos
            matches = []
            distances = []
            
            for nome, known_encoding in self.encodings_conhecidos.items():
                distance = face_recognition.face_distance([known_encoding], face_encoding)[0]
                distances.append(distance)
                matches.append(distance <= tolerancia)
            
            name = "Desconhecido"
            confidence = 0
            
            if True in matches:
                best_match_index = np.argmin(distances)
                if matches[best_match_index]:
                    name = self.nomes_conhecidos[best_match_index]
                    confidence = (1 - distances[best_match_index]) * 100
            
            # Desenhar resultado
            cor = (0, 255, 0) if name != "Desconhecido" else (0, 0, 255)
            cv2.rectangle(imagem_bgr, (left, top), (right, bottom), cor, 2)
            cv2.rectangle(imagem_bgr, (left, bottom - 35), (right, bottom), cor, cv2.FILLED)
            
            texto = f"{name} ({confidence:.0f}%)" if name != "Desconhecido" else name
            cv2.putText(imagem_bgr, texto, (left + 6, bottom - 6), 
                       cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
            
            print(f"• {texto}")
        
        # Mostrar resultado
        cv2.imshow('Resultado do Reconhecimento', imagem_bgr)
        print("\nPressione qualquer tecla para fechar...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def main():
    """Função principal para testar o módulo"""
    reconhecimento = ReconhecimentoFacial()
    
    while True:
        print("\n" + "="*50)
        print("MENU DE RECONHECIMENTO")
        print("="*50)
        print("1. Iniciar reconhecimento em tempo real")
        print("2. Reconhecer rostos em uma imagem")
        print("3. Recarregar dados de cadastro")
        print("0. Sair")
        print("="*50)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '1':
            reconhecimento.iniciar_reconhecimento()
        
        elif opcao == '2':
            caminho = input("\nDigite o caminho da imagem: ").strip()
            if Path(caminho).exists():
                reconhecimento.reconhecer_imagem(caminho)
            else:
                print("❌ Arquivo não encontrado!")
        
        elif opcao == '3':
            reconhecimento.carregar_dados()
        
        elif opcao == '0':
            print("\n👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida!")


if __name__ == "__main__":
    main()
