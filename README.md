# DEPRECATION NOTICE

THIS PROJECT IS DEPRECATED BECAUSE WE NO LONGER NEED A WRAPPER AROUND COPR. WE RUN THE COPR CLI MANUALLY FROM A FEDORA CONTAINER NOW (https://github.com/kwk/llvm-daily-fedora-rpms):

```yaml
jobs:
  build-on-copr:
    runs-on: ubuntu-latest
    container: fedora:37
    steps:
      - name: Install Copr CLI
        run: |
          dnf install -y copr-cli
```

A good use of this project is to see how the poetry setup was arranged and how the pypi releases work there. Also the Python Multiple Inheritance stuff been done here is really nice to write and compose but it is hard to maintain. 

-----

# llvm_snapshot_builder

Builds LLVM snapshots on Copr

## Status

[![Documentation Status](https://readthedocs.org/projects/llvm_snapshot_builder/badge/?version=latest)](https://llvm_snapshot_builder.readthedocs.io/en/latest/?badge=latest)
[![CodeQL](https://github.com/kwk/llvm_snapshot_builder/actions/workflows/codeql.yml/badge.svg)](https://github.com/kwk/llvm_snapshot_builder/actions/workflows/codeql.yml)
[![ci-cd](https://github.com/kwk/llvm_snapshot_builder/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/kwk/llvm_snapshot_builder/actions/workflows/ci-cd.yml)
[![codecov](https://codecov.io/gh/kwk/llvm_snapshot_builder/branch/main/graph/badge.svg?token=ASSPTOL3JU)](https://codecov.io/gh/kwk/llvm_snapshot_builder)
[![release](https://img.shields.io/github/release/kwk/llvm_snapshot_builder.svg)](https://github.com/kwk/llvm_snapshot_builder/releases)

## Installation

```bash
$ pip install llvm_snapshot_builder
```

## Usage

For a more in-depth example, take a look at [the example in the documentation](https://llvm_snapshot_builder.readthedocs.io/en/latest/example.html).

After installing you can explore the CLI program with:

```bash
$ python -m llvm_snapshot_builder.cli --help
```

or with:

```console
$ llvm_sb --help
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

### Commit message conventions and semantic versioniong (semver)

We use semantic versioning and [these commit message conventions](https://www.conventionalcommits.org/en/v1.0.0/)
can be used to automatically bump the version number and generate the changelog.

## License

`llvm_snapshot_builder` was created by Konrad Kleine <kkleine@redhat.com>. It is licensed under the terms of the MIT license.

## Credits

`llvm_snapshot_builder` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
