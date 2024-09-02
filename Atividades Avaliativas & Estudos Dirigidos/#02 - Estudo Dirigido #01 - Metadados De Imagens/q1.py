#este programa ira extrair metadados de imagens JPEG em um diretorio especificado pelo user
import os
from exif import Image

nomeDiretorio = input('Digite o nome do diretorio: ')
nomeImagens = []
imagens = []

for f in os.listdir(nomeDiretorio):
    if os.path.splitext(f)[1].lower() in ('.jpg', '.jpeg'):
        nomeImagens.append(os.path.join(nomeDiretorio, f))

for i in nomeImagens:
    with open(i, "rb") as t:
        nomeImagens = t
        imagens.append(Image(nomeImagens))

for index, image in enumerate(imagens):
    print(f"Imagem {index}")
    print("---------------------")
    print(f"Fabricante da lente: {image.get('lens_make', 'Unknown')}")
    print(f"Modelo da lente: {image.get('lens_model', 'Unknown')}")
    print(f"Data/hora: {image.datetime_original}.{image.subsec_time_original} {image.get('offset_time', '')}")
    print(f"Coordenadas: Latitude: {image.gps_latitude} {image.gps_latitude_ref}   Longitude: {image.gps_longitude} {image.gps_longitude_ref}\n\n")