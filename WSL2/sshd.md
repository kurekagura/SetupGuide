# WSL2のUbuntuにSSHを構成する

## SSH Server（sshd）の構成

### Ubuntuでの作業

パッケージのインストール状況を確認する。

```bash
apt list openssh-server -a
# openssh-server/jammy,now 1:8.9p1-3 amd64 [installed]

apt list openssh-client -a
# openssh-client/jammy,now 1:8.9p1-3 amd64 [installed,automatic]
```

`sshd_config`の編集（`ssh_config`と間違わないように）。

```bash
sudo vi sshd_config

# パスワード認証方式⇒公開鍵認証方式を構成後に「no」にする。
PasswordAuthentication yes

# 公開鍵認証方式
# PubkeyAuthentication yes
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

```cmd
netsh.exe interface portproxy show v4tov4

ipv4 をリッスンする:         ipv4 に接続する:

Address         Port        Address         Port
--------------- ----------  --------------- ----------
*               22          172.22.198.252  22
```

このように構成するには、

```pwsh
netsh.exe interface portproxy add v4tov4 listenaddress=* listenport=22 connectaddress=172.22.198.252 connectport=22
```

とするか簡潔に以下でも同じ。

```pwsh
netsh.exe interface portproxy add v4tov4 listenport=22 connectaddress=172.22.198.252
```

リッスンアドレスには「*」ではなくホストのIPアドレスを指定しても良い。

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

## 公開鍵認証方式

`sshd_config` に `PubkeyAuthentication yes` を追記する。

```text
# 公開鍵認証方式の構成後、「no」にする。
PasswordAuthentication yes

# 公開鍵認証方式を有効化
PubkeyAuthentication yes
```

### クライアント（Linux）での秘密鍵生成

```bash
>ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/home/taro/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /hoem/taro/.ssh/id_rsa
Your public key has been saved in /home/taro/.ssh/id_rsa.pub
```

先ほど構成したパスワード認証SSH経由で、作成した公開鍵をサーバー側へコピーする。

```bash
>ssh-copy-id <Ubuntuのユーザー>@<ホスト名orホストのIPアドレス>

/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/taro/.ssh/id_rsa.pub"
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
xxx@xxx.xxx.xxx.xxx's password: <=Ubuntuのユーザーのパスワード

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'xxx@xxx.xxx.xxx.xxx'"
and check to make sure that only the key(s) you wanted were added.
```

パスワード認証と同じコマンドでログインする（※パスフレーズの入力を求められる）。

```bash
ssh <Ubuntuのユーザー>@<ホスト名orホストのIPアドレス>
```

【ssh-copy-idがやっていること】sshdが稼働している（Ubuntu on WSL）のホームディレクトリで、`cat .ssh/authorized_keys`（ファイル） すると理解できる。このファイルに複数の公開鍵が追記される。

### クライアント（Windows10）での秘密鍵生成

```cmd
# where ssh-keygen
# C:\Windows\System32\OpenSSH\ssh-keygen.exe

>ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (C:\Users\taro/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in C:\Users\taro/.ssh/id_rsa.
Your public key has been saved in C:\Users\taro/.ssh/id_rsa.pub.
```

先ほど構成したパスワード認証SSH経由で、作成した公開鍵をサーバー側へコピーする。Windows版ssh-copy-idは提供されていないため、以下のPowerShellを実行する（<>を適切に設定）。

```pwsh
cat ~/.ssh/id_rsa.pub | ssh <Ubuntuのユーザー>@<ホスト名orホストのIPアドレス> `
"mkdir -p ~/.ssh && chmod 700 ~/.ssh && `
cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

⇒ 生成した秘密鍵（ C:\Users\taro/.ssh/id_rsa）は RLogin などのSSHターミナルソフトでも利用できる。

⇒ dockerのLinuxコンテナから一時的に秘密鍵を共有したい場合、次のように起動すると可能。

但し、起動後にパーミッションを600に設定する必要がある（一度でOK）。``chmod 600 ~/.ssh/id_rsa``

```pwsh
docker run -v ""${env:USERPROFILE}\.ssh"":""/root/.ssh"" -it tmpimage /bin/bash
```

### パスワード認証方式の無効化

公開鍵認証方式を構成後はパスワード認証方式を無効化しておく。

## [refs]

- [Windows Subsystem for Linuxにssh接続する](https://qiita.com/ezmscrap/items/30eaf9531e240c992cf1)
- [WSLで作成したUbuntu環境にSSH接続する](https://ashitaka-blog.com/2022-07-03-215650/)
- [Windowsでssh-copy-idっぽいことをしたい](https://qiita.com/tabu_ichi2/items/446722c15e6b5678ccad)
