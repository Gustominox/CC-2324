import socket
import threading
import logging

class FS_Tracker:


    def __init__(self, port = 9090):

        # self.startTime = datetime.now()



        self.entrys = []
        
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
            self.entrys.append(line)
            # print(f"RECEIVED: \"{line}\" ")
        
        s.close()
    
    def startEntryControl(self):
        entrys = 0
        while entrys < 2:
            t = threading.Thread(target=self.FS_TRACK_PROTOCOL)
            t.start()
            t.join()
            entrys += 1
            
def main():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO)
    
    tracker = FS_Tracker()

    tcp = threading.Thread(target=tracker.startEntryControl)
    tcp.start()
    logging.info("Thread starting")
    
    tcp.join()
    # print(tracker.entrys)
    logging.info("ENDED NORMAL EXECUTION")

    
if __name__ == "__main__":
    main()