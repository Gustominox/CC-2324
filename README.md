# CC-2324

Projeto CC 2023-2024


Requesitos:

- O protocolo FS TRACK Protocol deve funcionar sobre TCP e suportar:
  - O registo de um FS_NODE
  - A Atualizacao de lista de ficheiros e blocos disponiveis num FS_NODE
  - O pedido de localizacao de um ficheiro devolvendo uma lista de FS_NODE e blocos neles disponiveis



Etapas sugeridas para esta fase:

1. Especificar o protocolo FS Track Protocol para funcionar sobre TCP
   - formato das mensagens protocolares (sintaxe)
   - função e significado dos campos (semântica)
   - diagrama temporal ilustrativo (comportamento)
2. Implementação e teste do protocolo FS Track Protocol
   exemplo de teste: registar um FS_Node (endereço) e ficheiros/blocos a seu cargo; pedir localização de um ficheiro;
