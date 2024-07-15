from django.test import TestCase
import classes
from PIL import Image

# Create your tests here.
# * No son test bien hechos, pido perdón...
# ! test de MarkImage
with open("test.jpg",'rb') as file:
    bytes_image = file.read()

mark_image = classes.MarkImage(
    bytes_image=bytes_image,
    bg_color=(0,0,0,0)
)
mark_image.remove_background()
# MarkStack testing
background = Image.new(
    mode="RGBA",
    size=(2000,2000),
    color=(252, 195, 38,255)
)
mark_image_2 = classes.MarkImage(
    bytes_image=bytes_image,
    bg_color=(0,0,0,0)
)
mark_image_2.remove_background()
images = [
    mark_image,
    mark_image_2
]

mark_stack = classes.MarkStack(
    images=images,
    background=background,
    padding=100,
    gap=-100

)
mark_stack._paste_images()