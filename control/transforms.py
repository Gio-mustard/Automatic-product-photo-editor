from PIL import Image
from PIL.Image import Resampling

def default(im:Image.Image,**kwargs)->Image.Image:
    return im

def rotate(im:Image.Image,deg:int=0,crop:bool=False,max_quality:bool=True,fillcolor:tuple = None):
    return im.rotate(
        angle=deg,
        resample=Resampling.BICUBIC if max_quality else Resampling.NEAREST,
        expand=1 if crop else 0,
        fillcolor= fillcolor
    )