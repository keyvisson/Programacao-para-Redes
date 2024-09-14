import socket, sys

# --------------------------------------------------
# Documentação Protocolo HTTP
# https://datatracker.ietf.org/doc/html/rfc2616
# --------------------------------------------------

# --------------------------------------------------
PORT        = 80
CODE_PAGE   = 'utf-8'
BUFFER_SIZE = 1024
# --------------------------------------------------

#definindo a funcao para criar o dicionario
def criar_dict(entrada):
#uso do strip e split para remover possíveis espaços em branco no início e no fim da entrada e separar pelo nova linha no final
    resposta = entrada.strip().split('\n')
#definindo dicionario
    dicionario = {"status": resposta[0].strip()}
    for linha in resposta[1:]:
        if ':' in linha:
            key, value = map(str.strip, linha.split(':', 1))
            dicionario[key] = value
    return dicionario

host = input('\nInforme o nome do HOST ou URL do site: ')

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    tcp_socket.connect((host, PORT))
except:
    print(f'\nERRO.... {sys.exc_info()[0]}')
else:
    requisicao = f'HEAD / HTTP/1.1\r\nHost: {host}\r\nAccept: text/html\r\n\r\n'
    try:
        tcp_socket.sendall(requisicao.encode(CODE_PAGE))
    except:
        print(f'\nERRO.... {sys.exc_info()[0]}')
    else:
        resposta = tcp_socket.recv(BUFFER_SIZE).decode(CODE_PAGE)
        #dicionario  sera criado de acordo com a reposta do tcp_socket.recv
        dicionario = criar_dict(resposta)
        print('-'*50)
        #loop para printar todas as chaves e valores no dicionario criado com a reposta
        for key, value in dicionario.items():
            print(f"{key}: {value}")
    tcp_socket.close()
