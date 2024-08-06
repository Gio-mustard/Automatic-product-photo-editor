from constants import StackOptions
from PIL import Image
"""
Para no tener que calcular aquí el gap y el padding podría
pre calcularlo cada que llame a un método de estos
o al instanciar cada mark stack podría tener una propiedad
con el size ya calculado del "free space" del background , ese 
"free space" del background podría ser lo que llamamos canvas.

? Como se calcula el gap 
* Multiplicando la cantidad de imágenes por el gap y retándolo del width o height del canvas según sea el caso.
"""
class ScalingFunctions:

    """
    # Initial
    Mantiene las dimensiones originales de cada imagen sobre el canvas, no se aplica ninguna transformación para su escalamiento.
    * No hace nada pero tiene que existir una función para hacer mas simple el algoritmo para aplicar las funciones de escalamiento
    """
    @classmethod
    def initial(cls)->tuple:
        return (lambda *n : None,lambda image,resize_options : image)

    """
    # Contain
    Calcula a cuanto tiene que redimencionar cada imagen para que todas las imágenes quepan (sean visibles) en el mark stack.
    """
    @classmethod
    def __get_contain_options(cls,canvas_size:tuple[int],images:tuple,direction:StackOptions):
        width,height = canvas_size
        max_width = None
        max_height = None
        len_images = len(images)
        match direction:
            # Calc in px
            case StackOptions.HORIZONTAL:
                max_width = width//len_images
            case StackOptions.VERTICAL:
                max_height = height//len_images

        return (max_width,max_height,len_images)
    
    @classmethod
    def __contain_scaling(cls,image:Image.Image,resize_options:tuple[int|None]):
        # ! se esta trabajando con la referencia original de la imagen
        new_width,new_height,len_image = resize_options
        width,height = image.size
        if new_height == None:
            # el with ya esta calculado, solo falta calcular la nueva escala del height ya que actualmente su valor es 'None'
            new_height = int((new_width/ width) * height)
        
        elif new_width == None:
            new_width = int((new_height/ height) * width)
        return image.resize(
            (new_width,new_height),
        )
    
    @classmethod
    def contain(cls)->tuple:
        return (cls.__get_contain_options,cls.__contain_scaling)

    """
    # cover
    En caso de que el canvas sea mas grande que las imágenes se les hará un sobre dimensionamiento para que cada imagen ocupe el 100% del height o width del canvas pero nunca los 2 a la vez.

    -> Como se sabe si se ocupara el 100% del height o width del canvas ??
    La dimension seleccionada para el sobre dimensionamiento sera la dimension mas chica, por ejemplo, si el canvas mide 500x200 las imágenes ocuparan el 100%  del height y el width de cada imagen crecerá según s escala original.
    """

    @classmethod
    def __get_cover_options(cls,canvas_size:tuple[int],images:tuple,direction:StackOptions):
        width,height = canvas_size
        return (width,height,direction)
    
    @classmethod
    def __cover_scaling(cls,image:Image.Image,resize_options:tuple[int|None])->tuple[int]:
        width_canvas,height_canvas,direction = resize_options
        new_width,new_height = (None,None)
        width,height = image.size

        if (width_canvas < height_canvas and direction == StackOptions.HORIZONTAL):
            new_width = width_canvas
            new_height = int((new_width/ width) * height)
        else:
            new_height = height_canvas
            new_width = int((new_height/ height) * width)
        
        return image.resize(
            (new_width,new_height)
        )

    @classmethod
    def cover(cls)->tuple:
        return (cls.__get_cover_options,cls.__cover_scaling)

scaling_object = ScalingFunctions()