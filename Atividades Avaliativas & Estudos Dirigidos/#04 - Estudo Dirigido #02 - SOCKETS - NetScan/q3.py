import socket

strHost = input('Digite o DNS: ')
ipHost = socket.gethostbyname(strHost)

list = []
counter = 0


with open('portas.txt', 'r') as file:
    for line in file: 
        split = line.split('/')
        split[0] = int(split[0])
        split[3] = split[3].rstrip('\n')
        list.append(split)

for i in list:

    sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockTCP.settimeout(1)
    resultadoTCP = sockTCP.connect_ex((ipHost,list[counter][0]))
    if resultadoTCP == 0:
        statusTCP = 'Aberta'
    else:
        statusTCP = 'Fechada' 
    print(f"\nPorta: {list[counter][0]} Protocolo: {list[counter][1]} Descrição: {list[counter][2]} Status para TCP: {statusTCP}\n")
    sockTCP.close()


    sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    resultadoUDP = sockUDP.connect_ex((ipHost,list[counter][0]))
    if resultadoUDP == 0:
        statusUDP = 'Aberta'
    else:
        statusUDP = 'Fechada' 
    print(f"\nPorta: {list[counter][0]} Protocolo: {list[counter][1]} Descrição: {list[counter][2]} Status para UDP: {statusUDP}\n")
    sockUDP.close()
    counter += 1