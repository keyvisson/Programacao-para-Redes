import socket
from socket_constants import *
from funcoes_socket import hora_atual, trace_route, vigenere

def processar_comandos(comando):
    if comando == 'HORA':
        return hora_atual()
    elif comando.startswith('ROTA '):
        url = comando.split(' ', 1)[1]
        return trace_route(url)
    elif comando.startswith('CRIPTO '):
        try:
            msg, key = comando.split('%')
            return vigenere(msg.split(' ', 1)[1], key)
        except ValueError:
            return 'Formato inválido para comando de criptografia.'
    else:
        return 'Comando não reconhecido.'

def main():
    print('Recebendo Mensagens...\n\n')

    # Criando o socket TCP
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Ligando o socket a porta
    tcp_socket.bind((HOST_SERVER, SOCKET_PORT))

    # Máximo de conexões enfileiradas
    tcp_socket.listen(MAX_LISTEN)

    while True:
        conexao, cliente = tcp_socket.accept()
        print('Conectado por: ', cliente)
        while True:
            mensagem = conexao.recv(BUFFER_SIZE)
            if not mensagem:
                break
            mensagem_decodificada = mensagem.decode(CODE_PAGE)
            print(cliente, mensagem_decodificada)
            
            resposta = processar_comandos(mensagem_decodificada)
            conexao.send(resposta.encode(CODE_PAGE))

        print('Finalizando Conexão do Cliente ', cliente)
        conexao.close()

if __name__ == '__main__':
    main()
