from uuid import uuid4
from rembg import remove
from PIL import Image, ImageEnhance
from io import BytesIO
from constants import StackOptions
from scaling_funtions import scaling_object
from transforms import default
class MarkImage(object):
    """
    Esta clase encapsula y abstrae los métodos principales de edición automática de imágenes (solo es una imagen)
    """

    def __init__(self, initial_image: bytes | Image.Image, bg_color: tuple[float | int] = (255, 255, 255, 255), transform=None) -> None:
        """
        @property __image : la imagen cruda del objeto
        @property __bg_color : la imagen creada con el color dado , esta se usara por detrás de __image
        @property __enhanced_image : es la __image pero resaltada para facilitar la visualización del objeto principal de la imagen (por ahora solo sirve para quitar el fondo de una imagen, se usa como una mascara de recorte).
        @id : solo es un identificador del objeto.
        ### TODO : aun no esta implementada.
        ! @property __transform : una función de trasformación aplicable solo a __image en el estado actual de la misma.
        """
        self.__check_types(
            initial_image
        )
        self.__image = self.__load_image(initial_image)
        self.__bg_color: tuple
        self.set_bg(bg_color)
        self.id = uuid4()
        self.__transform = transform
        self.__enhanced_image = None
        self.set_transform(default,any=None)

    # * validators
    def __check_types(self, initial_image) -> None:
        initial_image_type = type(initial_image)
        if (initial_image_type != Image.Image) and (initial_image_type != bytes):
            raise TypeError(
                f"initial_image must be Image or raw bytes you have this : {initial_image_type}.")

    def __validate_bg_color(self, bg_color: tuple[float | int]) -> bool | Exception:
        # TODO: Hay que crear Excepciones propias para la clase.
        """
        Valida que los canales del color estén en el rango de 8 bits y que tenga 4 canales.
        @param bg_color tuple[R,G,B,A] : El color de fondo para la imagen principal.
        @raises Exception: se invoca cuando la tupla de colores no tiene los 4 canales o no esta en el rango de 8 bits.
        """
        if not len(bg_color) == 4: raise Exception(
            "bg_color without 4 color channels")
        RANGE_COLORS = range(0, 256)
        for index, channel in enumerate(bg_color):
            if not channel in RANGE_COLORS:
                raise Exception(
                    f"Color in index {index} is not in 8 bits range")
        return True

    # * background methods
    def set_bg(self, new_bg_color: tuple[float | int]) -> None:
        """
        valida y establece el nuevo color de fondo crean do una imagen solida.
        @param new_bg_color:color tuple [R,G,B,A]
        """
        color_correct = self.__validate_bg_color(new_bg_color)
        if color_correct is True:
            self.__bg_color = Image.new(
                "RGBA", self.__image.size, new_bg_color)

    def remove_background(self) -> None:
        """
        elimina el fondo y actualiza la imagen actual.
        """
            # Se usa la enhanced_image para sea mas fácil reconocer el objeto principal de la imagen.
        # se elimina el fondo de la enhanced_image para después usarla como mascara de recorte en la imagen principal y se le coloca el color de fondo por detrás.
        enhanced_image = self.__enhance_image()
        enhanced_image_without_bg = remove(enhanced_image)
        self.__image = Image.composite(
            self.__image,
            self.__bg_color,
            enhanced_image_without_bg)

    # * main image methods
    def __load_bytes(self, bytes_image: bytes) -> Image.Image:
        """
        lee y retorna los bytes en una nueva imagen.
        """
        return Image.open(BytesIO(bytes_image))

    def __load_image(self, image: Image.Image | bytes) -> Image.Image:
        if type(image) == Image.Image:
            return image
        return self.__load_bytes(image)

    # * transform main image methods
    def set_transform(self, new_transform,**kwargs):
        self.__transform = (new_transform,kwargs)

    def apply_transform(self):
        params = self.__transform[1]
        transform = self.__transform[0]
        self.__image = transform(im=self.__image, **params)

    # * enhanced image methods
    def __enhance_image(self) -> Image.Image:
        """
        resalta la imagen actual '__image' y la guarda en la propiedad __enhance_image
        por ahora solo sube el brillo de la imagen y la convierte en escala de graces
        """
        enhancer = ImageEnhance.Brightness(self.__image.convert('L'))
        brightness_factor = 2.2
        self.__enhanced_image = enhancer.enhance(brightness_factor)
        return self.__enhanced_image

    # * object methods
    def copy(self):
        # retorna una copia del objeto en su estado actual
        return MarkImage(
            initial_image=self.__image.copy(),
        )

    def _show_image(self) -> None:
        """
        muestra la imagen en una ventana de visualización de imágenes (funciona incluso después de la finalización del script)\n
        !no debería de usarse solo ES DE PRUEBA
        """
        self.__image.show(f"{self.id}")

    def to_image(self) -> Image.Image:
        return self.__image

    def __str__(self) -> str:
        return f"{self.__image}"

    def to_bytes(self) -> bytes:
        return self.__image.tobytes()

class MarkStack:
    def __init__(self, images: tuple[MarkImage], background: Image.Image, padding: int = 10, gap: int = 10,alignment_in:set= (None,None),direction:int=StackOptions.HORIZONTAL,scaling_function=None):
        """
        @param alignment_in: tuple(HORIZONTAL,VERTICAL) constants from constants.py
        @param direction: HORIZONTAL || VERTICAL constants from constants.py
        """
        self._images = images
        self.__background = background
        self.__padding = padding  # in pixels
        self.__gap = gap  # in pixels
        self.__alignment_in = alignment_in
        self.__direction = direction
        self.__scaling_function = None
        self.__scaling_options = None
        self.__canvas_size = tuple()
        self.__calculate_and_update_canvas_size()
        
        self.scaling_function = scaling_object.initial if scaling_function == None  else scaling_function

    # canvas size
    def __calculate_and_update_canvas_size(self):
        width,height = self.__background.size
        width -= (self.__padding * 2)
        height -= (self.__padding * 2)
        match self.__direction:
            case StackOptions.HORIZONTAL:
                width -= self.__gap * (len(self._images) - 1)
            case StackOptions.VERTICAL:
                height -= self.__gap * (len(self._images) - 1)

        self.__canvas_size = (width,height)

    # background
    @property
    def background(self) -> Image.Image:
        return self.__background

    @background.setter
    def background(self, new_background):
        if type(new_background) != Image.Image: raise TypeError(
            "El background solo puede ser de tipo Image")
        self.__calculate_and_update_canvas_size()
        self.__background = new_background

    # padding
    @property
    def padding(self) -> int:
        return self.__padding

    @padding.setter
    def padding(self, new_padding: int) -> None:
        if new_padding < 0: raise ValueError(
            "El padding no puede ser inferior a 0 pixeles")
        self.__padding = new_padding
        self.__calculate_and_update_canvas_size()

    # gap
    @property
    def gap(self) -> int:
        return self.__gap

    @gap.setter
    def gap(self, new_gap: int) -> None:
        self.__gap = new_gap
        self.__calculate_and_update_canvas_size()

    # orientation
    @property
    def direction(self)->str:
        return f"StackOptions in {'Vertical'if self.__orientation == StackOptions.VERTICAL else 'Horizontal'}"
    
    @direction.setter
    def direction(self, new_direction)->None:
        self.__direction = new_direction
        self.__calculate_and_update_canvas_size()

    # scaling
    @property
    def scaling_function(self):
        return self.__scaling_function
    
    @scaling_function.setter
    def scaling_function(self, new_scaling_function:tuple)->None:
        options_function,scaling_function = new_scaling_function()
        self.__scaling_options = options_function(self.__canvas_size,self._images,self.__direction)
        self.__scaling_function = scaling_function

    def get_image() -> MarkImage: pass  # ? Porque no se llama 'get_mark_image()'

    def __get_alignments(self,has_horizontal:bool,has_vertical:bool,current_image_size:tuple)->tuple:
        horizontal_alignment = (self.__background.size[0]//2)-(current_image_size[0]//2) if has_horizontal else 0
        vertical_alignment = (self.__background.size[1]//2)-(current_image_size[1]//2) if has_vertical else 0
        return (horizontal_alignment,vertical_alignment)

    def __get_coordinates(self,previous_coordinates,previous_image_size,alignment)->tuple:
        horizontal_alignment,vertical_alignment = alignment
        if previous_coordinates is None:
            return (horizontal_alignment+self.padding,vertical_alignment+self.padding) # TODO temporal: hay que agregar el alignment
        if self.__direction == StackOptions.HORIZONTAL:
            return (
                horizontal_alignment + (previous_coordinates[0] + previous_image_size[0] + self.__gap),
                vertical_alignment   + self.__padding
            )
        elif self.__direction == StackOptions.VERTICAL:
            return (
                horizontal_alignment + self.__padding,
                vertical_alignment   + (previous_coordinates[1] + previous_image_size[1]+ self.__gap)
            )
        
    # processing stack images
    def _paste_images(self)->None:
        """
        1. verificar padding 
        2. colocar primer imagen (se le aplica el transform si aun no lo tiene #TODO hay que implementar esto después)
        3. iterar 2.
        4. crear imagen resultante (tiene que ser separada a el background) #? o puede ser el background el canvas para colocar las imágenes 
        """
        # Aquí suponemos que se usara el background para ir colocando las imágenes
        previous_coordinates = None
        previous_image_size = None
        for mark_image in self._images:
            mark_image:MarkImage
            image = mark_image.to_image()
            image = self.__scaling_function(
                image,self.__scaling_options
            )
            alignment = self.__get_alignments(
                current_image_size=image.size,
                has_horizontal= StackOptions.HORIZONTAL in self.__alignment_in,
                has_vertical=StackOptions.VERTICAL in self.__alignment_in
            )
            coordinates = self.__get_coordinates(previous_coordinates,previous_image_size,alignment)
            self.__background.paste(
                im=image,
                box=coordinates,
                mask=image
                )
            previous_image_size = image.size
            previous_coordinates = coordinates
    
    def make_stack(self)->Image:
        self._paste_images()
        return self.__background