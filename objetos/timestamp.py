from datetime import datetime


class Versiones:
    def __init__(self, value, timestamp, version):
        self.value = value
        self.timestamp = timestamp
        self.version = version

    def to_dict(self):
        return {
            "value": self.value,
            "timestamp": self.timestamp,
            "version": self.version
        }

    def updateManualVersion(self, version):
        self.version = version

    def updateVersion(self):
        self.version += 1

    def updateTimestamp(self, timestamp):
        self.timestamp = timestamp

    def getTimestamp(self):
        return self.timestamp
    
    def getVersion(self):
        return self.version