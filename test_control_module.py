from control.constants import StackOptions
from django.test import TestCase
from control import classes
from PIL import Image
from control.scaling_funtions import scaling_object
from control.transforms import *
import time
start = time.time()
# Create your tests here.
# * No son test bien hechos, pido perdón...
# ! test de MarkImage
with open("test2.jpg",'rb') as file:
    bytes_image = file.read()

mark_image = classes.MarkImage(
    initial_image=bytes_image,
    bg_color=(0,0,0,0)
)
mark_image.remove_background()
# MarkStack testing
background = Image.new(
    mode="RGBA",
    size=(1750,1450),
    color=(252, 195, 38,255)
)
mark_image.set_transform(auto_crop)()
mark_image.set_transform(
    out_shadow,
    blur=10,
    radius=20,
    shadow_color=(0,0,0,255),
    offset=(0,30),
)
mark_image.apply_transform()

mark_image_2 = mark_image.copy()
mark_image_3 = mark_image.copy()
mark_image_4 = mark_image.copy()
mark_image_5 = mark_image.copy()

images = [
    mark_image,
    mark_image_2,
    mark_image_3,
]
mark_stack = classes.MarkStack(
    images=images,
    background=background,
    padding=0,
    gap=-400,
    alignment_in = {StackOptions.VERTICAL},
    direction=StackOptions.HORIZONTAL,
    scaling_function=scaling_object.contain
)
def callback(im:Image.Image,id:str,index:int,num_images:int)->Image.Image:
    image_transformed  = im
    if index == 0:
        image_transformed = rotate(im,id,25,True,force=True)
    elif index == num_images-1:
        image_transformed = rotate(im,id,-25,True,force=True)
    return image_transformed


image = mark_stack.make_stack(callback,main_index = 1)
print(image)
image.save('prueba.png')
end = time.time()

# print the execution time
print(f"Execution time of the program is {(end - start)}s")