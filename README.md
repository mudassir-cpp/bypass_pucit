# bypass_pucit

[![PyPI - Version](https://img.shields.io/pypi/v/bypass-pucit.svg)](https://pypi.org/project/bypass-pucit)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bypass-pucit.svg)](https://pypi.org/project/bypass-pucit)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install bypass-pucit
```

## Usage

Apply the proxy settings:

```console
bypass_pucit set --proxy http://172.16.0.6:8080
```

Remove the proxy settings:

```console
bypass_pucit unset
```

On Linux, the tool relaunches itself through `sudo` when root access is needed, and it still edits the original user's shell files. On Windows, it requests a UAC/admin relaunch before writing proxy settings.

## Notes

- The tool updates only the package managers and system settings that are installed on the machine.
- If the shell is not `bash` or `zsh`, the Linux backend falls back to `~/.profile`.
- You can override the default proxy with `--proxy` or the `BYPASS_PUCIT_PROXY` environment variable.
- Linux and Windows backends now also configure `wget`, `Maven`, `Gradle`, `Docker`, and `pnpm` when those tools are present.

## License

`bypass-pucit` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
