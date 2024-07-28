class Session:
    List = []
    def AddStatusLogin(self, user):
        self.List.append(user)
        return self.List

    def getSession(self):
        for x in  self.List:
            return x

    def removeSession(self):
        self.List.clear()

    def checkStatus(self):
        if len(self.List) == 0:
            return False
        else:
            return True

