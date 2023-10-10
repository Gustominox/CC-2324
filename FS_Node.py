import socket
import sys
class FS_Node:

    def __init__(self, port = 9090):

        # self.startTime = datetime.now()




        self.hostname = socket.gethostname()
        self.endereco = socket.gethostbyname(self.hostname)  
        self.porta = port

    def updateEntrys(self, sendAdress = "127.0.0.1"):
        
        soc = socket.socket(socket.AF_INET,     # Familia de enderecos ipv4
                          socket.SOCK_STREAM)  # Connection-Oriented (TCP PROTOCOL)

        soc.connect((sendAdress, self.porta))

        try:
            soc.sendall(sys.argv[1].encode('utf-8'))
        except:
            print("Impossivel Conectar")
        
        # msg = soc.recv(1024)
        # line = msg.decode('utf-8')

        soc.close()
            
        print("CLOSING SOCKET")    

        
def main():
    
    node = FS_Node()
    node.updateEntrys() 
    
    
if __name__ == "__main__":
    main()