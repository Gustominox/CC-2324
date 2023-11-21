import socket
import struct
import time
from FS_Mediator import FRAG_SIZE, HASH_SIZE, FRAG_INDEX_SIZE, PAYLOAD_SIZE, PAYLOAD, PACKET_SIZE, HEADER_SEND

class FS_transfer:
    
    def __init__(self):
        self #TODO: Ver o que falta na inicialização

    
    def sendFrag(socket, ip, fragSize, fragDir, hashName, fragIndex): #os args são convertidos em bits e adicionados a um header
        with open(fragDir + hashName + "_" + str(fragIndex), 'rb') as file: #o ficheiro vai ter de estar guardado com o hash em vez do nome
            
            while True:

                data = file.read(PAYLOAD)

                if not data: #EOF
                    print(f"Data of {hashName} with fragment number {int(fragIndex)} should have been sent correctly")
                    break

                #hashName para Bits
                hashNameBits = format(int(hashName, 16), f'0{HASH_SIZE}b')

                #IndiceFrag para Bits
                fragIndexBits = bin(fragIndex)[2:].zfill(FRAG_INDEX_SIZE)

                #fragSize para Bits
                fragSizeBits = bin(fragSize)[2:].zfill(FRAG_SIZE)

                #formar o header sem a última flag de ultimo bloco de fragmento
                headerInc = "00" + hashNameBits + fragIndexBits + fragSizeBits
             

                if (len(data)) < PAYLOAD: #Caso do ultimo fragmento
                    payload = ''.join(format(byte, '08b') for byte in data)
                    c=0
                    while (len(payload) < PAYLOAD): #preenche o pacote com 0's à direita
                        payload <<= 1
                        c+=1
                    
                    payloadSize=(bin(c)[2:]).zfill(PAYLOAD_SIZE)
                    header = headerInc + payloadSize
                    packet = header + payload
                    socket.sendto(packet, (ip, 9090))

                else:
                    header = headerInc + '0' * PAYLOAD_SIZE
                    
                    packetBytes = int(header, 2).to_bytes(PACKET_SIZE // 8, byteorder='big') + ''.join(format(byte, '08b') for byte in data)

                    socket.sendto(packetBytes, (ip, 9090))
    
    def askFrag(socket, hashName, Index, ip):
        headerInc = "01"
        hashNameBits = format(int(hashName, 16), f'0{HASH_SIZE}b')
        fragIndexBits = bin(Index)[2:].zfill(FRAG_INDEX_SIZE)
       
        header = headerInc + hashNameBits + fragIndexBits
        packet = header.zfill(PACKET_SIZE)

        packetBytes = int(header, 2).to_bytes(PACKET_SIZE // 8, byteorder='big')

        socket.sendto(packetBytes, (ip,9090))

    def ping(socket,hashName,fragIndex, ip): #TODO: rever formato do pacote do ping (vale a pena mandar o hashName + fragIndex?) + onde chamar
        startTime=time.time()
        startTimeBytes=struct.pack('>d', startTime)

        hashNameBits = format(int(hashName, 16), f'0{HASH_SIZE}b')

        fragIndexBits = bin(fragIndex)[2:].zfill(FRAG_INDEX_SIZE)

        header = "10" + hashNameBits + fragIndexBits + fragIndexBits

        headerBytes = int(header, 2).to_bytes(HEADER_SEND // 8, byteorder='big')
        packet = headerBytes + startTimeBytes

        socket.sendto(packet, (ip, 9090))

        return startTimeBytes

        







