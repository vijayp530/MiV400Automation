import paramiko

class MacMachine:
    def __init__(self,ip,username,password):
        self.ip = ip
        self.username = username
        self.password = password
        try:
            print("Establishing connection to %s" % self.ip)
            transport = paramiko.Transport(self.ip, 22)
            transport.connect(username=self.username, password=self.password)
            print("Connection established")
        except paramiko.AuthenticationException:
            print("We had an authentication exception!")
            raise
            


#macObj=MacMachine("10.198.17.106","pjayaram","ShoreTel12$")