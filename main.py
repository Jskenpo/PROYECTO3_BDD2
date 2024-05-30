from objetos.data import Data
from objetos.columns import Column
from objetos.timestamp import Versiones
from objetos.metadata import Header

import persistencia.ReadAndWrite as rw

opcion = 0

data = []

def printMain():
    #clear a console
    #print("\033[H\033[J")
    menu = """
    1. Create Table
    2. Add Column
    3. scan
    4. Deshabilitar tabla
    5. Alter table --- (Agregar o quitar cf, cambio de indexrow, cambio version de version obj)                         (Valdez)
    6. Drop table --- (Borrar tabla si esta deshabilitada)                                                              (Manuel)
    8. Describe table --- (Mostrar metadata)                                                                            (Master)
    9. Put --- (Insertar y editar celdas)
    10. Delete --- (Borrar vercion o versiones)                                                                         (Sol)
    11. Count --- (Contar distinc clmID)                                                                                (Master)
    12. Truncate --- (chequeo de habilitada deshabilitad, forza deshabilitar y elimina versiones y vuelve a activar)    (Sol)
    13. Salir
    """

    print(menu)

"""

Row             Column+CELL
clm.clmID       column=cf:name, timestamp=versiones[-1], value=versiones[-1].value

"""

def printDropMenu():
    print("\033[H\033[J")
    print("1. Drop Normal")
    print("2. Drop All")

def printDeleteMenu():
    print("\033[H\033[J")
    print("1. Delete Normal")
    print("2. Delete All")
    print("3. Regresar")

def printJsons():
    #print("\033[H\033[J")
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
    print("\033[H\033[J")
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
    print("\033[H\033[J")
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
    print("\033[H\033[J")
    ftable = data[table]
    uniqueCLMID = ftable.uniqueCLMID()

    # imprimir de la manera anterior
    print("Row\t\t\tColumn+CELL")

    for id in uniqueCLMID:
        clm = ftable.getColumnsOfClmID(id)
        for c in clm:
            print(id, "\t\t\tcolumn=", c.getColumnFamily(), ":", c.getName(), ", timestamp=", c.getVersiones()[-1].getTimestamp(), ", value=", c.getVersiones()[-1].getValue())

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

while opcion != 13:
    printMain()
    opcion = int(input("Ingrese una opcion: "))

    if (opcion > 13 or opcion < 1):
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
        printTypeData()
        index = getIndextableData(table)
        printTable(index)
        print("-------------------")
        print("Tabla mostrada")
        print("-------------------")

    elif opcion == 4:
        table = readJson()
        index = getIndextableData(table)
        data[index].getMetadata().setDisabled()
        rw.updateJson(data[index])
        print("-------------------")
        print("Tabla deshabilitada")
        print("-------------------")

    elif opcion == 5:
        print("-------------------")
        print("Alter table")
        print("-------------------")

    elif opcion == 6:
        print("-------------------")
        print("Drop table")
        print("-------------------")
        printDropMenu()
        type = int(input("Ingrese la opcion a realizar: "))
        if type == 1:
            table = readJson()
            index = getIndextableData(table)
            
            rw.deleteJson(table, data[index].getMetadata().getEnabled())    

    elif opcion == 10:
        printDeleteMenu()
        print("-------------------")
        print("Delete")
        print("-------------------")
        while opcion != 3:
            opcion = int(input("Ingrese una opcion: "))
            if opcion == 1:
                print("-------------------")
                print("Version eliminada")
                print("-------------------")
            elif opcion == 2:
                print("-------------------")
                print("Versiones eliminadas")
                print("-------------------")
            elif opcion == 3:
                print("-------------------")
                print("Regresando")
                print("-------------------")
    
    elif opcion == 12:
        print("-------------------")
        print("Truncate")
        print("-------------------")
        truncateTable()

    elif opcion == 13:
        print("-------------------")
        print("Saliendo")
        print("-------------------")
