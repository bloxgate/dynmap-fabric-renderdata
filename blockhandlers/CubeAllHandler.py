import os
from .BlockHandler import BlockHandler

class CubeAllHandler(BlockHandler):
    def __init__(self, *extra_parents):
        super().__init__('block/cube_all', 'minecraft:block/cube_all', *extra_parents)

    def handle(self, blockFile, blockModel, modID):
        if ':' in blockModel['textures']['all']:
            txt = BlockHandler.lookup_texture(blockModel['textures']['all'].split(':')[1], modID)
            return f"block:id=%{os.path.splitext(blockFile)[0]},data=*,allfaces=0:{txt},stdrot=true\n"
        else:
            txt = BlockHandler.lookup_texture(blockModel['textures']['all'], None, False)
            return f"block:id=%{os.path.splitext(blockFile)[0]},data=*,allfaces=0:{txt},stdrot=true\n"