from objetos.data import Data
from objetos.columns import Column
from objetos.timestamp import Versiones
from objetos.metadata import Header

import persistencia.ReadAndWrite as rw

from datetime import datetime
import os

opcion = 0

data = []

def printMain():
    #clear a console
    
    menu = """
    1. Create Table
    2. Add Column
    3. scan
    4. Habilitar/Deshabilitar tabla
    5. Alter table
    6. Drop table
    7. Describe table 
    8. Put
    9. Delete
    10. Count
    11. Truncate
    12. Salir
    """

    print(menu)

"""

Row             Column+CELL
clm.clmID       column=cf:name, timestamp=versiones[-1], value=versiones[-1].value

"""

def printDropMenu():
    print("1. Drop All")
    print("2. Regresar")

def printDeleteMenu():
    print("1. Delete Normal")
    print("2. Delete All")
    print("3. Regresar")

def printJsons():
    jsons = rw.getJsonNames()
    count = 1
    for j in jsons:
        name = j.split(".")
        print(count,".- ", name[0])
        count += 1

def readJson():
    printJsons()
    file = input("Ingrese el nombre del archivo: ")
    jsonData = rw.readJson(file=file)
    
    # Procesar columnas
    columnas = jsonData["columns"]
    clm = []
    for c in columnas:
        vrs = []
        for v in c["versiones"]:
            vrs.append(Versiones(v["value"], v["timestamp"], v["version"]))
        clm.append(Column(c["clmID"], c["name"], c["type"], c["columnFamily"], vrs))
    
    # Procesar metadata correctamente
    metadata = jsonData["metadata"]
    mtd = Header(name=metadata["name"], ultimaMod=metadata["ultimaMod"], enabled=metadata["enabled"])
    
    # Crear instancia de Data y agregarla a la lista
    data.append(Data(jsonData["tablename"], jsonData["indexRow"], clm, mtd))
    return file




def printTypeData():
    print("Tipos de datos")
    print("1. String")
    print("2. Int")
    print("3. Float")
    print("4. Bool")

def inputString():
    return input("Ingrese el valor de la columna: ")

def inputInt():
    return int(input("Ingrese el valor de la columna: "))

def inputFloat():
    return float(input("Ingrese el valor de la columna: "))

def inputBool():
    return bool(input("Ingrese el valor de la columna: "))

switch = {
    1: inputString,
    2: inputInt,
    3: inputFloat,
    4: inputBool
}

def runSwitch(opcion):
    return switch.get(opcion,1)()

def printData():
    count = 1
    for d in data:
        print(count, "Tabla: ", d.getTableName())
        print("Columnas: ")
        for c in d.getColumns():
            print("Nombre: ", c.getName())
            print("Tipo: ", c.getType())
            print("Valor: ", c.getValue())
            for t in c.getTimestamp():
                print("Timestamp: ", t.getTimestamp())
                print("Version: ", t.getVersion())
        print("Column Family: ", d.getColumnFamily())
        print("Metadata: ")
        print("Nombre: ", d.getMetadata().getName())
        print("Ultima modificacion: ", d.getMetadata().getUltimaMod())
        print("Enabled: ", d.getMetadata().getEnabled())

def printTable(table):
    ftable = data[table]
    uniqueCLMID = ftable.uniqueCLMID()

    # imprimir de la manera anterior
    print("Row\t\t\tColumn+CELL")

    for id in uniqueCLMID:
        clm = ftable.getColumnsOfClmID(id)
    
        for c in clm:
            try:
                print(id, "\t\t\tcolumn=", c.getColumnFamily(), ":", c.getName(), ", timestamp=", c.getVersiones()[-1].getTimestamp(), ", value=", c.getVersiones()[-1].getValue())
            except:
                print("No hay versiones")
      

    while True:
        print("1. Volver")
        opcion = int(input("Ingrese una opcion: "))
        if opcion == 1:
            break

def getIndextableData(table):
    count = 1
    for d in data:
        if d.getTableName() == table:
            return count-1
        count += 1
    
def printPutMenu():
    print("1. Insertar")
    print("2. Editar")
    print("3. Volver")

    return int(input("Ingrese una opcion: "))

def printColumnFamily(table):
    unique = data[table].uniqueCLMID()
    count = 1
    for u in unique:
        print(count, ".- ", u)
        count += 1

    return (int(input("Ingrese una opcion: ")), unique[count-1])
def alterTable(table_index):
    table_index = next((i for i, d in enumerate(data) if d.getTableName() == table_index), None)
    
    if table_index is None:
        print("El archivo especificado no existe. Por favor, asegúrate de ingresar un nombre de archivo válido.")
        return
    
    table = data[table_index]
    old_table_name = table.getTableName()  
    
    print("1. Editar nombre de la tabla")
    print("2. Crear nueva column family")
    print("3. Eliminar una column family")
    print("4. Editar el nombre en la metadata")
    option = int(input("Seleccione una opción: "))

def deleteVersion():
    table = readJson()
    index = getIndextableData(table)
    if index is not None:
        clmID = input("Ingrese el Column ID: ")
        columnFamily = input("Ingrese el Column Family: ")
        column = input("Ingrese el nombre de la columna: ")
        version = int(input("Ingrese la version a borrar: "))
        if data[index].deleteVersion(clmID, columnFamily, column, version):
            rw.updateJson(data[index])
            print("Version eliminada")
        else:
            print("No se encontro la version")

def deleteAll():
    table = readJson()
    index = getIndextableData(table)
    if index is not None:
        clmID = input("Ingrese el Column ID: ")
        if data[index].deleteAllVersions(clmID):
            rw.updateJson(data[index])
            print("Todas las versiones eliminadas")
        else:
            print("No se encontro el columnID")
    
def alterTable(table_index):
    table_index = next((i for i, d in enumerate(data) if d.getTableName() == table_index), None)
    
    if table_index is None:
        print("El archivo especificado no existe. Por favor, asegúrate de ingresar un nombre de archivo válido.")
        return
    
    table = data[table_index]
    old_table_name = table.getTableName()  
    
    print("1. Editar nombre de la tabla")
    print("2. Crear nueva column family")
    print("3. Eliminar una column family")
    print("4. Editar el nombre en la metadata")
    option = int(input("Seleccione una opción: "))
    
    if option == 1:
        new_table_name = input("Ingrese el nuevo nombre de la tabla: ")
        new_table = Data(new_table_name, table.getIndexRow(), table.getColumns(), table.getMetadata())
        data[table_index] = new_table
        table.getMetadata().updateName(new_table_name)
        rw.updateJson(new_table)
        
        old_file_path = os.path.join(os.getcwd(), f"{old_table_name}.json")
        print(f"Intentando eliminar el archivo antiguo: {old_file_path}")
        try:
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
                print(f"Archivo {old_file_path} eliminado correctamente.")
            else:
                print(f"El archivo {old_file_path} no existe.")
        except Exception as e:
            print(f"Error al intentar eliminar el archivo {old_file_path}: {str(e)}")            
    elif option == 2:
        new_column_family = input("Ingrese el nombre de la nueva column family: ")
        table = data[table_index]
        if any(column.getColumnFamily() == new_column_family for column in table.getColumns()):
            print("La columna familia ya existe en la tabla.")
            return
        else:
            new_column_name = input("Ingrese el nombre de la nueva columna: ")
            new_column_type = input("Ingrese el tipo de dato de la nueva columna: ")
            new_column_value = input("Ingrese el valor de la nueva columna: ")
            new_column_clmID = input("Ingrese el clmID de la nueva columna: ")
            new_column = Column(new_column_clmID, new_column_name, new_column_type, new_column_family, [
                Versiones(new_column_value, datetime.now().isoformat(), 1)
            ])
            table.getColumns().append(new_column)
            rw.updateJson(table)
            print("Nueva columna familia creada y columna agregada con éxito.")
    elif option == 3:
        column_family_to_delete = input("Ingrese el nombre de la column family a eliminar: ")
        table = data[table_index]
        for column in table.getColumns():
            if column.getColumnFamily() == column_family_to_delete:
                table.getColumns().remove(column)
        rw.updateJson(table)
    elif option == 4:
        new_metadata_name = input("Ingrese el nuevo nombre de metadatos: ")
        table.getMetadata().updateName(new_metadata_name)
        rw.updateJson(table)

def truncateTable():
    table = readJson()
    index = getIndextableData(table)
    if index is not None:
        print(f"Truncating '{table}' table (it may takes a while):")
        print(" - Disabling table...")
        data[index].getMetadata().setDisabled()
        rw.updateJson(data[index])

        print(" - Truncating table...")
        data[index].truncate()
        rw.updateJson(data[index])

        print(f"Table '{table}' truncated successfully.")


while opcion != 12:
    printMain()
    opcion = int(input("Ingrese una opcion: "))

    if (opcion > 12 or opcion < 1):
        print("-------------------")
        print("Opcion incorrecta")
        print("-------------------")
    elif opcion == 1:
        tablename = input("Ingrese el nombre de la tabla: ")
        table = Data(tablename, len(data)+1)
        data.append(table)
        rw.write_json(table)
        print("-------------------")
        print("Tabla creada")
        print("-------------------")

    elif opcion == 2:
        table = readJson()
        printTypeData()
        type = int(input("Ingrese el tipo de dato: "))
        value = runSwitch(type)
        if type == 1:
            type = "String"
        elif type == 2:
            type = "Int"
        elif type == 3:
            type = "Float"
        elif type == 4:
            type = "Bool"
        name = input("Ingrese el nombre de la columna: ")
        columnFamily = input("Ingrese el columnFamily: ")
        clmID = input("Ingrese el Column ID: ")
        index = getIndextableData(table)
        data[index].addColumn(clmID,name, type, value, columnFamily)
        data[index].getMetadata().updateLastMod()
        rw.updateJson(data[index])
        print("-------------------")
        print("Columna agregada")
        print("-------------------")

    elif opcion == 3:
        table = readJson()
        index = getIndextableData(table)
        printTable(index)
        print("-------------------")
        print("Tabla mostrada")
        print("-------------------")

    elif opcion == 4:
        table = readJson()
        index = getIndextableData(table)
        if data[index].getMetadata().getEnabled() == True:
            data[index].getMetadata().setDisabled()
            rw.updateJson(data[index])
            print("-------------------")
            print("Tabla deshabilitada")
            print("-------------------")
        else:
            data[index].getMetadata().setEnabled()
            rw.updateJson(data[index])
            print("-------------------")
            print("Tabla habilitada")
            print("-------------------")

    elif opcion == 5:
        table_index = readJson()
        alterTable(table_index)
        print("-------------------")
        print("Alter table")
        print("-------------------")
    elif opcion == 6:
        print("-------------------")
        print("Drop table")
        print("-------------------")
        printDropMenu()
        type = int(input("Ingrese la opcion a realizar: "))
        while type != 2:
            if type == 1:
                table = readJson()
                index = getIndextableData(table)
                rw.deleteJson(table, data[index].getMetadata().getEnabled())
                print("-------------------")
                back = input("Desea regresar al menu principal? (s/n): ")
                if back == "s":
                    break
            elif type == 2:
                break

    elif opcion == 7:
        table = readJson()
        index = getIndextableData(table)
        print("-------------------")
        print("Nombre de la tabla: ", data[index].getTableName())
        print("Ultima modificacion: ", data[index].getMetadata().getUltimaMod())
        print("Enabled: ", data[index].getMetadata().getEnabled())
        columnF =  data[index].getColumnFamily()
        for column in columnF:
            print("Column Family: ", column)
            version = data[index].getVersionOfCF(column)
            print("Version: ", version)
        print("-------------------")
    
    elif opcion == 8:
        # put
        table = readJson()
        index = getIndextableData(table)
        printTable(index)
        rowId = input("Ingrese el Row ID (Presione exit si no hay): ")
        if rowId == "exit":
            continue
        cf = input("Ingrese el Column Family: ")
        value = input("Ingrese el valor: ")
        column = data[index].checkClm(cf, rowId)
        column.addVersiones(datetime.now().isoformat(), int(column.getVersiones()[-1].getVersion())+1, value)
        data[index].getMetadata().updateLastMod()
        rw.updateJson(data[index])
        
    elif opcion == 9:
        print("-------------------")
        print("Delete")
        print("-------------------")
        while opcion != 3:
            printDeleteMenu()
            opcion = int(input("Ingrese una opcion: "))
            if opcion == 1:
                print("-------------------")
                print("Delete")
                print("-------------------")
                deleteVersion()
            elif opcion == 2:
                print("-------------------")
                print("Delete All")
                print("-------------------")
                deleteAll()
            elif opcion == 3:
                print("-------------------")
                print("Regresando")
                print("-------------------")
                

    elif opcion == 10:
        table = readJson()
        index = getIndextableData(table)
        
        print("-------------------")
        print("Cantidad de filas en la tabla: ", len(data[index].uniqueCLMID()))
        print("-------------------")

    elif opcion == 11:
        print("-------------------")
        print("Truncate")
        print("-------------------")
        truncateTable()

    elif opcion == 12:
        print("-------------------")
        print("Saliendo")
        print("-------------------")
