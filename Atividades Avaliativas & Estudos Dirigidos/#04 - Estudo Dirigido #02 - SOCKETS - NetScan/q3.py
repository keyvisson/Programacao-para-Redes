# from importlib.metadata import files
# import socket

# with open('portas.txt', 'r') as file:
#     for line in file: 
#         split = line.split('/')
#         split[3] = split[3].rstrip('\n')
#         print(split)

# strHost = input('Digite o DNS: ')
# ipHost = socket.gethostbyname(strHost)

# sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# with open('portas.txt', 'r') as file:
#     for line in file: 
#         try:
#             split = line.split('/')
#             split[0] = int(split[0])
#             split[3] = split[3].rstrip('\n')
#             resultadoTCP = sockTCP.connect((ipHost,split[0]))
#             if resultadoTCP == 0:
#                 status = 'Aberta'
#                 print(status)
#             else:
#                 status = 'Fechada' 
#                 print(status)
#         except TimeoutError:
#             status = 'Fechada'
#             print(status)
    
# sockTCP.close()
# sockUDP.close()

import socket

strHost = input('Digite o DNS: ')
ipHost = socket.gethostbyname(strHost)

sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True: 
    try:
        resultadoTCP = sockTCP.connect((ipHost,80))
        resultadoUDP = sockUDP.connect((ipHost,20))
        if resultadoTCP == 0:
            print ("Porta está aberto")
        else:
            print ("Porta não está aberto") 

    except TimeoutError:
        print ("Porta não está aberto") 
        break

sockTCP.close()
sockUDP.close()