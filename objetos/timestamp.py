from datetime import datetime


class TimeStamp:
    def __init__(self, timestamp, version):
        self.timestamp = timestamp
        self.version = version

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