import os
from .BlockHandler import BlockHandler

class CubeColumnHandler(BlockHandler):

    def __init__(self, *extra_parents):
        super().__init__('block/cube_column', 'minecraft:block/cube_column', *extra_parents)

    def convert_texture_key_to_side(self, key):
        if key == "end":
            return "topbottom"
        elif key == "side":
            return "allsides"
        else:
            #This shouldn't happen AFAIK, but just roll with it
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