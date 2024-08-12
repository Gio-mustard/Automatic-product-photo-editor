class History:
    MARK_IMAGES = 0
    __TRANSFORMS = {
        None:set()
    }
    def __init__(self) -> None:
        self.MARK_IMAGES+=1

    @classmethod
    def push(cls,id_mark_image,transform)->None:
        if not id_mark_image in cls.__TRANSFORMS:
            cls.__TRANSFORMS[id_mark_image] = set()
        cls.__TRANSFORMS[id_mark_image].add(transform)

    @classmethod
    def has(cls,id_mark_image,transform) -> bool:
        try:
            return transform in cls.__TRANSFORMS[id_mark_image]
        except KeyError:
            return False
        
    @classmethod
    def remove(cls,id_mark_image,transform)->None:
        cls.__TRANSFORMS[id_mark_image].remove(transform)

    @classmethod
    def num_of_mark_images(cls)->int:
        return len(cls.MARK_IMAGES)