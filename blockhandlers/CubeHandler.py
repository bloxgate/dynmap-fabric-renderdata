import os
from .BlockHandler import BlockHandler

class CubeHandler(BlockHandler):
    def __init__(self, *extra_parents):
        super().__init__('block/cube', 'minecraft:block/cube', *extra_parents)

    def convert_texture_key_to_side(self, key):
        if key == "up":
            return "top"
        elif key == "down":
            return "bottom"
        else:
            return key

    def handle(self, blockFile, blockModel, modID):
        entry = f"block:id=%{os.path.splitext(blockFile)[0]},data=*,"
        for key in blockModel['textures'].keys():
            if key == 'particle':
                continue
            lookupKey = self.determine_namespace_and_adjust_for_lookup(blockModel['textures'][key])
            txtSide = self.convert_texture_key_to_side(key)
            txt = BlockHandler.lookup_texture(lookupKey[0], modID, lookupKey[1])
            entry += f"{txtSide}=0:{txt},"
        entry += "stdrot=true\n"
        return entry