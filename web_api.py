#!/usr/bin/env python3
"""
API Web para Reconhecimento Facial
Processa imagens recebidas via linha de comando
"""

import sys
import json
import face_recognition
import pickle
import numpy as np
from pathlib import Path
import cv2


class FacialRecognitionAPI:
    def __init__(self):
        self.pasta_dados = Path("dados")
        self.pasta_rostos = Path("rostos_cadastrados")
        self.arquivo_encodings = self.pasta_dados / "encodings.pkl"
        
        # Criar pastas se não existirem
        self.pasta_dados.mkdir(exist_ok=True)
        self.pasta_rostos.mkdir(exist_ok=True)
    
    def carregar_encodings(self):
        """Carrega os encodings salvos"""
        if self.arquivo_encodings.exists():
            with open(self.arquivo_encodings, 'rb') as f:
                return pickle.load(f)
        return {}
    
    def salvar_encodings(self, encodings):
        """Salva os encodings"""
        with open(self.arquivo_encodings, 'wb') as f:
            pickle.dump(encodings, f)
    
    def cadastrar_rosto(self, caminho_imagem, nome):
        """
        Cadastra um rosto a partir de uma imagem
        
        Args:
            caminho_imagem: Caminho para a imagem
            nome: Nome da pessoa
            
        Returns:
            dict com status e mensagem
        """
        try:
            # Carregar imagem
            imagem = face_recognition.load_image_file(caminho_imagem)
            
            # Detectar rostos
            face_locations = face_recognition.face_locations(imagem)
            
            if len(face_locations) == 0:
                return {
                    'success': False,
                    'message': 'Nenhum rosto detectado na imagem'
                }
            
            if len(face_locations) > 1:
                return {
                    'success': False,
                    'message': f'Múltiplos rostos detectados ({len(face_locations)}). Use uma imagem com apenas um rosto.'
                }
            
            # Gerar encoding
            face_encodings = face_recognition.face_encodings(imagem, face_locations)
            
            if len(face_encodings) == 0:
                return {
                    'success': False,
                    'message': 'Não foi possível gerar encoding facial'
                }
            
            face_encoding = face_encodings[0]
            
            # Salvar imagem
            imagem_bgr = cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR)
            caminho_salvar = self.pasta_rostos / f"{nome}.jpg"
            cv2.imwrite(str(caminho_salvar), imagem_bgr)
            
            # Salvar encoding
            encodings = self.carregar_encodings()
            encodings[nome] = face_encoding
            self.salvar_encodings(encodings)
            
            return {
                'success': True,
                'message': f'Rosto de {nome} cadastrado com sucesso!',
                'total_cadastrados': len(encodings)
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao processar imagem: {str(e)}'
            }
    
    def reconhecer_rosto(self, caminho_imagem, tolerancia=0.6):
        """
        Reconhece rostos em uma imagem
        
        Args:
            caminho_imagem: Caminho para a imagem
            tolerancia: Tolerância para reconhecimento
            
        Returns:
            dict com rostos detectados e suas identificações
        """
        try:
            # Carregar encodings conhecidos
            encodings_conhecidos = self.carregar_encodings()
            
            if not encodings_conhecidos:
                return {
                    'success': False,
                    'message': 'Nenhuma pessoa cadastrada no sistema'
                }
            
            # Carregar imagem
            imagem = face_recognition.load_image_file(caminho_imagem)
            
            # Detectar rostos
            face_locations = face_recognition.face_locations(imagem)
            face_encodings = face_recognition.face_encodings(imagem, face_locations)
            
            if len(face_locations) == 0:
                return {
                    'success': True,
                    'message': 'Nenhum rosto detectado',
                    'rostos': []
                }
            
            rostos_detectados = []
            
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Comparar com rostos conhecidos
                matches = []
                distances = []
                nomes = list(encodings_conhecidos.keys())
                
                for nome, known_encoding in encodings_conhecidos.items():
                    distance = face_recognition.face_distance([known_encoding], face_encoding)[0]
                    distances.append(distance)
                    matches.append(distance <= tolerancia)
                
                nome = "Desconhecido"
                confianca = 0
                
                if True in matches:
                    best_match_index = np.argmin(distances)
                    if matches[best_match_index]:
                        nome = nomes[best_match_index]
                        confianca = (1 - distances[best_match_index]) * 100
                
                rostos_detectados.append({
                    'nome': nome,
                    'confianca': round(confianca, 2),
                    'posicao': {
                        'top': top,
                        'right': right,
                        'bottom': bottom,
                        'left': left
                    }
                })
            
            return {
                'success': True,
                'message': f'{len(rostos_detectados)} rosto(s) detectado(s)',
                'rostos': rostos_detectados
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao processar imagem: {str(e)}'
            }
    
    def listar_cadastrados(self):
        """Lista todas as pessoas cadastradas"""
        encodings = self.carregar_encodings()
        return {
            'success': True,
            'total': len(encodings),
            'pessoas': sorted(list(encodings.keys()))
        }
    
    def remover_cadastro(self, nome):
        """Remove um cadastro"""
        try:
            encodings = self.carregar_encodings()
            
            if nome not in encodings:
                return {
                    'success': False,
                    'message': f'{nome} não está cadastrado'
                }
            
            # Remover encoding
            del encodings[nome]
            self.salvar_encodings(encodings)
            
            # Remover imagem
            caminho_imagem = self.pasta_rostos / f"{nome}.jpg"
            if caminho_imagem.exists():
                caminho_imagem.unlink()
            
            return {
                'success': True,
                'message': f'Cadastro de {nome} removido com sucesso'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao remover cadastro: {str(e)}'
            }


def main():
    """Função principal da API"""
    if len(sys.argv) < 2:
        print(json.dumps({
            'success': False,
            'message': 'Uso: python web_api.py <acao> [parametros]'
        }))
        sys.exit(1)
    
    api = FacialRecognitionAPI()
    acao = sys.argv[1]
    
    try:
        if acao == 'cadastrar':
            if len(sys.argv) != 4:
                resultado = {
                    'success': False,
                    'message': 'Uso: python web_api.py cadastrar <caminho_imagem> <nome>'
                }
            else:
                caminho_imagem = sys.argv[2]
                nome = sys.argv[3]
                resultado = api.cadastrar_rosto(caminho_imagem, nome)
        
        elif acao == 'reconhecer':
            if len(sys.argv) < 3:
                resultado = {
                    'success': False,
                    'message': 'Uso: python web_api.py reconhecer <caminho_imagem> [tolerancia]'
                }
            else:
                caminho_imagem = sys.argv[2]
                tolerancia = float(sys.argv[3]) if len(sys.argv) > 3 else 0.6
                resultado = api.reconhecer_rosto(caminho_imagem, tolerancia)
        
        elif acao == 'listar':
            resultado = api.listar_cadastrados()
        
        elif acao == 'remover':
            if len(sys.argv) != 3:
                resultado = {
                    'success': False,
                    'message': 'Uso: python web_api.py remover <nome>'
                }
            else:
                nome = sys.argv[2]
                resultado = api.remover_cadastro(nome)
        
        else:
            resultado = {
                'success': False,
                'message': f'Ação desconhecida: {acao}'
            }
        
        print(json.dumps(resultado))
        
    except Exception as e:
        print(json.dumps({
            'success': False,
            'message': f'Erro: {str(e)}'
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()
