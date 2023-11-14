import socket
import sys
    ## TODO: falta ver que tamanho queremos
    # FS_Transfer_Protocol (que vai ser chamado após um pedido ao FS_Mediator)
    #  Ver que porta usar para enviar os pacotes (mesma ou não?)
PACKET_SIZE = 1024 
IP_ADDR = 32 #tamanho IPv4  
FRAG_SIZE = 32
FLAG_LAST = 1
HEADER = IP_ADDR + FRAG_SIZE + FLAG_LAST
PAYLOAD = PACKET_SIZE - HEADER

class FS_Mediator:

    def __init__(self,hostname):
        self.hostname = hostname
        self.endereco = socket.gethostbyname(self.hostname)
        self.porta = 9090
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.endereco,self.porta))

    def parseHeader (data): #Para IP(4 bytes), fragSize(4 bytes)
        
        # IP
        ip_bytes = data[:4]
        ip = '.'.join(str(byte) for byte in ip_bytes)

        # fragSize
        frag_size_bytes = data[4:8]
        frag_size = int.from_bytes(frag_size_bytes, byteorder='big')

        # flag bit
        flag_byte = data[8]
        flag = (flag_byte & 0b10000000) >> 7
    
        # payload
        rest_bits = flag_byte & 0b01111111
        payload = rest_bits + data[9:]

        return ip, frag_size, flag, payload
    
##    def listenUDP(self,sock):
        while True:
            data, addr = sock.recvfrom(1024)
        

    def main():
        if len(sys.argv) <= 1:
            print("Error opening Mediator: no hostname provided")
        else:
            mediator = FS_Mediator(sys.argv[1])
            while True:
                data, addr = mediator.sock.recvfrom(PACKET_SIZE)
                ip, fragSize, flag, payload = mediator.parseHeader(data) # IP para a verificação?? Ver addr acima e ip se são iguais???

                if(flag):
                    frag += fragSize
                    ##TODO: Ver como se vai obter o nome dos fragmentos para se saber onde escrever, talvez seja necessário
                    #fragFile = open(fragDir + fileName + "_" + str(fragIndex), "wb" ) 
                    #fragFile.write(frag)
                    #fragFile.close()
                
                flag += payload
            


            







        
            
