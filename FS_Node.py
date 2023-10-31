import socket
import sys
import logging
import json
from FS_MSG import FS_Msg


cont = {
    "FILE1": [
        128,
        [
            0, 0, 0, 0, 0]
    ],
    "FILE2": [
        0,
        [0, 0, 0, 0, 0]
    ],
    "FILE3": [
        512,
        [0, 0, 0, 0, 0]
    ]
}


class FS_Node:

    def __init__(self, hostname, port=9090):

        # self.startTime = datetime.now()
        self.soc = socket.socket(socket.AF_INET,     # Familia de enderecos ipv4
                                 socket.SOCK_STREAM)  # Connection-Oriented (TCP PROTOCOL)

        self.hostname = hostname
        self.endereco = socket.gethostbyname(self.hostname)
        self.porta = port
        self.soc.connect((self.endereco, self.porta))

        self.nodeId = f"{self.endereco}"
        self.contents = {}

    def sendTcpMsg(self, msg):

        message = msg.toText()

        try:
            print(f"Sending: {message}")
            self.soc.sendall(message.encode('utf-8'))
        except:
            print("Impossivel Conectar")
            return

        if msg.MSG_TYPE == "ASK FILE":

            message = self.soc.recv(1024)
            line = message.decode('utf-8')
            print(line)

        else:
            pass

    def createMsg(self, MSG_TYPE, BODY={}):

        if MSG_TYPE == "UPDATE NODE":
            BODY = self.contents

        msg = FS_Msg(self.hostname, self.endereco, MSG_TYPE, BODY)

        return msg

    def addFile(self, filePath):

        with open(filePath, 'rb') as file:
            data = file.read()  # .replace('\n',' ')

        # TODO support various fragSizes, increase depending on file size
        fragSize = 8

        fileSize = len(data)

        numFrags = int(fileSize / fragSize)

        lastFragSize = fileSize - (numFrags * fragSize)

        print(lastFragSize)

        # TODO em vez de usar path Adicionar o SHA-256 aqui para ser o fich id
        self.contents[filePath] = [fileSize, [True] * numFrags]


def main():

    if len(sys.argv) > 1:
        node = FS_Node(sys.argv[1],int(sys.argv[2]))
    else:
        node = FS_Node()

    node.addFile("askFile.msg")
    msg = node.createMsg("UPDATE NODE")
    node.sendTcpMsg(msg)

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO)

    while True:
        print("Node > ", end="")

        option = input()

        if option == "update":

            msg = node.createMsg("UPDATE NODE")
            node.sendTcpMsg(msg)

        elif option == "ask":
            file = input()

            BODY = {file: "NONE"}
            msg = node.createMsg("ASK FILE", BODY)
            node.sendTcpMsg(msg)

        elif option == "add":
            print("Insert File > ", end="")
            filePath = input()
            node.addFile(filePath)

        elif option == "list":

            print(json.dumps(node.contents, indent=4))

        elif option == "exit":

            # TODO: needs to send delete node msg before closing
            node.soc.close()
            logging.info("Terminate normal execution")
            break

        else:
            logging.info("Unknown Option")


if __name__ == "__main__":
    main()
