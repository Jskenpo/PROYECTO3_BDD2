from objetos.data import Data
from objetos.columns import Column
from objetos.timestamp import Versiones
from objetos.metadata import Header
from datetime import datetime
import persistencia.ReadAndWrite as rw
import os
opcion = 0

data = []

def printMain():
    #clear a console
    print("\033[H\033[J")
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

def printJsons():
    print("\033[H\033[J")
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



def getIndextableData(table):
    count = 1
    for d in data:
        if d.getTableName() == table:
            return count-1
        count += 1
    


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
        if type == 1:
            table = readJson()
            index = getIndextableData(table)
            
            rw.deleteJson(table, data[index].getMetadata().getEnabled())    

    elif opcion == 13:
        print("-------------------")
        print("Saliendo")
        print("-------------------")
