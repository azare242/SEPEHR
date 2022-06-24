class Message:
    def __init__(self,info: list):
        self.id = info[0]
        self.txt = info[1]
        self.sendby = info[2]

    def get_info(self):
        return f"""[TEXT: {self.txt}, SEND BY: {self.sendby}]"""
