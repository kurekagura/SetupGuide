# Windows OpenSSH Server

## インストール

[アプリと機能]-[オプション機能]から「OpenSSH サーバー」をインストールできる。

`%programdata%\ssh\sshd_config`

OpenSSH

テンプレート `C:\Windows\System32\OpenSSH\sshd_config_default` を `%programdata%\ssh\sshd_config` としてコピーする。

後者のフォルダは最初、空であるが、sshdを起動すると複数のファイル（ホスト認証用の秘密鍵と公開鍵）が作成された。

`services.msc`

サービス名：sshd　表示名：OpenSSH SSH Server
スタートアップの種類：手動

PowerShellを管理者として実行、sshdを起動する

```PowerShell
start-service sshd
```

再起動は

```PowerShell
restart-service sshd -force
```

自動起動にする場合。

```PowerShell
Set-Service sshd -StartupType 'Automatic'
```

## ファイアーウォール設定

管理者として実行、「受信の規則」を作成。

```PowerShell
netsh advfirewall firewall add rule name=".MY_SSHD" dir=in action=allow protocol=TCP localport=22　description="私が作成した"
```

Windowsファイアーウォール `wf.msc` で確認。

有効/無効の切換え。

```PowerShell
netsh advfirewall firewall set rule name=".MY_SSHD" new enable=yes/no
```

## パスワード認証と公開鍵認証の有効化

既定ではパスワード認証であるが、後の為に公開鍵認証を有効にしておく。管理者権限でないと編集できない(notepadを管理者として実行)。

```ini
# 後で公開鍵認証にするため有効にしておく。
PubkeyAuthentication yes
# 公開鍵認証方式を構成後にnoに変更、無効化する。
PasswordAuthentication yes
```

## Linux SSHクライアントからの接続

```PowerShell
docker run --name=tmpcontainer -p 22:22 -d -it tmpimage-gpu
```

```bash
# host\winuser1のhostは不要。
# domain\winuser1のdomainは必要かも（winuser1@domain@host）
ssh winuser1@host.docker.internal

The authenticity of host 'host.docker.internal (<コンテナから見たホストのIP>)' can't be established.
ECDSA key fingerprint is SHA256:<hoge>.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'host.docker.internal,<コンテナから見たホストのIP>' (ECDSA) to the list of known hosts.
winuser1@host.docker.internal's password: <= winuser1のパスワード入力
```

### 秘密鍵の生成と公開鍵の転送

**Windows側ユーザーがAdministratorsの場合**の方法を示す。

※ 一般ユーザの場合は、公開鍵の保存先が異なるので注意。

また暗号化アルゴリズムは既定の `RSA`（-tでEd25519等を指定できる）、鍵を生成するディレクトリは既定の `~/.ssh` とする（-f で指定できる）。

```bash
>ssh-keygen
Enter passphrase (empty for no passphrase): <= パスフレーズ入力
#./sshに秘密鍵（id_sra）と公開鍵（id_sra.pub）が生成される。
```

SSHパスワード認証経由で、作成した公開鍵を Windows OpenSSH Server 側へコピーする。

コピー先を、一旦、 `C:/ProgramData/ssh/任意のファイル名` としておく。

```bash
scp ~/.ssh/id_rsa.pub winuser1@host.docker.internal:C:/ProgramData/ssh/winuser1_rsa.pub
```

Server 側で、`administrators_authorized_keys` へ追記する（存在しない場合は新規に作成）。

```PowerShell
#ファイルが無ければ作成。存在した場合でもエラーになるのみ。
New-Item ${env:programdata}/ssh/administrators_authorized_keys

#既に他の公開鍵が記録されている場合は追記となる。
Get-Content ${env:programdata}/ssh/winuser1_rsa.pub -Encoding UTF8 | Out-File -Encoding UTF8 ${env:programdata}/ssh/administrators_authorized_keys -Append

#「UTF8 BOM付き」となるが問題は発生してない。
```

`administrators_authorized_keys`の権限設定を変更する必要がある。

```PowerShell
icacls.exe "C:\ProgramData\ssh\administrators_authorized_keys" /inheritance:r /grant "Administrators:F" /grant "SYSTEM:F"
```

例えば、追記の場合。

```bash
scp ~/.ssh/id_ed25519.pub winuser2@host.docker.internal:C:/ProgramData/ssh/winuser2_ed25519.pub
```

```PowerShell
Get-Content ${env:programdata}/ssh/winuser2_ed25519.pub -Encoding UTF8 | Out-File -Encoding UTF8 ${env:programdata}/ssh/administrators_authorized_keys -Append
```

Linuxから接続。※ -i で秘密鍵を指定できる。

```bash
ssh winuser1@host.docker.internal
```

## Administratorsメンバの特殊設定

sshd_configの設定をコメントアウトすると一般ユーザーとして扱えるようだ。

```ini
Match Group administrators
       AuthorizedKeysFile __PROGRAMDATA__/ssh/administrators_authorized_keys
```

## Troubles

### ssh-copy-id が上手く行かない

ssh-copy-idコマンドで、`%userprofile%/.ssh/authorized_keys`（ファイル）に公開鍵を追記できるば、コンソールによっては、上手く行かない（以下の標準出力の�...�が原因と思われる。authorized_keysが不正な行 " ; } " が追加されてしまうので削除した）。

```bash
>ssh-copy-id winuser1@host.docker.internal

/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/taro/.ssh/id_rsa.pub"
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
xxx@xxx.xxx.xxx.xxx's password: <= winuser1のパスワード入力

'exec' �...�
'cat' �...�
```

### 一般ユーザの場合

Administratorsではないユーザーの場合の公開鍵の追記先ファイルは、`%userprofile%/.ssh/authorized_keys` である。

## refs

- [【MSDocs】公開キーのデプロイ](https://learn.microsoft.com/ja-jp/windows-server/administration/openssh/openssh_keymanagement#deploying-the-public-key)
