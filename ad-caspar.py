from phidias.Main import *

from front_end import *
from def_cls_builder import *
from routines_parser import *
from direct_cmd_parser import *
from smart_env_int import *

# instantiate the engine
PHIDIAS.run()
# run the engine shell
PHIDIAS.shell(globals())


