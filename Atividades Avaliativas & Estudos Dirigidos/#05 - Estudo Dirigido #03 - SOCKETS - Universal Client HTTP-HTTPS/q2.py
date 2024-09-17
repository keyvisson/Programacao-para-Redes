import socket, sys

# --------------------------------------------------
# Documentação Protocolo HTTP
# https://datatracker.ietf.org/doc/html/rfc2616
# --------------------------------------------------

# --------------------------------------------------
PORT = 80  
CODE_PAGE   = 'utf-8'
BUFFER_SIZE = 1024
# --------------------------------------------------

host = input('\nInforme o nome do HOST ou URL do site: ')

# Remove o prefixo "http://"
if host.startswith('http://'):
    host = host[7:]
# Remove o prefixo "https://"
if host.startswith('https://'):
    host = host[8:]

socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_tcp.settimeout(10)

try:
    socket_tcp.connect((host, PORT))
except socket.timeout:
    print('\nERRO.... Tempo de conexão esgotado.')
except socket.gaierror:
    print('\nERRO.... Nome do host não pôde ser resolvido.')

else:
    requisicao = f'GET / HTTP/1.1\r\nHost: {host}\r\nAccept: text/html\r\nConnection: close\r\n\r\n'

    try:
        socket_tcp.sendall(requisicao.encode(CODE_PAGE))
    except Exception as e:
        print(f'\nERRO.... {e}')
    else:
        resposta_completa = b''
        while True:
            try:
                resposta = socket_tcp.recv(BUFFER_SIZE)
                if not resposta:
                    break
                resposta_completa += resposta
            except socket.timeout:
                print('\nERRO.... Tempo esgotado ao receber dados.')
                break

        socket_tcp.close()
    
        if b'\r\n\r\n' in resposta_completa:
            cabecalho, corpo = resposta_completa.split(b'\r\n\r\n', 1)
        else:
            cabecalho = resposta_completa
            corpo = b''

        tamanho_conteudo = None
        for linha in cabecalho.decode(CODE_PAGE, errors='ignore').split('\r\n'):
            if linha.lower().startswith('content-length:'):
                tamanho_conteudo = int(linha.split(':')[1].strip())
                break
        
        if tamanho_conteudo is not None:
            corpo = corpo[:tamanho_conteudo]
        
        with open('output.html', 'wb') as arquivo:
            arquivo.write(corpo)
        
        print('-'*50)
        print('Resposta salva em "output.html".')
        print('-'*50)