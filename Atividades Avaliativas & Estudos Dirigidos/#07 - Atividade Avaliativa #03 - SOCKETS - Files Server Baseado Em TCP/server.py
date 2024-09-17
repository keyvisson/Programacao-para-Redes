import socket
import os

SERVER = '127.0.0.1'
PORT = 31435

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((SERVER, PORT))
sock.listen(1)

print('Esperando pedidos...')

def handle_download(conn, filename):
    try:
        file_size = os.path.getsize(filename)
        conn.sendall(str(file_size).encode('utf-8'))

        print(f"Abrindo o arquivo {filename}...")
        with open(filename, 'rb') as fd:
            conteudo_arq = fd.read(4096)
            total_packets = (file_size // 4096) + 1
            packet_count = 0

            while conteudo_arq:
                packet_count += 1
                print(f'Pacote {packet_count}/{total_packets}: Enviando {len(conteudo_arq)} bytes...')
                conn.sendall(conteudo_arq)
                conteudo_arq = fd.read(4096)

        print(f"Arquivo {filename} enviado com sucesso.")

    except Exception as e:
        print(f"Erro ao processar o pedido: {e}")

def handle_upload(conn, filename):
    try:
        file_size = int(conn.recv(4096).decode('utf-8'))
        print(f"Tamanho do arquivo a ser recebido: {file_size} bytes")

        with open(filename, 'wb') as fd:
            received_size = 0
            total_packets = (file_size // 4096) + 1
            packet_count = 0

            while received_size < file_size:
                data = conn.recv(4096)
                packet_count += 1
                if not data:
                    break

                received_size += len(data)
                print(f'Pacote {packet_count}/{total_packets}: Recebidos {len(data)} bytes')
                fd.write(data)

        print('Recepção do arquivo concluída.')

    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

while True:
    conn, addr = sock.accept()
    print(f'Conexão estabelecida com {addr}')
    
    try:
        msg = conn.recv(4096).decode('utf-8')
        command, filename = msg.split(':', 1)

        if command == 'DOWNLOAD':
            handle_download(conn, filename)
        elif command == 'UPLOAD':
            if os.path.isfile(filename):
                new_name = input(f"Arquivo {filename} já existe. Digite um novo nome: ")
                filename = new_name

            handle_upload(conn, filename)
        else:
            print("Comando inválido")

    finally:
        conn.close()

sock.close()
