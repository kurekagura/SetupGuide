# telnetd

xinetdなどのスーパーデーモンは利用せず、コマンド `/usr/sbin/in.telnetd` に オプション `-debug listenport` を渡すことで直接起動する。

## 権限

`in.telnetd` を起動するユーザーの補助グループにtelnetdがある必要がある。また、telnetするユーザーの補助グループにもtelnetdが必要である。

## ユーザーの属性変更に制約がある場合（sudoが不可）

例えば、Kubernetes上でPODとして提供されるコンテナなど、ユーザーへの補助グループ追加やデフォルトシェルの変更を行うことが出来ない場合（以下、usermodやchshはsudoが必要なため）、

```bash
usermod -aG telnetd taro
```

```bash
chsh -s /bin/bash taro
```

Dockerfile（build）の段階で、以下のファイルのパーミッションを変更する。

以下では、起動ユーザー、ログインユーザーの主グループもしくは補助グループの一つがrootグループであることを前提としている。chownでスティッキービットが外れるので、chmodで再セットする。

```Dockerfile
#root:telnetd->root:root
RUN chown root:root /usr/lib/telnetlogin && chmod 4755 /usr/lib/telnetlogin
```

```bash
# インストール直後
-rwsr-xr-- 1 root telnetd 14744 Mar 23  2020 /usr/lib/telnetlogin
# 変更後
-rwsr-xr-- 1 root root 14744 Mar 23  2020 /usr/lib/telnetlogin
```

## 起動と管理

コンテナ上で以下のコマンドで起動できる。但し、telnetクライアントから一度は接続できるものの、セッションが終了した時点で、in.telnetdも終了してしまう。

```bash
/usr/sbin/in.telnetd -debug 2323
```

この起動管理をSupervisordに担わせる。

## refs

- [man telnetd](https://linuxjm.osdn.jp/html/netkit/man8/telnetd.8.html)
