from enum import Enum,auto,unique
# mark stack

@unique
class StackOptions(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()
#* directions to paste
HORIZONTAL = 17
VERTICAL = 10
# * scales
CONTAIN = 11
COVER = 12 # default in mark stack
FIRST_SCALE_DOWN = 13
INHERIT = 14
