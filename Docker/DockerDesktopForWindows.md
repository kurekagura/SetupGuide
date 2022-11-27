# Distroが格納されるファイル(.vhdx)の場所を移動する。

[[docker docs] Docker Desktop WSL 2 backend on Windows](https://docs.docker.com/desktop/windows/wsl/)
>Docker Desktop installs 2 special-purpose internal Linux distros docker-desktop and docker-desktop-data. The first (docker-desktop) is used to run the Docker engine (dockerd) while the second (docker-desktop-data) stores containers and images. Neither can be used for general development.

|distro|役割|既定の場所|
|:---|:---|:---|
|docker-desktop|Dockerエンジン（dockerd）を実行するために使用|%LocalAppData%\Docker\wsl\data\ext4.vhdx|
|docker-desktop-data|コンテナやイメージを保存するために使用|%LocalAppData%\Docker\wsl\distro\ext4.vhdx|

`docker-desktop-data(=\distro\ext4.vhdx)` が肥大化するため、任意の場所に移動させる。

<ins>【注意】ディストロ名のdocker-desktop-`data`とフォルダ`data`とが互い違いとなっているので間違わないように。</ins>

<ins>【2022/11/27追記】再インストールしたv4.14.1ではdocker-desktopとdocker-desktop-dataのファイル配置が上記の表とは逆転してような気がする</ins>

普通のコマンドプロンプトを起動。

停止と確認
```
>wsl --shutdown

>wsl -l -v
  NAME                   STATE           VERSION
* Ubuntu-22.04           Stopped         2
  docker-desktop         Stopped         2
  docker-desktop-data    Stopped         2

# 作業フォルダの作成。
# tarファイルが保存できるだけの空きスペースが必要。
>mkdir mytmp & cd mytmp
```

`docker-desktop-data`をtarファイルへ出力する。
```
wsl --export docker-desktop-data docker-desktop-data.tar
```

`docker-desktop-data`の登録を解除（削除）する。

<ins>【注意】ext4.vhdxが削除される。</ins>
```
wsl --unregister docker-desktop-data
```

`docker-desktop-data`の登録、tarファイルからインポートする。この時、移動先のフォルダは事前に作成しておいた。
```
mkdir o:\.wsldata\%USERNAME%
wsl --import docker-desktop-data o:\.wsldata\%USERNAME% docker-desktop-data.tar --version 2
```
importが成功するとtarファイルは不要。

※ 一度目は成功し運用していたが、二度目は失敗した（Docker DesktopがStarting状態のまま起動しなくなったので、最インストールした）。

## 参考

- [WSL2 Dockerのイメージ・コンテナの格納先を変更したい (WSL2のvhdxファイルを移動させたい)](https://qiita.com/neko_the_shadow/items/ae87b2480345152bc3cb)
- [Docker Desktop for Windows のデータを別のドライブに移動する](https://chizuwota.net/wsl/wsl2-move-docker-vdisk/)

- [WSL Docker のデータ保存場所を変更する](https://qiita.com/takelushi/items/94862caf2933275a02f7)

# 複数アカウントでの共有

上記の.vhdxをWindows10の複数アカウントで同じものを指定できそうであるが、誤って複数アカウントから同時アクセスした場合に壊れそうなのでやめておく。

- [How can I make Docker Desktop work for multiple users? "ERROR: Docker Desktop is not running" while Docker is working properly](https://stackoverflow.com/questions/74155397/how-can-i-make-docker-desktop-work-for-multiple-users-error-docker-desktop-is)
