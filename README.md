# MIMESIS - Boilerplate

> 🛟 **Need help or found a bug?** Get support at [support.doodesch.de/boilerplate](https://support.doodesch.de/boilerplate).

A small developer template for MIMESIS 0.4.0 and MelonLoader 0.7.3. Generate a mod with your own name and author, then build it without a private Workspace or access token.

![Boilerplate in MIMESIS](https://raw.githubusercontent.com/DooDesch-Mods/Mimesis-Boilerplate/main/docs/img/header.jpg)

## Start a mod

Download the **source kit** from the release files, or clone this repository. Store packages include it under `Source/Boilerplate/`. Python 3.10+ and .NET SDK 8+ are required.

```sh
python setup_mod.py MyMod ../MyMod --author "Your name"
dotnet build ../MyMod/MyMod.csproj -c Release -p:GamePath="/path/to/MIMESIS"
```

Install MelonLoader 0.7.3 in your MIMESIS installation first. On Windows, use `python` or `py -3`; the optional `setup_mod.sh` wrapper uses `python3`.

The destination must be new and outside the template folder. Setup never overwrites existing files, edits the template or deletes Git history. It copies an explicit source allowlist and creates a separate project without our private build imports, workflows, images or release identity. It includes its own public GitHub build workflow using official MelonLoader references.

The generated DLL is in `bin/Release/netstandard2.1/`. Copy only your mod DLL to `MIMESIS/Mods/`. Building the generated project does not deploy or launch the game. Alternatively supply `MelonLoaderPath` (the folder with MelonLoader.dll and 0Harmony.dll) and `GameManagedPath` (`MIMESIS_Data/Managed`) instead of `GamePath`.

## Included patterns

- A minimal `MelonMod` entry point with the correct MIMESIS game identity.
- Typed, nullable-aware, idempotent MelonPreferences initialization before patches run.
- An inactive Harmony example. Replace the target with a method from the current game build and guard your changes with `Enabled`.
- One build version: `-p:Version=1.0.0` reaches both assembly metadata and `MelonInfo`.
- `Private=false` references so loader and game assemblies stay out of your build output.
- Deterministic builds, explicit reference errors and no automatic game installation changes.

MelonLoader applies assembly Harmony patches automatically. Do not call `PatchAll()` again. Scene objects do not exist during mod initialization; resolve them after their scene is ready. Gameplay changes in a multiplayer mod need explicit host authority and settings synchronization. The template does not provide network synchronization or a MimicAPI dependency; add only what your mod needs.

The generated README includes a support link. Set your own support URL, project metadata, license and release workflow before publishing your mod. The template itself is MIT licensed; retain its license notice when distributing its source.

## Repeatable checks

```sh
python tools/test_setup.py
python tools/test_setup.py --loader "/path/to/MelonLoader/net35" --output ../CanaryMod
python tools/package_source.py dist/Boilerplate-source.zip
```

Checks cover renaming, author escaping, invalid identifiers, source-directory guards and preservation of an existing Git marker. The optional build generates a fresh mod and checks that only its own DLL is emitted. CI runs these checks and builds from the source ZIP on Windows and Linux with the official MelonLoader 0.7.3 references. Game DLLs and private Workspace files are not redistributed.

## Template demonstration

The optional `Boilerplate.dll` only logs initialization and creates `[Boilerplate] Enabled = true` in `UserData/MelonPreferences.cfg`. It does not change gameplay. Installing this demonstration DLL is not needed to develop your own mod.

![Native MIMESIS scenery used as developer-template context](https://raw.githubusercontent.com/DooDesch-Mods/Mimesis-Boilerplate/main/docs/img/game-context.jpg)

All images use real MIMESIS captures. This is game context, not a gameplay feature of the template.

## Build this repository

Our own demonstration release uses the shared DooDesch Workspace and standard MIMESIS release CI. That infrastructure is not copied into generated mods. To build independently, use the generator above.

Version: **1.2.0**. Author: DooDesch. [MIT License](LICENSE.md).

Repository: <https://github.com/DooDesch-Mods/Mimesis-Boilerplate>
