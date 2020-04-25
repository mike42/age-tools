# age-tools

Python library and command-line tools for working with Age of Empires I data files.

## Examples

Render a scenario file to a diamond-shaped image showing terrain, resources and unit locations:

```
age-scenario minimap foo.scx --out foo.png
```

Extract game data to a YAML file. This makes it possible to compare game data files (eg. using `diff`) to check the contents of a mod:

```
age-gamedata extract empires.dat --out empires.yml
```

Extract files from a DRS asset archive to find the "wololo" priest sound:

```
mkdir sounds
age-archive extract sounds.drs --directory sounds/
aplay sounds/5051.wav
```

## Attribution

- `dat`, `scn` and `drs` format handling is directly based on [SiegeEngineers/genie-rs](https://github.com/SiegeEngineers/genie-rs).
- SLP file format handling is based on the description at [SFTtech/openage](https://github.com/blob/9f13a91184e16af761fd9b654ff66cb3665261dd/doc/media/slp-files.md)

