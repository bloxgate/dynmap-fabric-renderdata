from abc import ABC, abstractmethod

class BlockHandler(ABC):
    textureToIDMap = dict()

    def __init__(self, *parents):
        self.parents = parents

    @abstractmethod
    def handle(self, blockFile, blockModel, modID):
        pass

    @abstractmethod
    def convert_texture_key_to_side(self, key):
        pass

    def can_handle(self, blockModel):
        if 'parent' in blockModel.keys() and blockModel['parent'] in self.parents:
            return True
        return False

    def determine_namespace_and_adjust_for_lookup(self, texturePath):
        if 'minecraft:' in texturePath:
            return (texturePath.split(':')[1], False)
        if ':' in texturePath:
            return (texturePath.split(':')[1], True)
        else:
            return (texturePath, False)

    @staticmethod
    def lookup_texture(path, modID, isModTexture=True):
        if isModTexture:
            adjustedPath = f"assets/{modID}/textures/{path}.png"
        else:
            adjustedPath = f"assets/minecraft/textures/{path}.png"

        if adjustedPath in BlockHandler.textureToIDMap:
            return BlockHandler.textureToIDMap[adjustedPath]
        else:
            i = len(BlockHandler.textureToIDMap.keys())
            BlockHandler.textureToIDMap[adjustedPath] = f"txt{i:04d}"
            return BlockHandler.textureToIDMap[adjustedPath]
    