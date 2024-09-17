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

url = input("Digite a URL completa da imagem: ")

def separar_url(url):
#remover o protocolo (http:// ou https://)
    if url.startswith('http://'):
        url = url[7:]
    elif url.startswith('https://'):
        url = url[8:]
    
#separar o host e o caminho da imagem
    partes = url.split('/', 1)
    servidor = partes[0]
    caminho_imagem = '/' + partes[1] if len(partes) > 1 else '/'
    return servidor, caminho_imagem

def obter_nome_arquivo(url):
    return url.split('/')[-1]

def baixar_imagem(url):
    servidor, caminho_imagem = separar_url(url)
    nome_arquivo = obter_nome_arquivo(url)
    print(f"Servidor: {servidor}")
    print(f"Imagem: {caminho_imagem}")
    print(f"Nome do arquivo: {nome_arquivo}")

    requisicao_url = f'GET {caminho_imagem} HTTP/1.1\r\nHOST: {servidor}\r\n\r\n'
    PORT = 80
    BUFFER_SIZE = 1024

    socket_conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_conexao.connect((servidor, PORT))
    socket_conexao.sendall(requisicao_url.encode())

#ler o cabecalho para encontrar o tamanho da imagem
    resposta = b""
    while b"\r\n\r\n" not in resposta:
        resposta += socket_conexao.recv(BUFFER_SIZE)
    
    cabecalho, dados = resposta.split(b"\r\n\r\n", 1)
    cabecalhos = cabecalho.decode(CODE_PAGE).splitlines()
    tamanho_conteudo = 0
    for linha in cabecalhos:
        if linha.startswith('Content-Length:'):
            tamanho_conteudo = int(linha.split(':')[1].strip())
            break
        
    with open(nome_arquivo, 'wb') as arquivo_imagem:
        arquivo_imagem.write(dados)

#continuar recebendo dados até que todo o conteúdo seja baixado
        while len(dados) < tamanho_conteudo:
            dados = socket_conexao.recv(BUFFER_SIZE)
            arquivo_imagem.write(dados)

    print(f"Download concluído: {nome_arquivo}")
    socket_conexao.close()

baixar_imagem(url)
