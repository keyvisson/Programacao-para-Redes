import socket

strHost = input('Digite o DNS: ')
ipHost = socket.gethostbyname(strHost)

sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True: 
    try:
        resultadoTCP = sockTCP.connect((ipHost,7))
        resultadoUDP = sockUDP.connect((ipHost,7))
        if resultadoTCP == 0:
            print ("Porta está aberto")
        else:
            print ("Porta não está aberto") 

    except TimeoutError:
        print ("Porta não está aberto") 
        break

# while True:
#     try:
#         if resultadoTCP == 0:
#             print ("Porta está aberto")
#         else:
#             print ("Porta não está aberto")
#     except TimeoutError():
#         break

sockTCP.close()
sockUDP.close()