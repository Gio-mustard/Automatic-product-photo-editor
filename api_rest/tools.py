import json
import base64
from django.core.files.uploadedfile import TemporaryUploadedFile,InMemoryUploadedFile

def convert_bytes_to_string(b:bytes,encoding:str='utf-8')->str:
    return base64.b64encode(b).decode(encoding)


def custom_decoder(dct)->dict:
    # TODO: hay parametrizar la bússqueda para convertir cualquier sub objeto.
    if 'background_color' in dct:
        dct['background_color'] = [int(num) for num in dct['background_color']]
    return dct

def json_to_dict(json_string)->dict:
    """
    Convierte un string en formato JSON a un diccionario de Python.
    
    Args:
        json_string (str): El string en formato JSON a convertir.
        
    Returns:
        dict: El diccionario de Python resultante de la conversión.
    """
    try:
        python_dict = json.loads(json_string,parse_int=lambda number:int(number),object_hook=custom_decoder)
        return python_dict
    except json.JSONDecodeError as e:
        print(f"Error al decodificar el JSON: {e}")
        return None

def fix_request_types(data:dict)->dict:
    new_data = {}
    for k,v in data.items():
        new_data[k] = v
        if (type(v[0]) in [TemporaryUploadedFile,InMemoryUploadedFile]):continue
        if v[0] == 'false' or v[0] == 'true':
            new_data[k] =   'true' in v[0]
            continue
        
        if v[0].startswith('{') and v[0].endswith('}'):
            new_data[k] = json_to_dict(v[0])
            continue

        if v[0].isalnum():
            new_data[k] = float(v[0])

    return new_data