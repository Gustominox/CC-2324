
class FS_Tracker_Table:
    def __init__(self):
        self.contents = {}  # Inicia o nodo vazio
        self.node_counter = 1 # Inicializa o counter global a 1 (autoincrementado)
        self.address = {} # Inicializa o endereço do nodo
    
    def __str__(self):
        return
    
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

    def update_fragment_status(self, node_id, file_id, fragment_index, status): #incluir lista de fragmentos
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
    
    def writeTable(self):
        string = []

        for node_id in self.contents.items():
            string.append("\nNodo->")
            string.append(node_id)
            string.append("Ficheiros->")
            for files in self.contents[node_id]:
                string.append(files)
                string.append(", ")
        
        return string
  