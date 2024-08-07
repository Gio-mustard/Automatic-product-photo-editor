from enum import Enum,auto,unique
# mark stack

@unique
class StackOptions(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()
    # * scales
    CONTAIN = auto()
    COVER = auto()
    INITIAL = auto() # default in mark stack