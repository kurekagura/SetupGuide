# VcXsrv

## HELP（引数など）を見る

`vcxsrv.exe -h` で exeと同フォルダに `XWin.log` が作成され、それにオプションの説明がある（[wiki](https://sourceforge.net/p/vcxsrv/wiki/Using%20VcXsrv%20Windows%20X%20Server/)にも同様の内容が記載）。

## "Disable Access Control"オプション

「アクセス制御をする」機能をどのように利用するのか？

作成した `.Xauthority` ファイルをホスト側へ渡すためにdockerのVolumeを使う。

```powershell
docker run `
    -v ""${env:userprofile}"":""/userprofile"" `
    --name=containername `
    -d -it imangename
```

コンテナ側で、`.Xauthority` を生成する。

```bash
> echo $DISPLAY
xxx.xxx.xxx.xxx:0.0
#名前解決できればホスト名でもOK

> xauth list
xauth:  file /root/.Xauthority does not exist

> magiccookie=$(echo 'some-pass-phrase'|tr -d '\n\r'|md5sum|gawk '{print $1}')
> xauth add "$DISPLAY" . "$magiccookie"
xauth:  file /root/.Xauthority does not exist

> xauth list
xxx.xxx.xxx.xxx:0  MIT-MAGIC-COOKIE-1  md5sumの結果の1列目

> cp ~/.Xauthority /userprofile
```

VcxSrvの起動ショートカットを作る。

```text
path\to\vcxsrv.exe -multiwindow -clipboard -auth "path\to\.Xauthority" 
```

## オプション

helpから抜粋。

- -ac<br>
    disable access control restrictions
- -auth file<br>
    select authorization file
- -[no]wgl<br>
    Enable the GLX extension to use the native Windows WGL interface for hardware-accelerated OpenGL
- -swrastwgl<br>
    Enable the GLX extension to use the native Windows WGL interface based on the swrast interface for accelerated OpenGL

## refs

- [Windows 10 Pro Version 20H2 Setup For WSL2](https://sourceforge.net/p/vcxsrv/wiki/VcXsrv%20&%20Win10/)
