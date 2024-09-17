import socket
import threading
from socket_constants import *
from funcoes_socket import hora_atual, trace_route, vigenere

clientes_conectados = {}  
comandos_cliente = {}   

def processar_comandos(comando, endereco_cliente):
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
    elif comando == 'LISTAR_CLIENTES':
        return '\n'.join([f'{ip}:{porta}' for ip, porta in clientes_conectados.values()])
    elif comando == 'LISTAR_COMANDOS':
        return '\n'.join(comandos_cliente.get(endereco_cliente, []))
    else:
        return 'Comando não reconhecido.'

def gerenciar_cliente(conexao, endereco_cliente):
    print(f'Conectado por: {endereco_cliente}')
    clientes_conectados[endereco_cliente] = endereco_cliente

    while True:
        mensagem = conexao.recv(BUFFER_SIZE)
        if not mensagem:
            break
        
        mensagem_decodificada = mensagem.decode(CODE_PAGE)
        print(f'{endereco_cliente} enviou: {mensagem_decodificada}')

        if endereco_cliente not in comandos_cliente:
            comandos_cliente[endereco_cliente] = []
        comandos_cliente[endereco_cliente].append(mensagem_decodificada)

        resposta = processar_comandos(mensagem_decodificada, endereco_cliente)
        conexao.send(resposta.encode(CODE_PAGE))
    
    print(f'Finalizando Conexão do Cliente {endereco_cliente}')
    del clientes_conectados[endereco_cliente]
    conexao.close()

def main():
    print('Recebendo Mensagens...\n\n')

    # Criando o socket TCP
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Ligando o socket a porta
    tcp_socket.bind((HOST_SERVER, SOCKET_PORT))

    # Máximo de conexões enfileiradas
    tcp_socket.listen(MAX_LISTEN)

    while True:
        conexao, endereco_cliente = tcp_socket.accept()
        cliente_thread = threading.Thread(target=gerenciar_cliente, args=(conexao, endereco_cliente))
        cliente_thread.start()

if __name__ == '__main__':
    main()