"""Create an allowlisted source kit, with no game binaries, Git history or local settings."""
import argparse
import hashlib
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FILES = ('setup_mod.py', 'setup_mod.sh', 'Core.cs', 'Config/BoilerplatePreferences.cs',
         'Patches/ExamplePatch.cs', 'templates/Standalone.csproj', 'templates/Build.yml', 'tools/test_setup.py',
         'tools/package_source.py', '.gitignore', 'README.md', 'CHANGELOG.md', 'LICENSE.md')


def package(destination: Path):
    contents = {f'Boilerplate/{name}': (ROOT / name).read_bytes() for name in FILES}
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(contents.items()):
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = (0o100755 if name.endswith('.sh') else 0o100644) << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, data)
    with zipfile.ZipFile(destination) as archive:
        if archive.testzip() is not None or set(archive.namelist()) != set(contents):
            raise ValueError(f'Source kit failed integrity check: {destination}')
    print(f'{destination}: {len(contents)} source files, SHA256 {hashlib.sha256(destination.read_bytes()).hexdigest()}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    package(parser.parse_args().output)
