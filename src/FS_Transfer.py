import struct
import time
from FS_Mediator import FRAG_SIZE, HASH_SIZE, FRAG_INDEX_SIZE, PAYLOAD, PAYLOAD_BYTES, HEADER_MAX

class FS_transfer:

    def __init__(self,socket):
        self.socket=socket


    def rightPaddingBytes(data, length):
        paddingLength = max(length - len(data), 0)
        padding = bytes(paddingLength) 
        return data + padding
    

    def rightPaddingBits(data, length):
        paddingLength = max(length - len(data), 0)
        padding = '0' * paddingLength
        return data + padding


    def sendFrag(self, socket, ip, fragSize, fragDir, hashName, fragIndex): #os args são convertidos em bits e adicionados a um header
        with open(fragDir + hashName + "_" + str(fragIndex), 'rb') as file: #o ficheiro vai ter de estar guardado com o hash em vez do nome

            data = file.read(PAYLOAD)
            data = self.rightPaddingBytes(data,PAYLOAD_BYTES) # padding

            if not data: #EOF
                print(f"Data of {hashName} with fragment number {int(fragIndex)} should have been sent correctly")
            
            #hashName para Bits
            hashNameBits = format(int(hashName, 16), f'0{HASH_SIZE}b')
            
            #IndiceFrag para Bits
            fragIndexBits = bin(fragIndex)[2:].zfill(FRAG_INDEX_SIZE)
            
            #fragSize para Bits
            fragSizeBits = bin(fragSize)[2:].zfill(FRAG_SIZE)
            
            #formar o header em bytes
            headerInc = "00" + hashNameBits + fragIndexBits + fragSizeBits
            headerInc = self.rightPaddingBits(headerInc,HEADER_MAX)
            header = int(headerInc, 2).to_bytes(HEADER_MAX // 8, byteorder='big')
            
            packet = header + data
            
            self.socket.sendto(packet, (ip, 9090))


    def askFrag(self, socket, hashName, Index, ip):
        
        hashNameBits = format(int(hashName, 16), f'0{HASH_SIZE}b')
        
        fragIndexBits = bin(Index)[2:].zfill(FRAG_INDEX_SIZE)
       
        headerInc = "01" + hashNameBits + fragIndexBits

        header = self.rightPaddingBits(headerInc,HEADER_MAX)
        
        packet = int(header, 2).to_bytes(HEADER_MAX // 8, byteorder='big')

        self.socket.sendto(packet, (ip, 9090))


    def ping(self, socket, hashName, fragIndex, ip):
        
        startTime=int(time.time())
        startTimeBytes=struct.pack('>d', startTime)

        hashNameBits = format(int(hashName, 16), f'0{HASH_SIZE}b')

        fragIndexBits = bin(fragIndex)[2:].zfill(FRAG_INDEX_SIZE)

        headerInc = "10" + hashNameBits + fragIndexBits + startTimeBytes

        header = self.rightPaddingBits(headerInc,HEADER_MAX)

        packet = int(header, 2).to_bytes(HEADER_MAX // 8, byteorder='big')

        self.socket.sendto(packet, (ip, 9090))

        return startTimeBytes
