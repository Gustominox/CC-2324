import socket
import sys
from FS_MSG import FS_Msg


class FS_Node:


    def __init__(self, port=9090):

        # self.startTime = datetime.now()

        self.hostname = socket.gethostname()
        self.endereco = socket.gethostbyname(self.hostname)
        self.porta = port
        self.nodeId = f"{self.endereco}"
        self.contents={}

    def adicionaFicheiroCompleto(self,file): #Adicionar o SHA-256 aqui
        self.contents[file]=file
        self.contents[file]#adicionar aqui os 20 fragmentos a TRUE
        
    def updateEntrys(self):

        soc = socket.socket(socket.AF_INET,     # Familia de enderecos ipv4
                            socket.SOCK_STREAM)  # Connection-Oriented (TCP PROTOCOL)
        
        try:
            soc.connect((self.endereco, self.porta))
            soc.sendall(message.encode('utf-8'))
        except:
            print("Impossivel Conectar")
            return
        soc.close()

        print("CLOSING SOCKET")
    
    def sendTcpMsg(self,msg):

        soc = socket.socket(socket.AF_INET,     # Familia de enderecos ipv4
                            socket.SOCK_STREAM)  # Connection-Oriented (TCP PROTOCOL)
        try:
            soc.connect((self.endereco, self.porta))
            
            soc.sendall(msg.encode('utf-8'))
        except:
            print("Impossivel Conectar")
        
        soc.close()

        print("CLOSING SOCKET")

    def sendTcpMsgFromFile(self,file):

        #using replace() everything is returned in one line.
        with open(sys.argv[1], 'r') as file:
            msg = file.read()# .replace('\n',' ')

        soc = socket.socket(socket.AF_INET,     # Familia de enderecos ipv4
                            socket.SOCK_STREAM)  # Connection-Oriented (TCP PROTOCOL)
        try:
            soc.connect((self.endereco, self.porta))
            message = FS_Msg()
            message.read_message(msg)
         
            soc.sendall(msg.encode('utf-8'))
        except:
            print("Impossivel Conectar")
            return
            
        if message.MSG_TYPE == "ASK FILE":

            msg = soc.recv(1024)
            line = msg.decode('utf-8')
            print(line)
        
        else: 
            pass
        
        soc.close()

        print("CLOSING SOCKET")
    
    def askForList(self):
        soc = socket.socket(socket.AF_INET,     # Familia de enderecos ipv4
                            socket.SOCK_STREAM)  # Connection-Oriented (TCP PROTOCOL)

        try:
            soc.connect((self.endereco, self.porta))
            soc.sendall("FILES LIST".encode('utf-8'))
        except:
            print("Impossivel Conectar")

        msg = soc.recv(1024)
        line = msg.decode('utf-8')
        print(line)
        soc.close()

        print("CLOSING SOCKET")


def main():

    
    node = FS_Node()
    
    
    node.sendTcpMsgFromFile(sys.argv[1])
    

if __name__ == "__main__":
    main()
