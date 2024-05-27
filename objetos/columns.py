from .timestamp import Versiones

class Column:

    def __init__(self, name, type, columnFamily, versiones):
        self.name = name
        self.type = type
        self.columnFamily = columnFamily
        self.versiones = [versiones]

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "columnFamily": self.columnFamily,
            "versiones": [t.to_dict() for t in self.versiones]
        }

    def addVersiones(self, timestamp, version, value):
        self.timestamp.append(
            Versiones(value = value, timestamp=timestamp, version=version)
            )

    def getName(self):
        return self.name
    
    def getType(self):
        return self.type

    def getValue(self):
        return self.value
    
    def getVersiones(self):
        return self.versiones
    
    def getColumnFamily(self):
        return self.columnFamily