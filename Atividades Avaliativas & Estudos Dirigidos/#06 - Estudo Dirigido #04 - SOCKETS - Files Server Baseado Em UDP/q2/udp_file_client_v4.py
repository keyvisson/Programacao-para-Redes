import socket

SERVER = '127.0.0.1'
PORT   = 31435

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5) 

while True:
    strNomeArq = input('Nome do arquivo a fazer download: ')
    sock.sendto(strNomeArq.encode('utf-8'), (SERVER, PORT))

    try:
        data, addr = sock.recvfrom(4096)
        file_size = int(data.decode('utf-8'))
        print(f"Tamanho do arquivo recebido: {file_size} bytes")
        
        fd = open(strNomeArq, 'wb')
        received_size = 0 

        while received_size < file_size:
            data, addr = sock.recvfrom(4096)

            if not data: 
                break

            received_size += len(data)
            print (f'Recebi {len(data) / received_size} bytes')
            fd.write(data)
        print('Recepção do arquivo concluída.')

    except socket.timeout:
        print('Tempo de espera esgotado')

    finally:
        fd.close()
        sock.close()
        break