# MIMESIS - Boilerplate

> 🛟 **Need help or found a bug?** Get support at [support.doodesch.de/boilerplate](https://support.doodesch.de/boilerplate).


> A starter template for MelonLoader mods for MIMESIS. Clone it, run the rename script, and you have a ready-to-build mod skeleton that already matches the project conventions.

![Version](https://img.shields.io/badge/version-1.1.2-blue)
![Game](https://img.shields.io/badge/game-MIMESIS-purple)
![MelonLoader](https://img.shields.io/badge/MelonLoader-0.7.3%2B-green)
![Status](https://img.shields.io/badge/status-template-lightgrey)

![Boilerplate in MIMESIS](https://raw.githubusercontent.com/DooDesch-Mods/Mimesis-Boilerplate/main/docs/img/header.jpg)

This is a developer template, not a player-facing feature mod. Installing it does nothing in game - it just logs that it initialized. Use it as the starting point for a new Mimesis mod.

## Features

- **Minimal MelonMod entry point** (`Core.cs`): on `OnInitializeMelon` it initializes preferences and logs `Boilerplate initialized. Enabled={value}`. No game behavior is patched.
- **MelonPreferences config scaffold** (`Config/BoilerplatePreferences.cs`): an idempotent `Initialize()` plus a typed `CreateEntry<T>` helper that demonstrates the standard preferences pattern.
- **Harmony patch stub** (`Patches/ExamplePatch.cs`): an example of the `[HarmonyPatch(typeof(Class), "Method")]` + Prefix/Postfix pattern with the patch body commented out.
- **One-command setup script** (`setup_mod.sh`, POSIX sh): prompts for a PascalCase mod name, renames the `.csproj`, replaces every `Boilerplate` occurrence across `.cs`/`.csproj`/`.md`/`.json`/`.yml`/`.gitignore`, renames the preferences file, and deletes `.git` so you do not push back to the template.
- **GitHub Actions release workflow** (`.github/workflows/build-and-release.yml`): on a `v*` tag it checks out a private Workspace repo, validates the version tag and injects its version into the Release build, publishes a GitHub Release with the DLL, and uploads the package to Thunderstore.
- **PostBuild auto-copy**: the built DLL is copied to the configured `ModsDirectory`; the shared deploy configuration defaults to `_Test/MIMESIS/Mods`.
- **Optional MimicAPI integration pre-wired but disabled**: a commented `MelonOptionalDependencies("MimicAPI")` in `Core.cs` and commented imports for the shared `MimicAPI.props` in the `.csproj`. Uncomment the imports to enable.

## Screenshots

Game context only. This project has no standalone gameplay feature.

![Native MIMESIS scenery used as developer-template context](https://raw.githubusercontent.com/DooDesch-Mods/Mimesis-Boilerplate/main/docs/img/game-context.jpg)

Game context only. Boilerplate is a developer template without a player-facing gameplay feature.

## Requirements

| Component | Version |
|---|---|
| MIMESIS | 0.4.0 |
| MelonLoader | 0.7.3+ |
| .NET SDK | for building (target framework `netstandard2.1`) |
| Workspace/lib | game DLLs (`lib/game`) + `MelonLoader.dll` / `0Harmony.dll` (`lib/melonloader`) |

## Configuration

Stored in `UserData/MelonPreferences.cfg` under the `Boilerplate` category.

| Option | Description | Default | Values/Range |
|---|---|---|---|
| `Enabled` | Enable Boilerplate functionality. When disabled, the mod will not modify game behavior. The template only logs this value - new mods are expected to gate their patches on it. | `true` | boolean (true/false) |

## Usage

There is no in-game usage and no keybinds - this is a developer template. Workflow for starting a new mod:

1. Clone or copy this folder.
2. Run `./setup_mod.sh` and enter a PascalCase mod name. The script renames the `.csproj`, replaces all `Boilerplate` strings, renames the Config preferences file, and removes `.git`.
3. Optionally rename the folder to match.
4. Re-init Git (`git init && git add . && git commit -m "Initial commit"`).
5. Confirm the shared Workspace imports and `WorkspaceLibPath` point at your Workspace checkout (local default: `$(MSBuildThisFileDirectory)../Workspace/lib`).
6. Build with `dotnet build -c Release` in the mod folder. The shared deploy configuration copies the DLL into `_Test/MIMESIS/Mods`.

To use the patch example, uncomment the patch body in `Patches/ExamplePatch.cs` and replace its example game class and method with your targets. The SDK includes the file automatically.

To use MimicAPI, uncomment the `MelonOptionalDependencies` attribute in `Core.cs` and the `MimicAPI.props` imports in the `.csproj`, then build the Workspace `MimicAPI` project.

## Compatibility

Built for Mimesis 0.4.0 / MelonLoader 0.7.3.

## Building (developers)

```sh
dotnet build -c Release
```

References resolve through `Workspace/lib/game` (game DLLs) and `Workspace/lib/melonloader` (`MelonLoader.dll`, `0Harmony.dll`). The shared deploy configuration copies the built DLL into `_Test/MIMESIS/Mods`. The GitHub Actions workflow pins the build SDK to 8.0.x; the local environment uses a newer SDK.

## Credits / License

Author: DooDesch. Licensed under the MIT License (see `LICENSE.md`).

Repository: <https://github.com/DooDesch-Mods/Mimesis-Boilerplate>

## Images

Gallery images are captured in MIMESIS; release artwork uses real game photos.
