"""Repeatable generator regression tests; optionally compile a generated project."""
import argparse
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('setup_mod', ROOT / 'setup_mod.py')
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


class GeneratorTests(unittest.TestCase):
    def test_rename_and_author_are_complete(self):
        with tempfile.TemporaryDirectory() as folder:
            output = setup.generate('TestMod', Path(folder) / 'mod', 'Tester "Q" & Co')
            self.assertEqual(len(list(output.rglob('*.csproj'))), 1)
            project = ET.parse(output / 'TestMod.csproj')
            self.assertEqual(project.findtext('./PropertyGroup/Authors'), 'Tester "Q" & Co')
            core = (output / 'Core.cs').read_text(encoding='utf-8')
            self.assertIn('TestMod.Build.ModVersion.Current', core)
            self.assertIn('Tester \\"Q\\" & Co', core)
            self.assertTrue((output / 'Config/TestModPreferences.cs').is_file())
            for path in output.rglob('*'):
                if path.is_file():
                    self.assertNotIn('Boilerplate', path.read_text(encoding='utf-8'))
            workflow = (output / '.github/workflows/build.yml').read_text(encoding='utf-8')
            self.assertIn('TestMod.csproj', workflow)
            self.assertNotIn('DooDesch-Mods', workflow)
            self.assertFalse((output / '.git').exists())

    def test_existing_destination_and_git_are_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder)
            sentinel = destination / '.git'
            sentinel.write_text('existing repository', encoding='utf-8')
            with self.assertRaises(ValueError):
                setup.generate('TestMod', destination, 'Tester')
            self.assertEqual(sentinel.read_text(), 'existing repository')

    def test_invalid_identifiers_and_source_destination(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'invalid'
            for name in ('4Mod', 'class', '../Mod', 'My Mod', 'Boilerplate', '', 'Mod;Run'):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    setup.generate(name, target, 'Tester')
            self.assertFalse(target.exists())
        with self.assertRaises(ValueError):
            setup.generate('TestMod', ROOT / 'Generated', 'Tester')

    def test_rejects_control_characters_in_author(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                setup.generate('TestMod', Path(folder) / 'mod', 'Tester\nInjected')


def compile_generated(loader: Path, output: Path):
    target = setup.generate('CanaryMod', output, 'DooDesch')
    subprocess.run(['dotnet', 'build', str(target / 'CanaryMod.csproj'), '-c', 'Release',
                    f'-p:MelonLoaderPath={loader.resolve()}', '-p:Version=0.1.7'], check=True)
    binaries = sorted(p.name for p in (target / 'bin/Release/netstandard2.1').glob('*.dll'))
    if binaries != ['CanaryMod.dll']:
        raise AssertionError(f'Loader or game dependency leaked into output: {binaries}')
    print(f'Generated project builds independently: {target}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--loader', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--temp-root', type=Path, help='Writable directory for temporary test fixtures')
    args = parser.parse_args()
    if args.temp_root:
        args.temp_root.mkdir(parents=True, exist_ok=True)
        tempfile.tempdir = str(args.temp_root.resolve())
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(GeneratorTests))
    if not result.wasSuccessful():
        raise SystemExit(1)
    if args.loader:
        if not args.output:
            parser.error('--loader requires --output pointing to a new directory')
        compile_generated(args.loader, args.output)
