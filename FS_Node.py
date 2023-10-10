import socket

class FS_Node:

    def __init__(self, port = 9090):

        # self.startTime = datetime.now()




        self.hostname = socket.gethostname()
        self.endereco = socket.gethostbyname(self.hostname)  
        self.porta = port

    def startTCP(self, sendAdress = "127.0.0.1"):
        
        soc = socket.socket(socket.AF_INET,     # Familia de enderecos ipv4
                          socket.SOCK_STREAM)  # Connection-Oriented (TCP PROTOCOL)

        soc.connect((sendAdress, self.porta))

        try:
            
            soc.sendall("REGIST FS_NODE".encode('utf-8'))

        except:
            debug("Impossivel Conectar")
        
        # msg = soc.recv(1024)
        # line = msg.decode('utf-8')

        soc.close()
            
        print("CLOSING SOCKET")    

        
def main():
    
    node = FS_Node()
    node.startTCP() 
    
if __name__ == "__main__":
    main()