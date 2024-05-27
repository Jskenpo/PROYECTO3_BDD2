from datetime import datetime

from .columns import Column
from .timestamp import Versiones
from .metadata import Header

class Data:
    def __init__(self, tablename, indexRow, columns=None, metadata=None):
        self.tablename = tablename
        self.indexRow = indexRow
        if columns is not None:
            self.columns = columns
        else:
            self.columns = []
        if metadata is not None:
            self.metadata = metadata
        else:
            self.metadata = Header(tablename)

    def to_dict(self):
        return {
            "tablename": self.tablename,
            "indexRow": self.indexRow,
            "columns": [c.to_dict() for c in self.columns],
            "metadata": self.metadata.to_dict()
        }

    def addColumn(self, name, type, value, columnFamily):
        self.columns.append(
            Column(
                name = name, 
                type = type, 
                columnFamily = columnFamily,
                versiones = Versiones(value = value, timestamp=datetime.now().isoformat(), version=1)
                )
            )

    def getTableName(self):
        return self.tablename
    
    def getIndexRow(self):
        return self.indexRow
    
    def getColumns(self):
        return self.columns
    
    def getMetadata(self):
        return self.metadata
