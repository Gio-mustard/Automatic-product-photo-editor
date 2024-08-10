from constants import StackOptions
from django.test import TestCase
import classes
from PIL import Image
from scaling_funtions import scaling_object
from datetime import time
from transforms import rotate
# Create your tests here.
# * No son test bien hechos, pido perdón...
# ! test de MarkImage
with open("test.jpg",'rb') as file:
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
mark_image.set_transform(
    rotate,
    deg=18
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
    gap=0,
    alignment_in = {StackOptions.VERTICAL},
    direction=StackOptions.HORIZONTAL,
    scaling_function=scaling_object.contain
)
mark_stack.make_stack().show(time().minute)