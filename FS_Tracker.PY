import socket
import threading
import logging
from FS_Tracker_Table import FS_Table
from FS_MSG import FS_Msg

class FS_Tracker:


    def __init__(self, port = 9090):

        # self.startTime = datetime.now()



        self.entrys = []
        self.table = FS_Table()
        self.hostname = socket.gethostname()
        self.endereco = socket.gethostbyname(self.hostname)  
        self.porta = port
        
    # def FS_TRACK_PROTOCOL(self,soc):
    #     logging.info("Thread: Listening for node tcp message")
    #     connection, address = soc.accept() 
    #     # ler a msg q o node envia
        
    #     while True:
    #         data = connection.recv(1024)
    #         if not data:
    #             break
    #         line = data.decode('utf-8')
    #         self.entrys.append(line)
    #         # print(f"RECEIVED: \"{line}\" ")
    #     logging.info("Thread: Ended node tcp message")
        
    
    def startEntryControl(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        soc.bind(('', self.porta))            
        soc.listen()

        while True:
            
            connection, address = soc.accept() # Diferenciar que tipo de msg o node esta a enviar
            data = connection.recv(1024)
            msg = data.decode('utf-8')
            pckg = self.tcpDecode(msg)
            
            message = FS_Msg()
            message.read_message(pckg)
            print(message)
            
            if message.MSG_TYPE == "UPDATE NODE":
                logging.info("Received update request")
                
                # self.table.addCompleteNode( message.SENDER_ID, message.SENDER_IP, fragments, fileId)
    
            elif message.MSG_TYPE == "DELETE NODE":
                continue
            elif message.MSG_TYPE == "FILES LIST":
                connection.send(str(self.entrys).encode())
                continue
            elif message.MSG_TYPE == "END TRACKER":
                soc.close()
                break
            else:
                logging.error(f"INVALID MESSAGE FROM NODE: {message.MSG_TYPE}")
    
    def tcpDecode(self,msg):
        pckg = ""
        for line in msg.split('\n'):
            if not (line == '' or line[0] == '#' ):
                pckg += line
        return pckg 
            
        
        
            
def main():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO)
    
    tracker = FS_Tracker()
    tracker.entrys.append("DEFAULT ENTRY")
    tcp = threading.Thread(target=tracker.startEntryControl)
    tcp.start()
    
    tcp.join()
    print(tracker.entrys)
    logging.info("ENDED NORMAL EXECUTION")

    
if __name__ == "__main__":
    main()