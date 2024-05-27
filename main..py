from objetos.data import Data

opcion = 0

data = []

def printMain():
    menu = """
    1. Create Table
    2. Add Column
    3. Mostrar Tabla
    4. Salir
    """

    print(menu)

def printData():
    for (d, i) in data:
        print(i, "Tabla: ", d.getTableName())
        print("Columnas: ")
        for c in d.getColumns():
            print("Nombre: ", c.getName())
            print("Tipo: ", c.getType())
            print("Valor: ", c.getValue())
            print("Timestamp: ", c.getTimestamp())
            print("Version: ", c.getTimestamp().getVersion())
        print("Column Family: ", d.getColumnFamily())
        print("Metadata: ", d.getMetadata())

def printColumns():
    for (d, i) in data:
        print(i, "Tabla: ", d.getTableName())

while opcion != 4:
    printMain()
    opcion = int(input("Ingrese una opcion: "))

    if (opcion > 4 or opcion < 1):
        print("-------------------")
        print("Opcion incorrecta")
        print("-------------------")
    elif opcion == 1:
        tablename = input("Ingrese el nombre de la tabla: ")
        columnFamily = input("Ingrese el columnFamily: ")
        data.append(Data(tablename, len(data), columnFamily))
        print("-------------------")
        print("Tabla creada")
        print("-------------------")

    elif opcion == 2:
        printColumns()
        index = int(input("Ingrese el index de la tabla: "))
        name = input("Ingrese el nombre de la columna: ")
        type = input("Ingrese el tipo de la columna: ")
        value = input("Ingrese el valor de la columna: ")
        data[index].addColumn(name, type, value)
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
