import socket
import sys
import logging
import json
from FS_MSG import FS_Msg


cont = {
        "FILE1": [
            128,
            [
                0,0,0,0,0            ]
        ],
        "FILE2": [
            0,
            [0,0,0,0,0]
        ],
        "FILE3": [
            512,
            [0,0,0,0,0]
        ]
    }
    



class FS_Node:


    def __init__(self, port=9090):

        # self.startTime = datetime.now()
        self.soc = socket.socket(socket.AF_INET,     # Familia de enderecos ipv4
                            socket.SOCK_STREAM)  # Connection-Oriented (TCP PROTOCOL)

        self.hostname = socket.gethostname()
        self.endereco = socket.gethostbyname(self.hostname)
        self.porta = port
        
        self.soc.connect((self.endereco, self.porta))
        
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

        message = msg.toText()
        

        try:
            print(f"Sending: {message}")
            self.soc.sendall(message.encode('utf-8'))
        except:
            print("Impossivel Conectar")
            return
            
        if msg.MSG_TYPE == "ASK FILE":

            message = self.soc.recv(1024)
            line = message.decode('utf-8')
            print(line)
        
        else: 
            pass
        

        print("CLOSING SOCKET")

    def sendTcpMsgFromFile(self,filePath):

        #using replace() everything is returned in one line.
        with open(filePath, 'r') as file:
            msg = file.read()# .replace('\n',' ')
        
        try:

            message = FS_Msg()
            message.read_message(msg)
            print(message)
            self.soc.sendall(msg.encode('utf-8'))
        except:
            print("Impossivel Conectar")
            return
            
        if message.MSG_TYPE == "ASK FILE":

            msg = self.soc.recv(1024)
            line = msg.decode('utf-8')
            print(line)
        
        else: 
            pass
        

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
    def createMsg(self,MSG_TYPE,BODY={}):
                    
        if MSG_TYPE == "UPDATE NODE":
            BODY = self.contents

        msg =  FS_Msg(self.hostname,self.endereco,MSG_TYPE,BODY)
        
        return msg
    
    def addFile(self,filePath):
        
        # TODO only supports UTF-8 type files 
        with open(filePath, 'r') as file:
            data = file.read()# .replace('\n',' ')
        
        fragSize = 8
        
        fileSize = len(data)
        
        numFrags = int(fileSize / fragSize)
        
        lastFragSize = fileSize - (numFrags * fragSize)
        
        print(lastFragSize)
               
        
        self.contents[filePath] = [fileSize,[True] * numFrags]

def main():

    
    node = FS_Node(9090) # TODO port in argv
    node.addFile("askFile.msg")
    msg = node.createMsg("UPDATE NODE")
    node.sendTcpMsg(msg)

    
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO)
    
    
    while True:
        print("Node > ",end="")
        
        option = input()
        if option == "update":
            
            msg = node.createMsg("UPDATE NODE")
            node.sendTcpMsg(msg)
            
        elif option == "ask":
            file = input()

            BODY = {file : "NONE"}
            msg = node.createMsg("ASK FILE",BODY)
            node.sendTcpMsg(msg)
            
        elif option == "add":
            print("Insert File > ",end="")
            filePath = input()
            node.addFile(filePath)

        elif option == "list":
        
            print(json.dumps(node.contents, indent=4))

            
        elif option == "exit":
        
            node.soc.close()
            logging.info("Terminate normal execution")
            break
        
        else:
            logging.info("Unknown Option")        
            

if __name__ == "__main__":
    main()
