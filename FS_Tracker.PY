import socket
import threading
import logging

class FS_Tracker_Table:
    def __init__(self):
        self.contents = {}  # Inicia o nodo vazio
        self.node_counter = 1 # Inicializa o counter global a 1 (autoincrementado)
        self.address = {} # Inicializa o endereço do nodo
    
    def add_node(self, node_id, address):
        # Adiciona um nodo ao tracker
        node_id = self.node_counter
        self.contents[node_id] = {}
        self.node_addresses[node_id] = address
        self.node_counter += 1
        return node_id

    def add_file_with_fragments(self, node_id, file_id):
        # Adiciona um ficheiro a um nodo com os fragmentos inicializados a falso
        if node_id not in self.contents:
            self.contents[node_id] = {}
        fragments = [False] * 20
        self.contents[node_id][file_id] = fragments

    def update_fragment_status(self, node_id, file_id, fragment_index, status):
        # Dá update ao fragmento de um ficheiro para um dado estado (Tanto para adicionar como remover)
        if node_id in self.contents and file_id in self.contents[node_id]:
            if 0 <= fragment_index < 20:
                self.contents[node_id][file_id][fragment_index] = status
    
    def remove_file_from_node(self, node_id, file_id):
        # Remove um ficheiro de um nodo
        if node_id in self.contents and file_id in self.contents[node_id]:
            del self.contents[node_id][file_id]
    
    def remove_node(self, node_id):
        # Remove a node and all its associated information from the table
        if node_id in self.contents:
            del self.contents[node_id]
        if node_id in self.node_addresses:
            del self.node_addresses[node_id]

    def get_fragment_status(self, node_id, file_id):
        # Verifica o estado de fragmentos de um ficheiro (Para verificação manual?)
        if node_id in self.contents and file_id in self.contents[node_id]:
            return self.contents[node_id][file_id]
        else:
            return None

    def get_nodes_with_fragment(self, file_id, fragment_index):
        # Retorna os nodos que têm um fragmento de um ficheiro
        nodes_with_fragment = []
        for node_id, files in self.contents.items():
            if file_id in files:
                fragments = files[file_id]
                if 0 <= fragment_index < 20 and fragments[fragment_index]:
                    nodes_with_fragment.append(node_id)
        return nodes_with_fragment
    
    def get_nodes_with_filename(self, filename):
        # Verifica os nodos que têm um ficheiro
        nodes_with_filename = []
        for node_id, files in self.contents.items():
            if filename in files:
                nodes_with_filename.append(node_id)
        return nodes_with_filename

    def get_table_of_contents(self):
        # Retorna a tabela de nodos
        return self.contents
    
    def get_node_address(self, node_id):
        # Retorna o endereço de um nodo
        return self.node_addresses.get(node_id)

class FS_Tracker:


    def __init__(self, port = 9090):

        # self.startTime = datetime.now()



        self.entrys = []
        
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
            
            if pckg[0] == "UPDATE NODE":
                logging.info("Received update request")
                
                for entry in pckg[1:]:
                    self.entrys.append(entry)
                
            elif pckg[0] == "DELETE NODE":
                continue
            elif pckg[0] == "FILES LIST":
                connection.send(str(self.entrys).encode())
                continue
            elif pckg[0] == "END TRACKER":
                soc.close()
                break
            else:
                logging.error(f"INVALID MESSAGE FROM NODE: {pckg[0]}")
    
    def tcpDecode(self,msg):
        pckg = []
        for line in msg.split('\n'):
            if not (line == '' or line[0] == '#' ):
                pckg.append(line)
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