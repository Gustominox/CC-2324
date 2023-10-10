import socket
class FS_Tracker:


    def __init__(self, port = 9090):

        # self.startTime = datetime.now()




        self.hostname = socket.gethostname()
        self.endereco = socket.gethostbyname(self.hostname)  
        self.porta = port
        
    def FS_TRACK_PROTOCOL(self):
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        s.bind(('', self.porta))            
        s.listen()

        connection, address = s.accept()
                
        while True:
            data = connection.recv(1024)
            if not data:
                break
            line = data.decode('utf-8')

        
def main():
    
    tracker = FS_Tracker()
    tracker.FS_TRACK_PROTOCOL() 
    
if __name__ == "__main__":
    main()