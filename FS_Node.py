import socket
import sys

messageUpdate = """
# NODE_ID 
SENDER_ID=LegionGusto;
# NODE_IP 
SENDER_IP=127.0.0.1;
# HEADER
MSG_TYPE=UPDATE NODE;
# BODY
BODY={
FILE1 128 [00000],
FILE2 0 [11111],
FILE3 512 [10110]
};"""

messageEnd = """
# NODE_ID 
SENDER_ID=LegionGusto;
# NODE_IP 
SENDER_IP=127.0.0.1;
# HEADER
MSG_TYPE=END TRACKER;
"""





class FS_Node:

    def __init__(self, port=9090):

        # self.startTime = datetime.now()

        self.hostname = socket.gethostname()
        self.endereco = socket.gethostbyname(self.hostname)
        self.porta = port

    def updateEntrys(self):

        soc = socket.socket(socket.AF_INET,     # Familia de enderecos ipv4
                            socket.SOCK_STREAM)  # Connection-Oriented (TCP PROTOCOL)

        try:
            soc.connect((self.endereco, self.porta))
            soc.sendall(message.encode('utf-8'))
        except:
            print("Impossivel Conectar")

        soc.close()

        print("CLOSING SOCKET")
    
    def sendTcpMsg(self,msg):

        soc = socket.socket(socket.AF_INET,     # Familia de enderecos ipv4
                            socket.SOCK_STREAM)  # Connection-Oriented (TCP PROTOCOL)
        try:
            soc.connect((self.endereco, self.porta))
            print(msg)
            
            soc.sendall(msg.encode('utf-8'))
        except:
            print("Impossivel Conectar")
        
        soc.close()

        print("CLOSING SOCKET")

    def sendTcpMsgFromFile(self,file):

        #using replace() everything is returned in one line.
        with open(sys.argv[2], 'r') as file:
            msg = file.read()# .replace('\n',' ')

        soc = socket.socket(socket.AF_INET,     # Familia de enderecos ipv4
                            socket.SOCK_STREAM)  # Connection-Oriented (TCP PROTOCOL)
        try:
            soc.connect((self.endereco, self.porta))
            print(msg)
            
            soc.sendall(msg.encode('utf-8'))
        except:
            print("Impossivel Conectar")
        
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
    
    
    if sys.argv[1] == "FILES LIST":
        node.askForList()
    elif sys.argv[1] == "UPDATE NODE":
        node.sendTcpMsgFromFile(sys.argv[2])
    else:
        print("ERROR: Unknown command")


if __name__ == "__main__":
    main()
