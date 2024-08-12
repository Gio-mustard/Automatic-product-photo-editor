from PIL import Image
from PIL.Image import Resampling
from history import History

def __check_history(im,id_mark_image,transform)->Image.Image|None:
    if History.has(
            id_mark_image=id,
            transform=rotate
    ): return im
    # En caso de que no se haya aplicado esta transformación a la mark image.
    History.push(
            id_mark_image=id,
            transform=rotate
        )

def default(im:Image.Image,**kwargs)->Image.Image:
    return im

def rotate(im:Image.Image,id_mark_image:str,deg:int=0,crop:bool=False,max_quality:bool=True,fillcolor:tuple = None):
    returned = __check_history(im,id_mark_image,rotate)
    if isinstance(returned,Image.Image):return returned
    return im.rotate(
        angle=deg,
        resample=Resampling.BICUBIC if max_quality else Resampling.NEAREST,
        expand=1 if crop else 0,
        fillcolor= fillcolor
    )