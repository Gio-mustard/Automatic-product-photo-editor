import json
import base64
from django.core.files.uploadedfile import TemporaryUploadedFile,InMemoryUploadedFile
from PIL import Image

def convert_bytes_to_string(b:bytes,encoding:str='utf-8')->str:
    return base64.b64encode(b).decode(encoding)


def custom_decoder(dct)->dict:
    # TODO: hay parametrizar la bússqueda para convertir cualquier sub objeto.
    if 'background_color' in dct:
        for index,color in enumerate(dct['background_color']):
            if type(color) in  (tuple,list):
                dct['background_color'][index] = [int(num) for num in color]
            else:
                dct['background_color'] = [int(num) for num in dct['background_color']]
                break
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
        
        if len(v) == 1 and not k =='background_image':
            new_data[k] = v[0]

    return new_data

def make_image_with_gradient(colors:tuple[int], width:int, height:int):
    """
    Crea una imagen de gradiente que transiciona a través de los colores proporcionados.

    Args:
    - colores (list): Lista de colores en formato RGB o RGBA.
    - ancho (int): Ancho de la imagen.
    - alto (int): Alto de la imagen.
    
    Returns:
    - PIL.Image: Imagen generada con el gradiente.
    """
    # Crear una nueva imagen en modo RGB
    image = Image.new("RGBA", (width, height))
    # Obtener el objeto de acceso a los píxeles
    pixeles = image.load()

    # Calcular el ancho de cada segmento de color
    segment_size = width // (len(colors) - 1)
    
    # Generar gradiente
    for i in range(len(colors) - 1):
        # Color inicial y final del segmento
        color_inicio = colors[i]
        color_fin = colors[i + 1]

        # Bucle para llenar los píxeles del segmento con el gradiente entre color_inicio y color_fin
        for x in range(i * segment_size, (i + 1) * segment_size):
            if x >= width:  # En caso de que el ancho no sea divisible por el número de segmentos
                break
            # Calcular la interpolación lineal para cada componente de color
            t = (x - i * segment_size) / segment_size
            r = int(color_inicio[0] + (color_fin[0] - color_inicio[0]) * t)
            g = int(color_inicio[1] + (color_fin[1] - color_inicio[1]) * t)
            b = int(color_inicio[2] + (color_fin[2] - color_inicio[2]) * t)
            a = int(color_inicio[3] + (color_fin[3] - color_inicio[3]) * t)

            # Llenar los píxeles verticales de la imagen
            for y in range (height):
                pixeles[x, y] = (r,g,b,a)
    return image