#!/usr/bin/env python3

import zipfile
import argparse
import json
import tempfile
import os

import blockhandlers

handlers = [blockhandlers.CubeAllHandler(), blockhandlers.CubeHandler(), blockhandlers.CubeColumnHandler(), blockhandlers.LeavesHandler()]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates dynmap texture support for cube/all models in a mod")
    parser.add_argument("modjar", type=str, help="The mod's jar file")
    args = parser.parse_args()

    entries = []
    modID = ""
    assetsID = ""
    tmpDir = tempfile.TemporaryDirectory()
    with zipfile.ZipFile(args.modjar, mode='r') as modjar:
        modData = json.loads(modjar.read("fabric.mod.json"), strict=False)
        modID = modData['id']

        #Extract mod assets
        assetMembers = []
        for file in modjar.namelist():
            if file.startswith(f"assets/{modID}"):
                assetMembers.append(file)
        if len(assetMembers) == 0:
            print(f"Unable to find assets for {modID}.")
            assetsID = input("Enter assets path: ")
            for file in modjar.namelist():
                if file.startswith(f"assets/{assetsID}"):
                    assetMembers.append(file)
        else:
            assetsID = modID
        modjar.extractall(path=tmpDir.name, members=assetMembers)

    for blockFile in os.listdir(os.path.join(tmpDir.name, "assets", assetsID, "models", "block")):
        fullBlockFile = os.path.join(tmpDir.name, "assets", assetsID, "models", "block", blockFile)
        if os.path.isdir(fullBlockFile):
            continue
        with open(fullBlockFile, mode='r') as blockModel:
            model = json.loads(blockModel.read())
            for handler in handlers:
                if handler.can_handle(model):
                    entries.append(handler.handle(blockFile, model, assetsID))
                    break

    with open(f"{modID}-texture.txt", "w") as outFile:
        outFile.writelines(f"modname:{modID}\n\n")
        for k,v in blockhandlers.BlockHandler.textureToIDMap.items():
            outFile.writelines(f"texture:id={v},filename={k},xcount=1,ycount=1\n")
        for entry in entries:
            outFile.writelines(entry)
        outFile.flush()

        