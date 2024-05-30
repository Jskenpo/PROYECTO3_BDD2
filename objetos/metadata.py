from datetime import datetime


class Header:

    def __init__(self, name, ultimaMod=None, enabled=None):
        self.name = name
        if ultimaMod is not None:
            self.ultimaMod = ultimaMod
        else:
            self.ultimaMod = datetime.now().isoformat()
        if enabled is not None:
            self.enabled = enabled
        else:
            self.enabled = True
    
    def to_dict(self):
        return {
            "name": self.name,
            "ultimaMod": self.ultimaMod,
            "enabled": self.enabled
        }

    # update metadata
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
    