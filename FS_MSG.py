class FS_MSG:
    def __init__(self):
        self.SENDER_ID = None  # SENDER_ID
        self.MSG_TYPE = None 
        self.BODY = {}
    def __str__(self):
        return
    
    def __repr__(self):
        return
    
    def read_message(self,data):
        print(data)
        
        for line in data:
            line.split(";")
            for field in line:
                field.split("=")
                
                if field[0] == "SENDER_ID":
                    self.SENDER_ID = field[1]
                elif field[0] == "MSG_TYPE":
                    self.MSG_TYPE = field[1]
                elif field[0] == "BODY":
                    body = ''.join(field[1].splitlines().strip("\{\} ").split(","))
                    
                else:
                  pass