from uuid import uuid4
from rembg import remove
from PIL import Image,ImageEnhance
from io import BytesIO

class MarkImage(object):
    """
    Esta clase encapsula y abstrae los métodos principales de edición automática de imágenes (solo es una imagen)
    """
    def __init__(self, bytes_image: bytes,bg_color:tuple[float|int]=(255,255,255,255),transform=None) -> None:
        """
        @property __image : la imagen cruda del objeto
        @property __bg_color : la imagen creada con el color dado , esta se usara por detrás de __image
        @property __enhanced_image : es la __image pero resaltada para facilitar la visualización del objeto principal de la imagen (por ahora solo sirve para quitar el fondo de una imagen, se usa como una mascara de recorte).
        @id : solo es un identificador del objeto.
        ### TODO : aun no esta implementada.
        ! @property __transform : una función de trasformación aplicable solo a __image en el estado actual de la misma.
        """
        self.__image = self.__load_bytes(bytes_image)
        self.__bg_color:tuple
        self.set_bg(bg_color)
        self.id = uuid4()
        self.__transform = transform
        self.__enhanced_image = None

    #* validators
    def __validate_bg_color(self, bg_color:tuple[float|int])->bool|Exception:
        # TODO: Hay que crear Excepciones propias para la clase.
        """
        Valida que los canales del color estén en el rango de 8 bits y que tenga 4 canales.
        @param bg_color tuple[R,G,B,A] : El color de fondo para la imagen principal. 
        @raises Exception: se invoca cuando la tupla de colores no tiene los 4 canales o no esta en el rango de 8 bits. 
        """
        if not len(bg_color) == 4: raise Exception("bg_color without 4 color channels")
        RANGE_COLORS = range(0,256)
        for index,channel in enumerate(bg_color):
            if not channel in RANGE_COLORS:
                raise Exception(f"Color in index {index} is not in 8 bits range")
        return True

    #* background methods
    def set_bg(self, new_bg_color:tuple[float|int])->None:
        """
        valida y establece el nuevo color de fondo crean do una imagen solida.
        @param new_bg_color:color tuple [R,G,B,A]
        """
        color_correct = self.__validate_bg_color(new_bg_color)
        if color_correct is True:
            self.__bg_color = Image.new("RGBA", self.__image.size,new_bg_color)
        
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

    #* main image methods
    def __load_bytes(self, bytes_image: bytes)->Image.Image:
        """
        lee y retorna los bytes en una nueva imagen.
        """
        return Image.open(BytesIO(bytes_image))

    #* transform main image methods
    def set_transform(self, new_transform):pass

    def apply_transform(self):pass

    #* enhanced image methods
    def __enhance_image(self) -> Image.Image:
        """
        resalta la imagen actual '__image' y la guarda en la propiedad __enhance_image
        por ahora solo sube el brillo de la imagen y la convierte en escala de graces
        """
        enhancer = ImageEnhance.Brightness(self.__image.convert('L'))
        brightness_factor = 2.2
        self.__enhanced_image = enhancer.enhance(brightness_factor)
        return self.__enhanced_image

    #* object methods
    def copy(self):
        # retorna una copia del objeto en su estado actual
        return MarkImage(
            bytes_image=self.__image.tobytes(),
            importance=self.importance,
        )

    def _show_image(self)->None:
        """
        muestra la imagen en una ventana de visualización de imágenes (funciona incluso después de la finalización del script)\n
        !no debería de usarse solo ES DE PRUEBA
        """
        self.__image.show(f"{self.id}")

    def __str__(self)->str:
        return f"{self.__image}"
    
    def to_bytes(self)->bytes:
        return self.__image.tobytes()