# Dynmap Fabric Renderdata

Since there currently isn't an equivalent of [DynmapBlockScan](https://github.com/webbukkit/DynmapBlockScan) for Fabric, I've written a small python script that can generate texture definitions for blocks that extend from `block/cube_all`.

## Using this repo

Find the `-texture.txt` files for your mods in `models/` and place them in `dynmap/renderdata/` on your server. You will need to restart your server for Dynmap to load the files.

## Contributing

If you'd like to add renderdata simply run the included python script on the mod jar file like so:

```bash
python3 simple-texture-generator.py mod-file.jar
```

 A file called `modid-texture.txt` will be generated. Just move it to the right location inside `models/` and you're good to make a PR.

### Adding Extra Blocks

If you want to add blocks that aren't children of `block/cube_all` you can do so, but it must be done manually with the current version of the script.

## Caveats

This script currently doesn't enter into subdirectories of the `models/block` folder, so not all compatible blocks may have renderdata generated.