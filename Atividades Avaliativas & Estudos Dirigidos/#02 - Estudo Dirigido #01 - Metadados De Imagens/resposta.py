#este programa ira extrair metadados de imagens JPEG em um diretorio especificado pelo user

import os

def extrair_info_exif_jpeg(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'rb') as arquivo:
            dados = arquivo.read()
            if dados[0:2] != b'\xFF\xD8':
                print(f'O arquivo {caminho_arquivo} não é uma imagem JPEG.')
                return None
            
            marcador_exif = dados.find(b'\xFF\xE1')
            if marcador_exif == -1:
                print(f'O arquivo {caminho_arquivo} não possui metadados EXIF.')
                return None

            tamanho_exif = (dados[marcador_exif + 4] << 8) + dados[marcador_exif + 5]
            dados_exif = dados[marcador_exif + 6:marcador_exif + 6 + tamanho_exif]

            return dados_exif
    except FileNotFoundError:
        print(f'ERRO: O arquivo {caminho_arquivo} não foi encontrado.')
    except Exception as e:
        print(f'ERRO: {e}')
    return None

def obter_info_exif(dados_exif):
    if not dados_exif:
        return None

    info_exif = {}

    tags_de_interesse = {
        0x0100: "Largura da imagem",
        0x0101: "Altura da imagem",
        0x010F: "Fabricante da câmera",
        0x0110: "Modelo da câmera",
        0x9003: "Data de captura",
        0x8825: "Informações de GPS"
    }

    posicao = 2
    try:
        while posicao < len(dados_exif):
            tag = (dados_exif[posicao] << 8) + dados_exif[posicao + 1]
            if tag in tags_de_interesse:
                tipo_dado = (dados_exif[posicao + 2] << 8) + dados_exif[posicao + 3]
                num_componentes = (dados_exif[posicao + 4] << 24) + (dados_exif[posicao + 5] << 16) + (dados_exif[posicao + 6] << 8) + dados_exif[posicao + 7]
                if tipo_dado == 2:  # String
                    valor_dado = dados_exif[posicao + 8:posicao + 8 + num_componentes]
                    info_exif[tags_de_interesse[tag]] = valor_dado.decode('utf-8')
                elif tipo_dado == 3:  # Short
                    valor_dado = (dados_exif[posicao + 8] << 8) + dados_exif[posicao + 9]
                    info_exif[tags_de_interesse[tag]] = valor_dado
                elif tipo_dado == 4:  # Long
                    valor_dado = (dados_exif[posicao + 8] << 24) + (dados_exif[posicao + 9] << 16) + (dados_exif[posicao + 10] << 8) + dados_exif[posicao + 11]
                    info_exif[tags_de_interesse[tag]] = valor_dado

            posicao += 12 + num_componentes * tipo_dado
    except Exception as e:
        print(f'ERRO ao ler metadados EXIF: {e}')

    return info_exif

def extrair_info_gps(dados_exif):
    info_gps = {}

    if 0x8825 in dados_exif:
        dados_gps = dados_exif[0x8825]
        posicao = 2
        try:
            while posicao < len(dados_gps):
                tag = (dados_gps[posicao] << 8) + dados_gps[posicao + 1]
                tipo_dado = (dados_gps[posicao + 2] << 8) + dados_gps[posicao + 3]
                num_componentes = (dados_gps[posicao + 4] << 24) + (dados_gps[posicao + 5] << 16) + (dados_gps[posicao + 6] << 8) + dados_gps[posicao + 7]
                if tipo_dado == 2:  # String
                    valor_dado = dados_gps[posicao + 8:posicao + 8 + num_componentes]
                    info_gps[tag] = valor_dado.decode('utf-8')
                posicao += 12 + num_componentes * tipo_dado
        except Exception as e:
            print(f'ERRO ao ler informações de GPS: {e}')

    return info_gps

def obter_cidade(info_gps):

    pass

def main():
    diretorio = input("Digite o caminho do diretório: ")
    cidades = {}

    try:
        for nome_arquivo in os.listdir(diretorio):
            caminho_arquivo = os.path.join(diretorio, nome_arquivo)
            if os.path.isfile(caminho_arquivo) and nome_arquivo.lower().endswith('.jpg'):
                dados_exif = extrair_info_exif_jpeg(caminho_arquivo)
                if dados_exif:
                    info_exif = obter_info_exif(dados_exif)
                    if info_exif:
                        print(f'Nome do arquivo: {nome_arquivo}')
                        for chave, valor in info_exif.items():
                            print(f'{chave}: {valor}')

                        # Processar informações de GPS
                        if 0x8825 in info_exif:
                            info_gps = extrair_info_gps(info_exif[0x8825])
                            cidade = obter_cidade(info_gps)
                            if cidade:
                                cidades[cidade] = cidades.get(cidade, 0) + 1

                        print("-" * 50)
    
        print("Cidades onde fotos foram capturadas e a quantidade de fotos em cada uma:")
        for cidade, contagem in cidades.items():
            print(f"{cidade}: {contagem} fotos")
    except Exception as e:
        print(f'ERRO: {e}')

if __name__ == "__main__":
    main()




#o codigo abaixo tem funcoes similares mas utilizando bibliotecas, foi utilizado para testes

# import os
# import json
# from exif import Image

# nomeDiretorio = input('Digite o nome do diretorio: ')
# nomeImagens = []
# imagens = []

# for f in os.listdir(nomeDiretorio):
#     if os.path.splitext(f)[1].lower() in ('.jpg', '.jpeg'):
#         nomeImagens.append(os.path.join(nomeDiretorio, f))

# for i in nomeImagens:
#     with open(i, "rb") as t:
#         nomeImagens = t
#         imagens.append(Image(nomeImagens))

# for index, image in enumerate(imagens):
#     print(f"Imagem {index}")
#     print("---------------------")
#     print(f"Fabricante da lente: {image.get('lens_make', 'Unknown')}")
#     print(f"Modelo da lente: {image.get('lens_model', 'Unknown')}")
#     print(f"Data/hora: {image.datetime_original}.{image.subsec_time_original} {image.get('offset_time', '')}")
#     print(f"Coordenadas: Latitude: {image.gps_latitude} {image.gps_latitude_ref}   Longitude: {image.gps_longitude} {image.gps_longitude_ref}\n\n")