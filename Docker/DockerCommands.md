# docker commands

## run -d

Detach(-d)して、Runnning状態とする。即座にExitedにならないよう（Docker DesktopのTerminalからログインできるよう）、[ENTRYPOINT]や[CMD]で呼び出す最後のコマンドでブロッキングされるようにしておく。

```PowerShell
docker run -d image
```

## run -u

UID/GIDはint32の最大値2^31-1( 2147483647 )のため、0-2147483647を指定できる。

```PowerShell
docker run -u 2147483647 -d image
```

存在しないuidを指定した場合、idコマンドの結果は以下のようになるものの、/etc/passwd,shadow,group にはレコードはない。

```bash
$ id
uid=2147483647 gid=0(root) groups=0(root)
```

以下のように作成することもできる（別途で防護策は必要）。

```Dockerfile
RUN chmod g+w /etc/passwd
#root:shadow->root:root 640->660
RUN chgrp root /etc/shadow && chmod g+w /etc/shadow
```

```sh
#!/usr/bin/env sh
echo "`id -n -u`:x:`id -n -u`:0::/root_group:/bin/bash" >> /etc/passwd
echo "`id -n -u`::19354:0:99999:7:::" >> /etc/shadow
```

## run -v

```PowerShell
docker run -v ""O:\home\taro"":""/home/taro"" -d image
```

- ""path""（PowerShell）

## run --tmpfs

/tmpにはスティッキービットが立っている。コンテナ上では、ファイルは作成できるものの、ディレクトリは作成できない（理由は不明）。--tmpfsを使うとこの問題を回避できる。

```sh
$ ls -ld /tmp
drwxrwxrwt 1 root root 4096 Dec 28 14:56 /tmp

```PowerShell
docker run --tmpfs /tmp -d image
```

## run --gpus all

```PowerShell
docker run `
    --gpus all `
    --ulimit memlock=-1 --ulimit stack=8388608 `
    --ipc=host `
    -d -it image
```
