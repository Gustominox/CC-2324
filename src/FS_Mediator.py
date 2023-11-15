import socket
import sys
    ## TODO: falta ver que tamanho queremos
    # FS_Transfer_Protocol (que vai ser chamado após um pedido ao FS_Mediator)
    # Ver se é necessário multithreading
PACKET_SIZE = 1024 
ASK_SEND_FLAG = 1
IP_ADDR = 32 #tamanho IPv4  
FRAG_SIZE = 32
FLAG_LAST = 1
HEADER_RECV = ASK_SEND_FLAG + IP_ADDR + FRAG_SIZE + FLAG_LAST #estrutura dos dados a receber
HASH_SIZE = 32
FRAG_NUMBER_SIZE = 32
HEADER_SEND = ASK_SEND_FLAG + IP_ADDR + HASH_SIZE + FRAG_NUMBER_SIZE #estrutura dos dados a enviar

class FS_Mediator:

    def __init__(self, sock):
        self.sock = sock

    def parseHeader (data):
        
        bitString = ''.join(format(byte, '08b') for byte in data)
        
        #flag do tipo de mensagem (Receber ou enviar fragmento)
        tipoMsg = int(bitString[:ASK_SEND_FLAG+1])

        #IP
        ipBits = bitString[ASK_SEND_FLAG+1:(ASK_SEND_FLAG + IP_ADDR)+1]
        ipBytes = [ipBits[i:i+8] for i in range(0, 32, 8)]
        ip = ".".join(str(int(byte, 2)) for byte in ipBytes)

        if(tipoMsg==0): ## Receber Fragmentos

            # fragSize
            frag_size = int(bitString[(ASK_SEND_FLAG+IP_ADDR)+1 : (ASK_SEND_FLAG+IP_ADDR+FRAG_SIZE)+1])

            # flag bit
            flagLastFrag = bitString[HEADER_RECV-FLAG_LAST+1:HEADER_RECV+1]

            # payload
            payload = bitString[FRAG_SIZE+2:].encode('utf-8')

            return ip, frag_size, flagLastFrag, payload
        
        else: ## Pedido de envio de fragmentos
            
            hashName = bitString[ASK_SEND_FLAG+IP_ADDR+1:(ASK_SEND_FLAG+IP_ADDR+HASH_SIZE)+1]
            
            fragNumber = bitString[HEADER_SEND-FRAG_NUMBER_SIZE+1:HEADER_SEND+1]

            return ip, hashName, fragNumber




    def main():
        if len(sys.argv) <= 1:
            print("Error opening Mediator: no hostname provided")
        else:
            mediator = FS_Mediator(sys.argv[1])
            while True:
                data, addr = mediator.sock.recvfrom(PACKET_SIZE)

                if(((data[0] & 0b10000000) >> 7) == 0): ## Receber fragmentos

                    ip, fragSize, flag, payload = mediator.parseHeader(data)

                    if(ip == addr): # TODO: ver se verificação está boa

                        if(flag): # verifica ultimo fragmento
                            frag += payload[:fragSize+1]
                            #TODO: Ver como se vai obter o nome dos fragmentos para se saber onde escrever, talvez seja necessário:
                            #fragFile = open(fragDir + fileName + "_" + str(fragIndex), "wb" ) 
                            #fragFile.write(frag)
                            #fragFile.close()

                        frag += payload
                    
                    else:
                        print("MEDIATOR_RECV ERROR: IP is different")
                
                else:

                    ip, hashName, fragNumber = mediator.parseHeader(data)
                    
                    if(ip == addr): # TODO: ver se verificação está boa

                        #TODO: Ver onde está o ficheiro no nodo e proseguir para o envio

                    else:
                        print("MEDIATOR ERROR: IP is different")




                


                        