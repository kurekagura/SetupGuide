# Linux Software Installation in Dockerfile

## PowerShell

```Dockerfile
# PowerShell
&& wget --quiet https://github.com/PowerShell/PowerShell/releases/download/v7.2.7/powershell-lts_7.2.7-1.deb_amd64.deb -O ~/PowershellInstaller.deb \
&& dpkg -i ~/PowershellInstaller.deb \ 
```

## Visual Studio Code

**Requires `gdebi` to install.**

```Dockerfile
ENV DONT_PROMPT_WSL_INSTALL 1
```

```Dockerfile
# vscode
&& wget --quiet https://go.microsoft.com/fwlink/?LinkID=760868 -O ~/VSCodeInstaller.deb \
&& gdebi --non-interactive ~/VSCodeInstaller.deb \
&& mkdir -p ~/.config/Code \
&& code --install-extension spadin.remote-x11@1.5.0 --no-sandbox --user-data-dir=~/.config/Code --extensions-dir=/.vscode/ext-default \
&& code --install-extension ms-python.python@2022.19.13141010 --user-data-dir=~/.config/Code --extensions-dir=/.vscode/ext-default \
&& code --install-extension alefragnani.Bookmarks@13.3.1 --user-data-dir=~/.config/Code --extensions-dir=/.vscode/ext-default \
&& code --install-extension oderwat.indent-rainbow@8.3.1 --user-data-dir=~/.config/Code --extensions-dir=/.vscode/ext-default \
&& echo "export DONT_PROMPT_WSL_INSTALL=1" >> ~/.bashrc \
```

Other usefull extensions.

```text
ms-ceintl.vscode-language-pack-ja@1.74.12140928
```

```text
/usr/bin/code -> /usr/share/code/bin/code*
```

```bash
# code
You are trying to start Visual Studio Code as a super user which isn't recommended.
If this was intended, please add the argument `--no-sandbox` 
and specify an alternate user data directory using the `--user-data-dir` argument.

# code --user-data-dir=/root/.config/Code --extensions-dir=/root/.vscode/extensions --no-sandbox
```

```Dockerfile
# The case you want to share extensions.
&& echo 'code(){ /usr/bin/code --extensions-dir=/.vscode/ext-default --no-sandbox "$@";}' >> ~/.bashrc \
&& echo "export -f code" >> ~/.bashrc \
```

vscode linux default user's setting is stored in `$HOME/.config/Code/User/settings.json`.

[Search Visual Studio Code extensions](https://marketplace.visualstudio.com/vscode)

Click "Download Extension" to know the name of the extension. Use @ to separate its name and version.

code needs three writable folders:

1. --user-data-dir=(default:~/.config/Code)
1. --extensions-dir=(default:~/.vscode/extensions)
1. /tmp/runtime-root/ (e.g., mkdir -m 1770 /tmp/runtime-root)

[refs]

- [Visual Studio Code on Linux](https://code.visualstudio.com/docs/setup/linux)
- [Uninstall Visual Studio Code](https://code.visualstudio.com/docs/setup/uninstall)

## Miniconda

```Dockerfile
&& wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py39_4.9.2-Linux-x86_64.sh -O ~/MinicondaInstaller.sh \
&& /bin/bash ~/MinicondaInstaller.sh -b -p ~/miniconda3 \
```

```Dockerfile
&& echo ". ~/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc \
```

[refs]

- [Other's versions](https://repo.anaconda.com/miniconda/)
- [【Dockerfile】DockerにConda環境を構築し、仮想環境をActivateする](https://qiita.com/kuboko-jp/items/6388c186e16028d3e699)

## Anaconda

```Dockerfile
# Anaconda
&& wget --quiet https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh -O ~/AnacondaInstaller.sh \
&& /bin/bash ~/AnacondaInstaller.sh -b -p /opt/anaconda3 \
```

```Dockerfile
&& echo "export CONDA_ENVS_PATH=/path/to/envs" >> ~/.bashrc \
&& echo "export CONDA_PKGS_DIRS=/path/to/pkgs" >> ~/.bashrc \
&& echo "export PIP_CACHE_DIR=/path/to/pipcache" >> ~/.bashrc \
```

- [Installing in silent mode](https://docs.anaconda.com/anaconda/install/silent-mode/)

>The following instructions are for Miniconda. For Anaconda Distribution, substitute Anaconda for Miniconda in all of the commands and change <https://repo.anaconda.com/miniconda> to <https://repo.anaconda.com/archive> for downloading the installer.

>-b Batch mode with no PATH modifications to ~/.bashrc. Assumes that you agree to the license agreement. Does not edit the .bashrc or .bash_profile files.<br>-p Installation prefix/path.

- [Specify environment directories (envs_dirs)](https://conda.io/projects/conda/en/latest/user-guide/configuration/use-condarc.html#specify-env-directories)

## Troubles

### Trouble 1 - vscode

```bash
#gdebi --non-interactive ~/VSCodeInstaller.deb
(...)
update-alternatives: using /usr/bin/code to provide /usr/bin/editor (editor) in auto mode
/var/lib/dpkg/info/code.postinst: line 77: gpg: command not found
dpkg: error processing package code (--install):
 installed code package post-installation script subprocess returned error exit status 127
Processing triggers for mime-support (3.64ubuntu1) ...
Processing triggers for shared-mime-info (1.15-1) ...
Errors were encountered while processing:
 code

#echo $?
1
```
