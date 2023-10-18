import json
class FS_Msg:
    def __init__(self):
        self.SENDER_ID = "NO VALUE"  
        self.SENDER_IP = "NO VALUE"  
        self.MSG_TYPE = "NO VALUE"
        self.BODY = {}

    def __str__(self):

        out = ""
        out += "Message = { \n"
        out += f"SENDER_ID = {self.SENDER_ID}\n"
        out += f"SENDER_IP = {self.SENDER_IP}\n"
        out += f"MSG_TYPE = {self.MSG_TYPE}\n"
        out += f"BODY = {json.dumps(self.BODY, indent=4)}\n"
        out += "}"

        return out

    def __repr__(self):

        out = ""
        out += "Message = { \n"
        out += f"SENDER_ID = {self.SENDER_ID}\n"
        out += f"SENDER_IP = {self.SENDER_IP}\n"
        out += f"MSG_TYPE = {self.MSG_TYPE}\n"
        out += f"BODY = {self.BODY}\n"
        out += "}"

        return out
    
    def toText(self):
        out = ""
        out += F"SENDER_ID={self.SENDER_ID};\n"
        out += F"SENDER_IP={self.SENDER_IP};\n"
        out += F"MSG_TYPE={self.MSG_TYPE};\n"
        out += "BODY={\n"
        for file in self.BODY:
            fragments = "["
            for frag in self.BODY[file][1]:
                if frag: fragments += "1"
                else: fragments += "0"
            fragments += "]"
            out += f"{file} {self.BODY[file][0]} {fragments},\n"
        out += "};"
        return out

    def read_message(self, data):
        # print(f"DATA IN MSG: {data}")
        print(f"DATA: {data}")

        for field in data.split(";"):
            element = field.split("=")
            # print(element)
            if element[0] == "SENDER_ID":
                self.SENDER_ID = element[1]
            if element[0] == "SENDER_IP":
                self.SENDER_IP = element[1]
            elif element[0] == "MSG_TYPE":
                self.MSG_TYPE = element[1]
            elif element[0] == "BODY":
                bodyLines = element[1].strip("\{\} ").split(",")
                print(f"BODYLINES: {bodyLines}")
                
                for line in bodyLines:
                    if line != "":
                        elems = line.split(" ")
                        
                        nodeId = elems[0]
                        fileSize = int(elems[1])
                        fragments = []
                        for char in elems[2]:
                            if char == "0": fragments.append(False)
                            elif char == "1": fragments.append(True)
                            else: pass 
                            
                        self.BODY[nodeId] = [fileSize,fragments]
                    

            else:
                pass
