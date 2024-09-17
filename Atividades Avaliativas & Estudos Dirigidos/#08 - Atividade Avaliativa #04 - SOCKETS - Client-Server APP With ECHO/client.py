import socket
from socket_constants import *

def main():
    # Criando o socket TCP
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Ligando o socket a porta
    tcp_socket.connect((HOST_SERVER, SOCKET_PORT))

    while True:
        mensagem = input('\nDigite um dos seguintes comandos: \n "HORA" (Para saber a hora atual do servidor), \n "ROTA <url>" (Para saber a rota ate a URL informada.)) ou \n "CRIPTO <string>%<chave>" (para encerrar a conexao com o servidor): ')

        # if mensagem.lower() == 'SAIR':
        #     print("Conexao encerrado forcadamente.")
        #     break

        if mensagem:
            mensagem = mensagem.encode(CODE_PAGE)
            tcp_socket.send(mensagem)

            dado_recebido = tcp_socket.recv(BUFFER_SIZE)
            mensagem_recebida = dado_recebido.decode(CODE_PAGE)
            print(f'Resposta Recebida: {mensagem_recebida}')

    tcp_socket.close()

if __name__ == '__main__':
    main()
