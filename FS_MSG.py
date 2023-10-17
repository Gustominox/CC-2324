class FS_Msg:
    def __init__(self):
        self.SENDER_ID = "NO VALUE"  
        self.SENDER_IP = "NO VALUE"  
        self.MSG_TYPE = "NO VALUE"
        self.BODY = "NO VALUE"

    def __str__(self):

        out = ""
        out += "Message = { \n"
        out += f"SENDER_ID = {self.SENDER_ID}\n"
        out += f"SENDER_IP = {self.SENDER_IP}\n"
        out += f"MSG_TYPE = {self.MSG_TYPE}\n"
        out += f"BODY = {self.BODY}\n"
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
                self.BODY = element[1].strip("\{\} ").split(",")

            else:
                pass
