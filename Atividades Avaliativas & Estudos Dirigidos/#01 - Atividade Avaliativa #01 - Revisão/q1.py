#este programa irá ler 3 valoress e criar lista com essses valores

#importando bibliotecas random e os para gerar numeros aleatorios e salvar na diretorio atual
import random
import os

#definindo uma lista vazia para adicionar o elementos posteriormente
lista_gerada = []

#loop para solicitar info ao user e processar excessao caso haja
while True:
    try:
        quantidade = int(input('Digite a quantidade de números que deseja na lista: '))
        valor_minimo = int(input('Digite o menor valor que haverá na lista: '))
        valor_maximo = int(input('Digite o maior valor que haverá na lista: '))

        if quantidade or valor_minimo or valor_maximo == int(quantidade):
            break
    except ValueError:
        print('Um dos números digitados não é inteiro. Por favor, digite novamente: ')

#funcao para gerar a lista com numero aleatorios
def gerar_lista(quantidade, valor_minimo, valor_maximo):
    for i in range(quantidade):
        lista_gerada.append(random.randint(valor_minimo, valor_maximo))
    
    if len(lista_gerada) == quantidade:
        return True, lista_gerada
    else:
        return False, None

gerar_lista(quantidade, valor_minimo, valor_maximo)

#funcao para salvar a lista no diretorio do arquivo .py em execucao
def salvar_lista(nome_lista, nome_arquivo):
    diretorio_atual = os.path.dirname(__file__)
    diretorio_destino = os.path.join(diretorio_atual, nome_arquivo)

    with open(diretorio_destino, 'w') as f:
        for i in nome_lista:
            f.write(str(i) + '\n')

    with open(diretorio_destino, 'r') as f:
        lista_teste = []
        for l in f:
            lista_teste.append(int(l.strip()))

    if lista_teste == lista_gerada:
        return True, print('A lista foi salva corretamente!')
    else:
        return False, print('A lista não foi salva corretamente!')

salvar_lista(lista_gerada, 'lista_gerada')