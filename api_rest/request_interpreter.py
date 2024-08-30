from control.classes import MarkImage,MarkStack
from django.core.files.uploadedfile import InMemoryUploadedFile
from control.constants import StackOptions
from control.scaling_funtions import scaling_object
from control.transforms import rotate,scale
from PIL import Image
from io import BytesIO
from . tools import make_image_with_gradient
class Interpreter:
    def __make_to_mark(self,images:tuple[InMemoryUploadedFile],remove_bg:bool=False)->tuple[MarkImage]:
        mark_images = []
        bg_color = (0,0,0,0)
        for image in images:
            mark_image = MarkImage(
                    initial_image= image.read(),
                    bg_color=bg_color,
            )
            if remove_bg : mark_image.remove_background()
            mark_images.append(mark_image)
        return tuple(mark_images)
    
    def __get_background_size(self,stack_options:dict)->tuple[int]:
        size_background = stack_options['resolution'].split('x')
        size_background[0] = int(size_background[0])
        size_background[1] = int(size_background[1])
        return size_background
    
    def __get_alignments(self,stack_options:dict)->set:
        align = set()
        if "alignment" in stack_options:
            if "horizontal" in stack_options['alignment']:
                align.add(StackOptions.HORIZONTAL)
            if "vertical" in stack_options['alignment']:
                align.add(StackOptions.VERTICAL)
        return align
    
    def __get_scaling(self,stack_options):
        match stack_options['scaling']:
            case 'contain':
                return scaling_object.contain
            case "cover":
                return scaling_object.cover
            case _:
                return scaling_object.initial

    def __get_direction(self,stack_options):
        if stack_options['direction'].lower() == 'row':
            return StackOptions.HORIZONTAL
        elif stack_options['direction'].lower() == 'column':
            return StackOptions.VERTICAL
        
    def __default_transform(self,im:Image.Image,id_mark:str,current_index:int,len_images:int)->Image.Image:
        if current_index in self.__middle_index:
            return scale(im,id_mark,1.2)
        return rotate(
            im=im,
            id_mark_image=id_mark,
            deg=25 if current_index < self.__middle_index[0] else -25,
            crop=True
        )
        
            
    def __get_middle_indexs(self,images:list|tuple)->tuple:
        length = len(images)
        middle_index = [length//2]
        if middle_index[0]%2 == 0:
            middle_index = [middle_index[0],middle_index[0]-1]
        return tuple(middle_index)
    
    def __make_background(self,stack_options)->Image.Image:
        size_background = self.__get_background_size(stack_options)
        if len(stack_options['background_color'])==1:
            return Image.new(
               "RGBA",
                size=size_background,
                color=tuple(stack_options['background_color'][0])
            )
        else:
            return make_image_with_gradient(stack_options['background_color'],*size_background)
        

    def make_stack(self,request:dict)->tuple[BytesIO,str]:
        """
        Este método retorna el buffer donde esta guardada la imagen del stack y también retorna su mimetype.
        """
        mark_images = self.__make_to_mark(request['images'],request['remove_bg'])
        self.__middle_index = self.__get_middle_indexs(mark_images)
        stack_options = request['stack_options']
        alignment = self.__get_alignments(stack_options)
        direction = self.__get_direction(stack_options)
        scaling_function = self.__get_scaling(stack_options)
        # make stack
        background = self.__make_background(stack_options)
        mark_stack = MarkStack(
            images=mark_images,
            background=background,
            padding=stack_options['padding'],
            gap=stack_options['gap'],
            scaling_function=scaling_function,
            alignment_in=alignment,
            direction=direction
        )
        image:Image.Image = mark_stack.make_stack(self.__default_transform)
        mimetype = "PNG"
        buffer = BytesIO()
        image.save(buffer, format=mimetype)
        buffer.seek(0)
        return (buffer,mimetype)