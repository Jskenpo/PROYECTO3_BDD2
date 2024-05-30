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
    
    def checkClm(self, cf, rowID):
        for c in self.columns:
            if c.getColumnFamily() == cf and c.getClmID() == rowID:
                print("Columna ya existe")
                return c
        return None
    
    def uniqueCLMID(self):
        return set(c.getClmID() for c in self.columns)
    
    def getColumnsOfClmID(self, clmID):
        return [c for c in self.columns if c.getClmID() == clmID]


    # Update name
    def updateName(self, name):
        self.tablename = name
        self.metadata.updateName(name)

    # create
    def addColumn(self, clmID, name, type, value, columnFamily):
        self.columns.append(
            Column(
                clmID= clmID,
                name = name, 
                type = type, 
                columnFamily = columnFamily,
                versiones = [Versiones(value = value, timestamp=datetime.now().isoformat(), version=1)]
                )
            )

    def getVersionOfCF(self, columnFamily):
        #por cada columna, obtener el columnFamily y almacenarlo en una lista
        lista = []
        for column in self.columns:
            #si el columnFamily no esta en la lista, agregarlo
            if column.getColumnFamily() == columnFamily:
                #almacenar la version mas alta 
                lista.append(column.getVersiones()[-1].getVersion())
        if len(lista) == 0:
            return lista.append("No hay versiones para el columnFamily")
        return max(lista)
    
    def getColumnFamily(self):
        #por cada columna, obtener el columnFamily y almacenarlo en una lista
        lista = []
        for column in self.columns:
            #si el columnFamily no esta en la lista, agregarlo
            if column.getColumnFamily() not in lista:
                lista.append(column.getColumnFamily())

        if len(lista) == 0:
            return lista.append("No hay columnFamily")
        return lista

    def deleteVersion(self, clmID, columnFamily, column, version):
        for col in self.columns:
            if col.getClmID() == clmID and col.getColumnFamily() == columnFamily and col.getName() == column:
                for v in col.getVersiones():
                    if v.getVersion() == version:
                        col.getVersiones().remove(v)
                        self.metadata.updateLastMod()
                        return True
        return False
    
    def truncate(self):
        self.columns = []
        self.metadata.updateLastMod()
        self.metadata.setEnabled()

    def deleteAllVersions(self, clmID):
        for col in self.columns:
            if col.getClmID() == clmID:
                col.getVersiones().clear()
                self.metadata.updateLastMod()
                return True
        return False

    def getTableName(self):
        return self.tablename
    
    def getIndexRow(self):
        return self.indexRow
    
    def getColumns(self):
        return self.columns
    
    def getMetadata(self):
        return self.metadata
    
    def lastMod(self):
        self.metadata.updateLastMod()
