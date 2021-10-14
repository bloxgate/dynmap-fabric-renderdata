import os
from .BlockHandler import BlockHandler

class CubeAllHandler(BlockHandler):
    def __init__(self, *extra_parents):
        super().__init__('block/cube_all', 'minecraft:block/cube_all', *extra_parents)

    # Unneeded
    def convert_texture_key_to_side(self, key):
        pass

    def handle(self, blockFile, blockModel, modID):
        lookupKey = self.determine_namespace_and_adjust_for_lookup(blockModel['textures']['all'])
        txt = BlockHandler.lookup_texture(lookupKey[0], modID, lookupKey[1])
        return f"block:id=%{os.path.splitext(blockFile)[0]},data=*,allfaces=0:{txt},stdrot=true\n"