from objetos.data import Data
from objetos.columns import Column
from objetos.timestamp import Versiones
from objetos.metadata import Header

import persistencia.ReadAndWrite as rw

opcion = 0

data = []

def printMain():
    #clear a console
    print("\033[H\033[J")
    menu = """
    1. Create Table
    2. Add Column
    3. Mostrar Tabla
    4. Salir
    """

    print(menu)

def printJsons():
    print("\033[H\033[J")
    jsons = rw.getJsonNames()
    for j in jsons:
        name = j.split(".")
        print(name[0])

def readJson():
    printJsons()
    file = input("Ingrese el nombre del archivo: ")
    jsonData = rw.readJson(file= file)
    columnas = jsonData["columns"]
    clm = []
    metadata = jsonData["metadata"]
    mtd = []
    vrs = []
    for c in columnas:
        versiones = c["versiones"]
        for v in versiones:
            vrs.append(Versiones(v["value"], v["timestamp"], v["version"]))

        clm.append(Column(c["name"], c["type"], columnFamily=c["columnFamily"], versiones=vrs))
    mtd.append(Header(name=metadata["name"], ultimaMod=metadata["ultimaMod"], enabled=metadata["enabled"]))
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

def printTable():
    print("\033[H\033[J")
    count = 1
    for d in data:
        print(count, "Tabla: ", d.getTableName())
        count += 1

def getIndextableData(table):
    count = 1
    for d in data:
        if d.getTableName() == table:
            return count-1
        count += 1
    


while opcion != 4:
    printMain()
    opcion = int(input("Ingrese una opcion: "))

    if (opcion > 4 or opcion < 1):
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
        index = getIndextableData(table)
        print(index)
        print(data[index].getTableName())
        data[index].addColumn(name, type, value, columnFamily)
        rw.updateJson(data[index])
        print("-------------------")
        print("Columna agregada")
        print("-------------------")

    elif opcion == 3:
        printData()
        print("-------------------")
        print("Tabla mostrada")
        print("-------------------")

    elif opcion == 4:
        print("-------------------")
        print("Saliendo")
        print("-------------------")