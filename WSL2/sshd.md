# WSL2のUbuntuにSSHを構成する

## SSH Server（sshd）の構成

### Ubuntuでの作業

インストール済みを確認する。

```bash
apt list openssh-server -a
# openssh-server/jammy,now 1:8.9p1-3 amd64 [installed]

apt list openssh-client -a
# openssh-client/jammy,now 1:8.9p1-3 amd64 [installed,automatic]
```

`sshd_config`の編集（`ssh_config`と間違わないように）。

```bash
sudo vi sshd_config

PasswordAuthentication yes
PubkeyAuthentication yes
```

ホスト鍵の生成

```bash
sudo ssh-keygen -A
# ssh-keygen: generating new host keys: RSA DSA ECDSA ED25519
```

サービス起動

```bash
sudo service ssh start
# * Starting OpenBSD Secure Shell server sshd    [ OK ]
```

### Host（Windows）での作業

ポートフォワードの設定

クライアントからの接続に127.0.0.1ではなく、ホストのIPアドレスを指定した場合、以下のように*としておかないと接続に失敗した（原因は不明）。

```cmd
netsh.exe interface portproxy show v4tov4

ipv4 をリッスンする:         ipv4 に接続する:

Address         Port        Address         Port
--------------- ----------  --------------- ----------
*               22          172.22.198.252  22
```

このような設定とするには、

```pwsh
netsh.exe interface portproxy add v4tov4 listenaddress=* listenport=22 connectaddress=172.22.198.252 connectport=22
```

とするか簡潔に以下でも同じ。

```pwsh
netsh.exe interface portproxy add v4tov4 listenport=22 connectaddress=172.22.198.252
```

UbuntuのIPアドレスは内部DHCPにより変わるため以下で調べる。

```pwsh
wsl -d Ubuntu-20.04 -e hostname -I
# 172.22.198.252
```

## クライアントからのSSH接続

ホスト外からSSHする場合、Windows Firewall（`wf.msc`）でポートを許可するルールを追加しておく。

### Windows

パスワード認証で確認

```cmd
ssh <Ubuntuのユーザー>@<ホスト名orホストのIPアドレス>
# where ssh
# C:\Windows\System32\OpenSSH\ssh.exe
```

### Linux Container（on Dokcer Desktop）

パスワード認証で確認

```bash
ssh <Ubuntuのユーザー>@<ホスト名orホストのIPアドレス>
```

[refs]

- [Windows Subsystem for Linuxにssh接続する](https://qiita.com/ezmscrap/items/30eaf9531e240c992cf1)
