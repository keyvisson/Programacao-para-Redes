import socket, os

SERVER = '127.0.0.1'
PORT   = 31435

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER, PORT))

print ('Esperando pedidos .... ')

while True:
    msg, addr = sock.recvfrom(4096)
    print(f"Recebido pedido de {addr}: {msg.decode('utf-8')}")
    strNomeArq = msg.decode('utf-8')

    try:
        file_size = os.path.getsize(strNomeArq)
        sock.sendto(str(file_size).encode('utf-8'), addr)

        print(f"Abrindo o arquivo {strNomeArq}...")
        fd = open(strNomeArq, 'rb')
        conteudo_arq = fd.read(4096)
        print(f"Conteúdo lido: {conteudo_arq[:50]}...")

        while conteudo_arq:
            print(f'Enviando {len(conteudo_arq)} bytes ...')
            sock.sendto(conteudo_arq, addr)
            conteudo_arq = fd.read(4096)

        print(f"Arquivo {strNomeArq} enviado com sucesso.")
        

    except Exception as e:
        print(f"Erro ao processar o pedido: {e}")
        sock.sendto(b"Erro ao processar o arquivo", addr)
    
    finally:
        fd.close()
        sock.close()
        break