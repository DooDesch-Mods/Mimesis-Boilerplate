# MIMESIS - Boilerplate

> 🛟 **Need help or found a bug?** Get support at [support.doodesch.de/boilerplate](https://support.doodesch.de/boilerplate).


> A starter template for building MelonLoader mods for MIMESIS. Clone it, rename it, and you have a ready-to-build mod skeleton that matches the project conventions.

![Version](https://img.shields.io/badge/version-1.1.2-blue)
![Game](https://img.shields.io/badge/game-MIMESIS-purple)
![MelonLoader](https://img.shields.io/badge/MelonLoader-0.7.3%2B-green)
![Status](https://img.shields.io/badge/status-template-lightgrey)

![Boilerplate in MIMESIS](https://raw.githubusercontent.com/DooDesch-Mods/Mimesis-Boilerplate/main/docs/img/header.jpg)

This is a developer template, not a player-facing feature mod. Installing it does nothing in game - it only logs that it initialized. If you are a player, there is nothing to configure here. If you are a modder, use it as the starting point for a new Mimesis mod.

## Features

- Minimal `MelonMod` entry point that initializes preferences - no game behavior is patched.
- MelonPreferences config scaffold demonstrating the standard preferences pattern.
- A Harmony patch stub showing the Prefix/Postfix pattern, with the patch body commented out.
- A one-command setup script that renames the project to your mod name and removes the template Git history.
- A GitHub Actions workflow that builds on a version tag and publishes to GitHub Releases and Thunderstore.
- Optional MimicAPI integration pre-wired but disabled - uncomment to enable.

## Screenshots

Game context only. This project has no standalone gameplay feature.

![Native MIMESIS scenery used as developer-template context](https://raw.githubusercontent.com/DooDesch-Mods/Mimesis-Boilerplate/main/docs/img/game-context.jpg)

Game context only. Boilerplate is a developer template without a player-facing gameplay feature.

## Requirements

| Component | Version |
|---|---|
| MIMESIS | 0.4.0 |
| MelonLoader | 0.7.3+ |

## Installation

- Recommended: install via a Thunderstore mod manager (r2modman or Gale).
- Manual: download the package, extract `Boilerplate.dll` into `MIMESIS/Mods/`, and launch once to generate the config.

## Configuration

Stored in `UserData/MelonPreferences.cfg` under the `Boilerplate` category.

| Option | Description | Default | Values/Range |
|---|---|---|---|
| `Enabled` | Enable Boilerplate functionality. When disabled, the mod will not modify game behavior. The template only logs this value. | `true` | boolean (true/false) |

## Usage

There is no in-game usage and no keybinds. This is a developer template - it produces no visible effect in game.

For the full setup guide (rename script, build steps, GitHub Actions, and optional MimicAPI), see the repository:

<https://github.com/DooDesch-Mods/Mimesis-Boilerplate>

## Credits / License

Author: DooDesch. Licensed under the MIT License.

## Images

Gallery images are captured in MIMESIS; release artwork uses real game photos.

Built against MIMESIS 0.4.0 / MelonLoader 0.7.3.
