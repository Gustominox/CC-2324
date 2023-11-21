import sys
import time
import struct
import hashlib
import os
from FS_Transfer import FS_transfer
    ## TODO: falta ver que tamanho queremos
    # FS_Transfer_Protocol (que vai ser chamado após um pedido ao FS_Mediator)
    # É necessário multithreading

#Tamanhos dos componentes dos headers
PACKET_SIZE = 1024
ASK_SEND_FLAG = 2
FRAG_SIZE = 32
HASH_SIZE = 32
FRAG_INDEX_SIZE = 32
PAYLOAD_SIZE = 32
HEADER_RECV = ASK_SEND_FLAG + HASH_SIZE + FRAG_INDEX_SIZE + FRAG_SIZE + PAYLOAD_SIZE #header de pedido ao receber
HEADER_SEND = ASK_SEND_FLAG + HASH_SIZE + FRAG_INDEX_SIZE + 64 #header de pedido para enviar
PAYLOAD=PACKET_SIZE-HEADER_RECV

class FS_Mediator:

    def __init__(self, sock, fragDir):
        self.sock = sock
        self.fragDir = fragDir
        self.transfer = FS_transfer()

    def parseHeader (data): # recebe a data em bytes e retorna hashName em hex, payload em bytes e o resto em int
        
        bitString = ''.join(format(byte, '08b') for byte in data)
        
        #Flag do tipo de mensagem (Receber fragmento, enviar fragmento ou ping)
        tipoMsg = int(bitString[:ASK_SEND_FLAG])

        #Nome do hash de bin para hex
        hashName = format(int(bitString[ASK_SEND_FLAG:ASK_SEND_FLAG+HASH_SIZE], 2), f'0{HASH_SIZE//4}x')[2:]

        #Índice Fragmento
        fragIndex = int(bitString[ASK_SEND_FLAG+HASH_SIZE:ASK_SEND_FLAG+HASH_SIZE+FRAG_INDEX_SIZE])

        if(tipoMsg==2): #pedido de ping (cálculo da diferença de tempo)
            endTime = time.time()
            startTimeBit = bitString[ASK_SEND_FLAG+HASH_SIZE+FRAG_INDEX_SIZE:ASK_SEND_FLAG+HASH_SIZE+FRAG_INDEX_SIZE+64] # float tem tamanho de 64 bits 
            startTimeBytes = int(startTimeBit, 2).to_bytes(len(startTimeBit) // 8, byteorder='big')
            startTime = struct.unpack('>d', startTimeBytes)[0]

            return hashName, fragIndex, (endTime - startTime)

        if(tipoMsg==0): ## Receber Fragmentos

            # fragSize
            fragSize = int(bitString[HEADER_RECV-PAYLOAD_SIZE-FRAG_SIZE:HEADER_RECV-PAYLOAD_SIZE])

            # payloadSize > 0 (ultimo frag)
            payloadSize = int(bitString[HEADER_RECV-PAYLOAD_SIZE:HEADER_RECV])

            # payload
            payload = bitString[HEADER_RECV:].encode('utf-8')

            return hashName, fragIndex, fragSize, payloadSize, payload
        
        else: ## Pedido de envio de fragmentos
            
            return hashName, fragIndex
        
    def verifyHash(self,filePath,hashName,fragIndex):
        file = open(filePath, 'rb')
        data = file.read()
        verHash = hashlib.shake_256(data).hexdigest(8)
        if(verHash == hashName):
            print(f"Fragment {hashName}_{fragIndex} has been received correctly")
            return 1
        else:
            os.remove(filePath)
            print(f"Verification of {hashName}_{fragIndex} failed. File removed and new request sent.")
            return 0
    

    def fastestConn(ipList):
        fastestIp = min(ipList, key=lambda x: x[1])
        return fastestIp


    def main():
        if len(sys.argv) <= 1:
            print("Error opening Mediator: no hostname provided")
        else:
            mediator = FS_Mediator(sys.argv[1])
            while True:
                data, addr = mediator.sock.recvfrom(PACKET_SIZE) #TODO: Ver como escolher os vários pacotes
 

                if((data[0] & 0b11000000) == 0): ## Receber fragmentos

                    hashName, fragIndex, fragSize, payloadSize, payload = mediator.parseHeader(data)

                    filePath = mediator.fragDir + hashName + "_" + str(fragIndex)
                    
                    #TODO: Ver onde guardar este frag
                    if(payloadSize!=0): # verifica ultimo fragmento
                        frag += payload[:payloadSize]
                        file = open(filePath, 'wb') # Verificar antes da escrita
                        file.write(frag)
                        file.close()

                        if((mediator.verifyHash(filePath,hashName,fragIndex))==0): #Caso falhe a verificação
                            mediator.transfer.askFrag(hashName,fragIndex,addr[0])
                        
                        
                    frag += payload
                      
                elif(data[0] & 0b11000000 == 1): # Enviar fragmentos

                    hashName, fragIndex = mediator.parseHeader(data)

                    with open(mediator.fragDir + hashName + "_" + str(fragIndex), 'rb') as file:
                        fragSize = len(file)
                    
                    mediator.transfer.sendFrag(mediator.sock,addr[0],fragSize,mediator.fragDir,hashName,fragIndex)
                    break#TODO: Falta ver onde vamos guardar a informação relevante a cada fragmento ou escrevemos em ficheiro até ficar completo?
                
                else:
                    hashName, fragIndex, tempo = mediator.parseHeader(data)
                    #TODO: Adicionar uma tabela com chave hash+index+ip->tempo e chamar a função fastestConn
                   