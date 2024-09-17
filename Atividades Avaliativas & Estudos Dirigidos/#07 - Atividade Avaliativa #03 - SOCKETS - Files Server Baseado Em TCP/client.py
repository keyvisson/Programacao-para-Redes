#OBS: ao fazer upload de arquivo do client para o server o formato do arquivo nao é enviado corretamente. ainda é necessario ajuste para funcionar perfeitamente.

import socket
import os

SERVER = '127.0.0.1'
PORT = 31435

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER, PORT))

def download_file():
    strNomeArq = input('Nome do arquivo a fazer download: ')
    sock.sendall(f'DOWNLOAD:{strNomeArq}'.encode('utf-8'))

    try:
        file_size = int(sock.recv(4096).decode('utf-8'))
        print(f"Tamanho do arquivo recebido: {file_size} bytes")

        fd = open(strNomeArq, 'wb')
        received_size = 0
        total_packets = (file_size // 4096) + 1  # total number of packets
        packet_count = 0

        while received_size < file_size:
            data = sock.recv(4096)
            packet_count += 1
            if not data:
                break

            received_size += len(data)
            print(f'Pacote {packet_count}/{total_packets}: Recebi {len(data)} bytes')
            fd.write(data)

        print('Recepção do arquivo concluída.')

    except Exception as e:
        print(f'Erro: {e}')

    finally:
        fd.close()

def upload_file():
    strNomeArq = input('Nome do arquivo a fazer upload: ')
    if not os.path.isfile(strNomeArq):
        print('Arquivo não encontrado.')
        return

    new_name = input('Nome para salvar no servidor (deixe em branco para manter o mesmo): ')
    if not new_name:
        new_name = strNomeArq

    sock.sendall(f'UPLOAD:{new_name}'.encode('utf-8'))

    try:
        file_size = os.path.getsize(strNomeArq)
        sock.sendall(str(file_size).encode('utf-8'))
        print(f"Tamanho do arquivo a ser enviado: {file_size} bytes")

        fd = open(strNomeArq, 'rb')
        sent_size = 0
        total_packets = (file_size // 4096) + 1  # total number of packets
        packet_count = 0

        while True:
            data = fd.read(4096)
            if not data:
                break

            packet_count += 1
            sock.sendall(data)
            sent_size += len(data)
            print(f'Pacote {packet_count}/{total_packets}: Enviados {len(data)} bytes')

        print('Envio do arquivo concluído.')

    except Exception as e:
        print(f'Erro: {e}')

    finally:
        fd.close()

while True:
    action = input('Digite "upload" para enviar um arquivo ou "download" para receber um arquivo (ou "exit" para sair): ').strip().lower()
    if action == 'download':
        download_file()
    elif action == 'upload':
        upload_file()
    elif action == 'exit':
        break
    else:
        print('Comando inválido.')

sock.close()
