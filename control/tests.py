from constants import VERTICAL,HORIZONTAL
from django.test import TestCase
import classes
from PIL import Image

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
    size=(2000,2000),
    color=(252, 195, 38,255)
)
mark_image_2 = mark_image.copy()

images = [
    mark_image,
    mark_image_2
]

mark_stack = classes.MarkStack(
    images=images,
    background=background,
    padding=100,
    gap=-100,
    alignment_in = {VERTICAL,HORIZONTAL},
    direction=HORIZONTAL
)
mark_stack.make_stack().show()