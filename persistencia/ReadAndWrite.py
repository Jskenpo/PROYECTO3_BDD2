import json
import os

def getJsonNames():
    json_files = [f for f in os.listdir('data') if f.endswith('.json')]
    return json_files

def readJson(file):
    path = os.path.join('data', f'{file}.json')
    with open(path, 'r') as f:
        return json.load(f)
    
def write_json(data):
    path = os.path.join('data', f'{data.getTableName()}.json')
    

    # Crear el directorio si no existe
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # Escribir la cadena JSON en el archivo
    with open(path, 'w') as f:
        json.dump(data.to_dict(), f, indent=4)

def updateJson(data):
    path = os.path.join('data', f'{data.getTableName()}.json')
    with open(path, 'w') as f:
        json.dump(data.to_dict(), f, indent=4)

def deleteJson(file, status):
    if status == False:
        path = os.path.join('data', f'{file}.json')
        os.remove(path)
        print("...Tabla eliminada correctamente...")
    else:
        print("...La tabla habilitada, no es posible eliminar...")


    