import socket
import time

class FS_Transfer:
    
    def __init__(self, hostname):
        self.hostname = hostname
        self.endereco = socket.gethostbyname(self.hostname)
        self.porta = 9090
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.endereco,self.porta))


    def fastestConn(socket, ipList, timeout):
        results = []

        for ip in ipList:
            startTime = time.time()

            try:
                # Assuming the socket is already connected
                # If not, you may need to connect it before checking the speed
                with socket.create_connection((ip, socket.getpeername()[1]), timeout=timeout):
                    elapsedTime = time.time() - startTime
                    results.append((ip, elapsedTime))

            except socket.error as e:
                print(f"FS_TRANSFER ERROR: Connection to {ip} failed: {e}")

        if not results:
            print("FS_TRANSFER ERROR: No successful connections.")
            return None

        fastestIp = min(results, key=lambda x: x[1])
        return fastestIp
    
    
