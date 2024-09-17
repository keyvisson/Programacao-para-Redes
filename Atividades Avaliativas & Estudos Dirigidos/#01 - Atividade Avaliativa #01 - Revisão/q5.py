
arquivo_entrada = input("Digite o nome do arquivo inicial: ")
palavra_passe = input('digite a palavra passe: ')
arquivo_saida = input('digite o nome do arquivo de saida: ')


def aplicar_cifra_xor(caminho_arquivo_entrada, senha, caminho_arquivo_saida):
    try:
        with open(caminho_arquivo_entrada, 'rb') as arquivo_entrada:
            conteudo_entrada = arquivo_entrada.read()
        senha_bytes = senha.encode('utf-8')

        conteudo_transformado = []

        # Aplicação da cifra XOR
        for posicao, valor_byte in enumerate(conteudo_entrada):
            posicao_senha = posicao % len(senha_bytes)
            byte_resultante = valor_byte ^ senha_bytes[posicao_senha]
            conteudo_transformado.append(byte_resultante)

        with open(caminho_arquivo_saida, 'xb') as arquivo_saida:
            arquivo_saida.write(bytes(conteudo_transformado))

        print("Processo de cifragem concluído com sucesso!")

    except FileNotFoundError:
        print("O arquivo especificado para entrada não foi localizado.")
    except FileExistsError:
        print("Já existe um arquivo com esse nome de saída. Por favor, escolha outro nome.")
    except Exception as excecao:
        print(f"Ocorreu um erro durante o processo: {excecao}")

aplicar_cifra_xor(arquivo_entrada, palavra_passe, arquivo_saida)