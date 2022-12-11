# WSL2のIPアドレスについて

## 調べる方法

Windowsから ipconfig で表示される `vEthernet (WSL)`に割り当てられているのがWSLのIPアドレス（以降、WSL2のIPアドレス）。

またはPowerShellのCmdletを使うと抽出できる。

```pwsh
Get-NetIPConfiguration|Where-Object {$_.InterfaceAlias -eq 'vEthernet (WSL)'}|Select-Object IPv4Address
```

Ubuntuを起動し `ip a` や `ip a show dev eth0` 、 `ip r` でUbuntuのIPアドレスとデフォルトゲートウェイを調べることができる。

自分の環境での結果：

|adapter|ip,etc(例1)|ip,etc(例2)|
|:--:|:--|:--|
|vEthernet (WSL)|172.25.112.1/20|172.22.192.1|
|Ubuntu-20.04 eth0|172.25.120.1/20<br>brd 172.25.127.255<br>default via 172.25.112.1|172.22.192.108/20<br>brd 172.22.207.255<br>default via 172.22.192.1|
|Ubuntu-22.04 eth0|172.25.120.1/20<br>brd 172.25.127.255<br>default via 172.25.112.1|172.22.192.108/20<br>brd 172.22.207.255<br>default via 172.22.192.1|

```text
/20=255.255.240.0=255.255.[1111|0000].0

172.25.112.1/20=172.25.[0111|0000].1

172.25.120.1/20=172.25.[0111|1000].1

brd
172.25.127.255=172.25.[0111|1111].255

default via
172.25.120.1=172.25.[0111|1000].1
```

3つのNICは同じサブネットに属していて、2つのUbuntuが同一IPになっている。

## 特徴

- OS再起動でWSL2のIP/サブネットは自動割り当てされる（変わる）。
- `wsl.exe --shutdown`や`wsl -t Ubuntu-20.04`ではWSL2のIPは変わらないがUbuntuは変わる。
- WSL2にはクラスBのプライベートアドレスが割り当てられるよう（ホストWindowsにクラスCを割り当てているので、これを避けてクラスBが割り当てられているのかも）。

```text
クラスB：172.16.0.0～172.31.255.255 （172.16.0.0/12）
クラスC：192.168.0.0～192.168.255.255 （192.168.0.0/16）
クラスA：10.0.0.0～10.255.255.255 （10.0.0.0/8）
```

## PowerShellスクリプトから

IPの取得

```pwsh
# WSLのIPを取得
$WSLIP=(Get-NetIPConfiguration|Where-Object {$_.InterfaceAlias -eq 'vEthernet (WSL)'}|Select-Object -ExpandProperty IPv4Address).IPAddress

# 内部UbuntuのIPを取得
$ubuntu_ip = wsl -d Ubuntu-20.04 -e hostname -I
# -dはきちんと効いている
```

ポートプロキシの設定

```pwsh
#【重要】.ps1内では、iexで呼び出す必要がある。
Invoke-Expression "netsh.exe interface portproxy add v4tov4 listenaddress=$HOSTIP listenport=$Port connectaddress=$UBUNTUIP connectport=$Port"

# 直接netshを呼び出した場合、showでみても成功しているようにしか見えないのだが、機能しない。
netsh.exe interface portproxy add v4tov4 listenaddress=$HOSTIP listenport=$Port connectaddress=$UBUNTUIP connectport=$Port
netsh.exe interface portproxy show v4tov4
```

[netsh not working when run via Invoke-Command](https://stackoverflow.com/questions/50041418/netsh-not-working-when-run-via-invoke-command)

[refs]

- [Windows WSL2に外部から直接アクセスするための設定](https://rcmdnk.com/blog/2021/03/01/computer-windows-network/#windows%E8%B5%B7%E5%8B%95%E6%99%82%E3%81%AB%E3%81%A4%E3%81%AA%E3%81%92%E3%82%8B)
