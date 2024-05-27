from datetime import datetime


class Header:

    def __init__(self, name):
        self.name = name
        self.ultimaMod = datetime.now().isoformat()
        self.enabled = True

    def updateLastMod(self):
        self.ultimaMod = datetime.now().isoformat()

    def setEnabled(self):
        self.enabled = True

    def setDisabled(self):
        self.enabled = False

    def updateName(self, name):
        self.name = name

    def getName(self):
        return self.name
    
    def getUltimaMod(self):
        return self.ultimaMod
    
    def getEnabled(self):
        return self.enabled
    