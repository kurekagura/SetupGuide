# Dockerfile for Ubuntu

```Dockerfiles
FROM ubuntu:20.04
```

## wget and curl

If you use https, don't be with `--no-install-recommends`.

```Dockerfiles
RUN apt -y update && apt -y install wget=1.20.3-1ubuntu1 curl=7.68.0-1ubuntu2.14
```

## wget

```Dockerfile
wget=1.20.3-1ubuntu1
```

Usage:

- -O
- --quiet
- --no-check-certificate

```bash
wget --quiet --no-check-certificate https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh -O ~/AnacondaInstaller.sh
```

## curl

```Dockerfile
curl=7.68.0-1ubuntu2.14
```

Usage:

- -o
- --silent
- --insecure/-k

```bash
curl --silent --insecure https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh -o ~/AnacondaInstaller.sh
```

- [How to ignore invalid and self signed ssl connection errors with curl](https://www.cyberciti.biz/faq/how-to-curl-ignore-ssl-certificate-warnings-command-option/)

## cifs-utils

Can mount using cifs-utils only (samba-client not required).

```Dockerfile
 cifs-utils=2:6.9-1ubuntu0.2\
```

Usage:

```bash
sudo mount -t cifs -o username=[username],password=[password] //[server]/[share] /path/to/mount

or
cat>cifs.cred
username=yours
password=yours
domain=yours
[Clt+C]

mount -t cifs -o credentials=/abs/path/cifs.cred //host/shared /mnt/shared --verbose
```

## coreutils

```Dockerfile
 coreutils=8.30-3ubuntu2\
```

includes `md4sum`

## dnsutils

```Dockerfile
 dnsutils=1:9.16.1-0ubuntu2.11\
```

## fonts-takao

```Dockerfile
 fonts-takao=00303.01-3ubuntu1\
```

## gawk

```Dockerfile
gawk=1:5.0.1+dfsg-1\
```

## gdebi

```Dockerfile
 gdebi=0.9.5.7+nmu3\
```

- [Ubuntuに拡張子がdebのパッケージをインストールする方法](https://kaworu.jpn.org/kaworu/2018-06-06-1.php)

## gedit

```Dockerfile
 dbus-x11=1.12.16-2ubuntu2.3\
 gedit=3.36.1-1\
```

## git

```Dockerfile
 git=1:2.25.1-1ubuntu3.6\
```

## glmark2

```Dockerfile
 glmark2=2021.02-0ubuntu1~20.04.1\
```

## gnome-terminal

```Dockerfile
 dbus-x11=1.12.16-2ubuntu2.3\
 at-spi2-core=2.36.0-2\
 gnome-terminal=3.36.2-1ubuntu1~20.04\
```

## gosu

```Dockerfile
 gosu=1.10-1ubuntu0.20.04.2\
```

## gpg ([The GNU Privacy Guard](https://en.wikipedia.org/wiki/GNU_Privacy_Guard))

```Dockerfile
 gpg=2.2.19-3ubuntu2.2\
```

It may be installed as a recommendation of gdebi.

## kdiff3

```Dockerfile
 breeze=4:5.18.8-0ubuntu0.1\
 kdiff3=1.8.01-1build1\
```

For WSL

```Dockerfile
&& echo "export XDG_RUNTIME_DIR=/tmp/runtime-root">>~/.bashrc \
```

## nano

```Dockerfile
 nano=4.8-1ubuntu1\
```

## nfs

```Dockerfile
 nfs-common=1:1.3.4-2.5ubuntu3.4\
```

```Dockerfile
 nfs-kernel-server=1:1.3.4-2.5ubuntu3.4\
```

## openssh-client

```Dockerfile
 openssh-client=1:8.2p1-4ubuntu0.5\
```

## rsync

```Dockerfile
 rsync=3.1.3-8ubuntu0.4\
```

## samba

```Dockerfile
 samba=2:4.13.17~dfsg-0ubuntu1.20.04.2\
```

## screen

```Dockerfile
 screen=4.8.0-1ubuntu0.1\
```

- without --no-install-recommends

## subversion

```Dockerfile
 subversion=1.13.0-3ubuntu0.2\
```

## smbclient

```Dockerfile
 smbclient=2:4.13.17~dfsg-0ubuntu1.20.04.2\
```

## supervisor

```Dockerfile
 supervisor=4.1.0-1ubuntu1\
```

## telnetd

```Dockerfile
 telnetd=0.17-41.2build1\
```

```bash
/usr/sbin/in.telnetd -debug 23
```

## vim

```Dockerfile
vim=2:8.1.2269-1ubuntu5.9 \
```

## vsftpd

```Dockerfile
 vsftpd=3.0.3-12\
```

## xauth

```Dockerfile
 xauth=1:1.1-0ubuntu1\
```

## x11-apps

```Dockerfile
 x11-apps=7.7+8 \
```

To install X11 client libraries and to test X11-client (xeyes, etc).

## xinetd

```Dockerfile
 xinetd=1:2.3.15.3-1\
```

- without --no-install-recommends

## xterm

```Dockerfile
 xterm=353-1ubuntu1.20.04.2
```

## Troubles

### Trouble 1 - httpsからのwgetが失敗する

```Dockerfile
# Use
apt -y install wget
# instead of
apt -y --no-install-recommends install wget
```

`--no-check-certificate`オプションで回避できるが、recommendsもインストールしたほうが良い。

```Dockerfile
wget --no-check-certificate https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh -O ~/AnacondaInstaller.sh
```

curlも同様。

### Trouble 2 - gedit終了時の警告

geditを終了時、以下の警告が表示される。

```text
(gedit:285): Tepl-WARNING **: 11:42:36.587: GVfs metadata is not supported. 
Fallback to TeplMetadataManager. 
Either GVfs is not correctly installed or GVfs metadata are not supported on this platform. 
In the latter case, you should configure Tepl with --disable-gvfs-metadata.
```
