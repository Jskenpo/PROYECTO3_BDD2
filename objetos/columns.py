from .timestamp import TimeStamp

class Column:

    def __init__(self, name, type, value, timestamp):
        self.name = name
        self.type = type
        self.value = value
        self.timestamp = [timestamp]

    def addTimestamp(self, timestamp, version):
        self.timestamp.append(
            TimeStamp(timestamp=timestamp, version=version)
            )

    def getName(self):
        return self.name
    
    def getType(self):
        return self.type

    def getValue(self):
        return self.value
    
    def getTimestamp(self):
        return self.timestamp