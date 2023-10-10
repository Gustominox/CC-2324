class Pear:

    def __init__(self, conf_file, port = 9090):

        # self.startTime = datetime.now()

        self.conf = Config(conf_file)

        # innit_log(self.conf.logFile)


        # self.hostname = socket.gethostname()
        self.endereco = socket.gethostbyname(self.hostname)  # '10.0.0.1'
        self.porta = port

    