from .BlockHandler import BlockHandler
from .CubeAllHandler import CubeAllHandler
from .CubeHandler import CubeHandler

class LeavesHandler(BlockHandler):
    def __init__(self, *extra_parents):
        super().__init__('block/leaves', 'minecraft:block/leaves', *extra_parents)

    # Unneeded
    def convert_texture_key_to_side(self, key):
        pass

    internalHandlers = {"all": CubeAllHandler(), "cube": CubeHandler()}
    def handle(self, blockFile, blockModel, modID):
        if 'all' in blockModel['textures'].keys():
            return LeavesHandler.internalHandlers['all'].handle(blockFile, blockModel, modID)
        else:
            return LeavesHandler.internalHandlers['cube'].handle(blockFile, blockModel, modID)