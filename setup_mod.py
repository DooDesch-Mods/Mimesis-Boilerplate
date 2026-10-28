"""Generate an independent MIMESIS mod without modifying the template or Git history."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import sys
from xml.sax.saxutils import escape

SOURCE = Path(__file__).resolve().parent
FILES = ('Core.cs', 'Config/BoilerplatePreferences.cs', 'Patches/ExamplePatch.cs', '.gitignore', 'LICENSE.md')


def generate(name: str, destination: Path, author: str) -> Path:
    if not re.fullmatch(r'[A-Z][A-Za-z0-9_]*', name) or name == 'Boilerplate':
        raise ValueError('Name must start with an uppercase ASCII letter and use letters, digits or underscores. Choose a name other than Boilerplate.')
    if not author.strip() or any(ord(c) < 32 for c in author):
        raise ValueError('Author must be non-empty and contain no control characters.')
    target = destination.resolve()
    if target.exists():
        raise ValueError(f'Destination already exists; no files changed: {target}')
    if target == SOURCE or SOURCE in target.parents:
        raise ValueError('Choose a destination outside the template directory.')
    if not target.parent.is_dir():
        raise ValueError(f'Destination parent does not exist: {target.parent}')

    # Prepare inputs before creating output, so a missing input cannot leave a partial mod.
    output: dict[str, str] = {}
    for relative in FILES:
        content = (SOURCE / relative).read_text(encoding='utf-8')
        if relative == 'Core.cs':
            content = content.replace('DooDesch.ModVersion.Current', 'Boilerplate.Build.ModVersion.Current')
            content = content.replace('"DooDesch", null', f'{json.dumps(author, ensure_ascii=False)}, null')
        output[relative.replace('Boilerplate', name)] = content.replace('Boilerplate', name)
    project = (SOURCE / 'templates/Standalone.csproj').read_text(encoding='utf-8')
    output[f'{name}.csproj'] = project.replace('Boilerplate', name).replace('__AUTHOR_XML__', escape(author))
    workflow = (SOURCE / 'templates/Build.yml').read_text(encoding='utf-8')
    output['.github/workflows/build.yml'] = workflow.replace('Boilerplate', name)
    output['README.md'] = f'''# {name}

> 🛟 **Need help or found a bug?** Get support at [support.doodesch.de/{name.lower()}](https://support.doodesch.de/{name.lower()}).

MIMESIS 0.4.0 / MelonLoader 0.7.3 mod skeleton. Set your own support URL before publishing.

Build with .NET SDK 8 or later:

```sh
dotnet build -c Release -p:GamePath="/path/to/MIMESIS"
```

Alternatively pass `-p:MelonLoaderPath="/path/to/MelonLoader/net35"` and
`-p:GameManagedPath="/path/to/MIMESIS_Data/Managed"`.
Only `{name}.dll` from `bin/Release/netstandard2.1/` belongs in the game's `Mods/` folder.
The build does not deploy or launch the game. It never packages loader or game DLLs.

Preferences initialize before Harmony patches. MelonLoader patches the assembly automatically;
do not call `PatchAll()` again. The Enabled preference must guard your patch's changes.
The example patch is inactive until you replace its game type and method.
Scene objects are not available in `OnInitializeMelon`; resolve them when their scene is ready.

Use `-p:Version=1.0.0` when building a release. This sets both assembly and MelonInfo versions.
No private Workspace, MimicAPI or GitHub token is required to build this skeleton.
The generated GitHub build workflow downloads official loader references and uploads only your DLL.
Add a private reference source in CI when your own patches need game DLLs; do not publish game DLLs.
Set your metadata and release packaging before publication. Retain the included MIT license notice.
'''
    target.mkdir()
    try:
        for relative, content in output.items():
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8', newline='\n')
    except Exception:
        # Remove only the output directory this invocation just created.
        shutil.rmtree(target)
        raise
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name', help='PascalCase C# project name, for example MyMod')
    parser.add_argument('destination', type=Path, help='New directory; never overwrites existing directories')
    parser.add_argument('--author', required=True, help='Author shown by MelonLoader and assembly metadata')
    args = parser.parse_args()
    try:
        target = generate(args.name, args.destination, args.author)
    except (ValueError, OSError) as error:
        print(f'error: {error}', file=sys.stderr)
        return 1
    print(f'Created {target / (args.name + ".csproj")}; source and Git history unchanged.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
