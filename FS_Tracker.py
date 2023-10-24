import socket
import threading
import logging
import sys
from FS_Tracker_Table import FS_Table
from FS_MSG import FS_Msg

class FS_Tracker:


    def __init__(self, port = 9090):

        # self.startTime = datetime.now()



        self.table = FS_Table()
        self.hostname = socket.gethostname()
        self.endereco = socket.gethostbyname(self.hostname)  
        self.porta = port
        
    
    def startEntryControl(self,connection, address):
        
        while True:
            
            data = connection.recv(1024)
            msg = data.decode('utf-8')
            
            message = FS_Msg()
            message.read_message(msg)
            
            if message.MSG_TYPE == "UPDATE NODE":
                self.table.updateNode(message.SENDER_ID,message.BODY)
                logging.info(f"UPDATE: {message.SENDER_ID}")

                # logging.info(f"MESSAGE RECEIVED: \n{message.toText()}")
                
                print(self.table)
            elif message.MSG_TYPE == "DELETE NODE":
                
                self.table.removeNode(message.SENDER_ID)
                logging.info(f"REMOVE: {message.SENDER_ID}")
                # print(self.table)
                
            elif message.MSG_TYPE == "ASK FILE":
                
                node_list = self.table.getNodesWithFilename(message.BODY)
                print(f"NODE LIST: \n{node_list}")
                connection.send(f"{node_list}".encode('utf-8'))
                
            elif message.MSG_TYPE == "END TRACKER":
                pass
            else:
                logging.error(f"INVALID MESSAGE FROM NODE: {message.MSG_TYPE}")

            
        
        
            
def main():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO)
    if len(sys.argv) > 1:
        tracker = FS_Tracker(int(sys.argv[1]))
    else:
        tracker = FS_Tracker()
        
    
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    soc.bind(('', tracker.porta))            
    soc.listen()
    

    while True:
        connection, address = soc.accept() 
        tcp = threading.Thread(target=tracker.startEntryControl,args=(connection, address))
        tcp.start()
        
    logging.info("ENDED NORMAL EXECUTION")

    
if __name__ == "__main__":
    main()