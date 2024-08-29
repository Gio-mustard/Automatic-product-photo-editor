from PIL import Image,ImageFilter
from PIL.Image import Resampling
from . history import History

def __check_history(im,id_mark_image,transform)->Image.Image|None:
    if History.has(
            id_mark_image=id_mark_image,
            transform=transform
    ): return im
    # En caso de que no se haya aplicado esta transformación a la mark image.
    History.push(
            id_mark_image=id_mark_image,
            transform=transform
        )

def __print_kwargs_alert_if_exist(transform,kwargs):
    if not kwargs == {}:print("-"*8,f'Los parámetros {kwargs=} de la transformación {transform=} NO ESTÁN SIENDO USADOS REVISA TU ALGORITMO!','-'*8,sep="\n")

def default(im:Image.Image,*args,**kwargs)->Image.Image:
    return im

def rotate(im:Image.Image,id_mark_image:str,deg:int=0,crop:bool=False,max_quality:bool=True,fillcolor:tuple = None,force:bool=False,**kwargs):
    """
    !IMPORTANTE\n
    No es necesario y no deberías pasar los siguiente parámetros...\n
    @im\n
    @id_mark_image\n
    Estos se pasaran de forma automática cuando se llame el método para hacer la trasformación\n
    Los @kwargs no tienen (por ahora) funcionalidad pero es necesario para no tener errores de argumentos en las transformaciones.
    """
    __print_kwargs_alert_if_exist(rotate,kwargs)
    if not force:
        returned = __check_history(im,id_mark_image,rotate)
        if isinstance(returned,Image.Image):return returned
    return im.rotate(
        angle=deg,
        resample=Resampling.BICUBIC if max_quality else Resampling.NEAREST,
        expand=1 if crop else 0,
        fillcolor= fillcolor
    )
def scale(im:Image.Image,id_mark_image,step:int,force:bool=False,**kwargs)->Image.Image:
    __print_kwargs_alert_if_exist(rotate,kwargs)
    if not force:
        returned = __check_history(im,id_mark_image,rotate)
        if isinstance(returned,Image.Image):return returned
    new_width,new_height = im.size
    new_width*=step
    new_height*=step
    return im.resize((int(new_width), int(new_height)),Resampling.BICUBIC)
# ! Hay que mover esto a otro modulo para reutilizarlo en el mark stack
def __get_alignments(horizontal:bool,vertical:bool,image_size:tuple,canvas_size:tuple)->tuple:
        # return a coordinates for star a drawing
        horizontal_alignment = (canvas_size[0]//2)-(image_size[0]//2) if horizontal else 0
        vertical_alignment = (canvas_size[1]//2)-(image_size[1]//2) if vertical else 0
        return (horizontal_alignment,vertical_alignment)


def out_shadow(im:Image.Image,id_mark_image:str,shadow_color:tuple=(0,0,0,255),crop:bool=False,radius:int=30,blur:int=5,offset:tuple=(0,0),force:bool=False,**kwargs)->Image.Image:
    """
    !IMPORTANTE\n
    No es necesario y no deberías pasar los siguiente parámetros...\n
    @im\n
    @id_mark_image\n
    Estos se pasaran de forma automática cuando se llame el método para hacer la trasformación\n
    Los @kwargs no tienen (por ahora) funcionalidad pero es necesario para no tener errores de argumentos en las transformaciones.
    """
    __print_kwargs_alert_if_exist(out_shadow,kwargs)
    if not force:
        returned = __check_history(im,id_mark_image,out_shadow)
        if isinstance(returned,Image.Image):return returned
    width,height = im.size
    # create a copy of main image but coloring all black pixels
    shadow = Image.composite(
        Image.new("RGBA",(width, height),shadow_color),
        Image.new("RGBA",(width, height),(0,0,0,0)),
        im
    )
    # create a canvas
    if not crop:
        width += (width // 10) + abs(offset[0])
        height += (height // 10) + abs(offset[1])
    
    canvas = Image.new("RGBA",(width, height),color=(0,0,0,0))
    # paste a shadow in canvas
    coordinates_shadow = __get_alignments(
         horizontal=True,
         vertical=True,
         image_size=shadow.size,
         canvas_size=canvas.size
    )
    canvas.paste(shadow,(coordinates_shadow[0]+offset[0],coordinates_shadow[1]+offset[1]),mask=shadow)
    # blur shadow
    for _ in range(blur):
        canvas = canvas.filter(ImageFilter.BoxBlur(radius))
    # paste main image
    canvas.paste(im,coordinates_shadow,mask=im)
    return canvas