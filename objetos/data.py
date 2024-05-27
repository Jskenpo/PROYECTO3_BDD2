from datetime import datetime

from .columns import Column
from .timestamp import TimeStamp
from .metadata import Header

class Data:
    def __init__(self, tablename,indexRow,columnFamily):
        self.tablename = tablename
        self.indexRow = indexRow
        self.columnFamily = columnFamily
        self.columns = []
        self.metadata = Header(tablename)

    def addColumn(self, name, type, value):
        self.columns.append(
            Column(
                name = name, 
                type = type, 
                value = value, 
                timestamp = TimeStamp( datetime.now().isoformat(), 1)
                )
            )

    def getTableName(self):
        return self.tablename
    
    def getIndexRow(self):
        return self.indexRow
    
    def getColumnFamily(self):
        return self.columnFamily
    
    def getColumns(self):
        return self.columns
    
    def getMetadata(self):
        return self.metadata
