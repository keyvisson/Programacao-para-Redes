import socket
from socket_constants import *
import threading

def receber_respostas(tcp_socket):
    while True:
        dado_recebido = tcp_socket.recv(BUFFER_SIZE)
        if not dado_recebido:
            break
        mensagem_recebida = dado_recebido.decode(CODE_PAGE)
        print(f'\nResposta Recebida: {mensagem_recebida}')

def main():
    # Criando o socket TCP
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Ligando o socket a porta
    tcp_socket.connect((HOST_SERVER, SOCKET_PORT))

    # Inicia thread para receber respostas do servidor
    receber_thread = threading.Thread(target=receber_respostas, args=(tcp_socket,))
    receber_thread.start()

    while True:
        mensagem = input('\nDigite um dos seguintes comandos: \n "HORA" (Para saber a hora atual do servidor), \n "ROTA <url>" (Para saber a rota ate a URL informada), \n "CRIPTO <string>%<chave>" (para criptografar a string), \n "LISTAR_CLIENTES" (para listar clientes conectados), \n "LISTAR_COMANDOS" (para listar os comandos enviados) ou \n "SAIR" (para encerrar a conexão): ')

        if mensagem:
            if mensagem.upper() == 'SAIR':
                break

            mensagem = mensagem.encode(CODE_PAGE)
            tcp_socket.send(mensagem)
    
    tcp_socket.close()

if __name__ == '__main__':
    main()

