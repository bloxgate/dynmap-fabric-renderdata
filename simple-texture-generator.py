#!/usr/bin/env python3

import zipfile
import argparse
import json
import tempfile
import os

textures = set()
textureToIDMap= dict()

def AddOrGetTextureByPath(path, isMod):
    if isMod:
        adjustedPath = f"assets/{modID}/textures/{path}.png"
    else:
        adjustedPath = f"assets/minecraft/textures/{path}.png"

    if adjustedPath in textures:
        return textureToIDMap[adjustedPath]
    else:
        i = len(textures)
        textures.add(adjustedPath)
        textureToIDMap[adjustedPath] = f"txt{i:04d}"
        return textureToIDMap[adjustedPath]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates dynmap texture support for cube/all models in a mod")
    parser.add_argument("modjar", type=str, help="The mod's jar file")
    args = parser.parse_args()

    entries = []
    modID = ""
    tmpDir = tempfile.TemporaryDirectory()
    with zipfile.ZipFile(args.modjar, mode='r') as modjar:
        modData = json.loads(modjar.read("fabric.mod.json"))
        modID = modData['id']

        #Extract mod assets
        assetMembers = []
        for file in modjar.namelist():
            if file.startswith(f"assets/{modID}"):
                assetMembers.append(file)
        modjar.extractall(path=tmpDir.name, members=assetMembers)

    for blockFile in os.listdir(os.path.join(tmpDir.name, "assets", modID, "models", "block")):
        fullBlockFile = os.path.join(tmpDir.name, "assets", modID, "models", "block", blockFile)
        if os.path.isdir(fullBlockFile):
            continue
        with open(fullBlockFile, mode='r') as blockModel:
            model = json.loads(blockModel.read())
            if 'parent' in model.keys() and (model['parent'] == "block/cube_all" or model['parent'] == "minecraft:block/cube_all"):
                if ':' in model['textures']['all']:
                    txt = AddOrGetTextureByPath(model['textures']['all'].split(':')[1], True)
                    entries.append(f"block:id=%{os.path.splitext(blockFile)[0]},data=*,allfaces=0:{txt},stdrot=true\n")
                else:
                    txt = AddOrGetTextureByPath(model['textures']['all'], False)
                    entries.append(f"block:id=%{os.path.splitext(blockFile)[0]},data=*,allfaces=0:{txt},stdrot=true\n")

    with open(f"{modID}-texture.txt", "w") as outFile:
        outFile.writelines(f"modname:{modID}\n\n")
        for k,v in textureToIDMap.items():
            outFile.writelines(f"texture:id={v},filename={k},xcount=1,ycount=1\n")
        for entry in entries:
            outFile.writelines(entry)
        outFile.flush()

        