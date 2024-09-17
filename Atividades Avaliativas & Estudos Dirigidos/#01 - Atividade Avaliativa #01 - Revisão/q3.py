import hashlib
import struct
import time

def procurar_nonce(dados_para_hash, bits_para_zero):

    for numero in range(2**32):

        conteudo = struct.pack('<Q', numero) + dados_para_hash

        resultado = hashlib.sha256(conteudo).digest()

        if int.from_bytes(resultado[:bits_para_zero // 8], byteorder='big') == 0:
            duracao = time.time() - inicio
            return numero, duracao

    return None, None

bits_iniciais = int(input('Informe a quantidade de bits zero: '))
informacoes = input('Forneça uma mensagem para verificação: ').encode('utf-8')
inicio = time.time()
nonce_valido, tempo_total = procurar_nonce(informacoes, bits_iniciais)

if nonce_valido is not None:
    print(nonce_valido, tempo_total)
else:
    print('Nenhum NONCE foi identificado...')