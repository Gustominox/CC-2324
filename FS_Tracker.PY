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
        
    def FS_TRACK_PROTOCOL(self,soc):
        logging.info("Thread: Listening for node tcp message")
        connection, address = soc.accept() 
        # ler a msg q o node envia
        
        while True:
            data = connection.recv(1024)
            if not data:
                break
            line = data.decode('utf-8')
            self.entrys.append(line)
            # print(f"RECEIVED: \"{line}\" ")
        logging.info("Thread: Ended node tcp message")
        
    
    def startEntryControl(self):
        entrys = 0
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        soc.bind(('', self.porta))            
        soc.listen()

        while entrys < 2:
            
            connection, address = soc.accept() # Diferenciar que tipo de msg o node esta a enviar
            data = connection.recv(1024)
            msg = data.decode('utf-8')
            
            if msg == "UPDATE FS_NODE":
                logging.info("Received update request")
                
                t = threading.Thread(target=self.FS_TRACK_PROTOCOL,args= (soc,))
                t.start()
                t.join()
                entrys += 1
            elif msg == "DELETE FS_NODE":
                continue
            else:
                logging.error(f"INVALID MESSAGE FROM NODE: {msg}")
                
        soc.close()
        
            
def main():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO)
    
    tracker = FS_Tracker()

    tcp = threading.Thread(target=tracker.startEntryControl)
    tcp.start()
    
    tcp.join()
    print(tracker.entrys)
    logging.info("ENDED NORMAL EXECUTION")

    
if __name__ == "__main__":
    main()