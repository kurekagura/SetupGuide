# Linuxについて忘れてた事

## /tmp

/tmpにはスティッキービットが立っている。

```sh
$ ls -ld /tmp
drwxrwxrwt 1 root root 4096 Dec 28 14:56 /tmp
```

スティッキービットを立てるには

```sh
chmod o+u <ディレクトリ>
# or
chmod 1777 <ディレクトリ>
```

[Docker]

ファイル作成は行えるが、ディレクトリは不可のようだ。--tmpfsを使う。

## /etc/skel/

.bashrc等のテンプレートがある。

[refs]

- [useradd時のホームディレクトリのスケルトン](https://install-memo.hatenadiary.org/entry/20091006/1254837600)

## useradd

Ubuntuではadduserは対話的にユーザーを作る場合に使う。

```bash
useradd -m -N -s /bin/bash -p <crypt関数で暗号化したパスワード> taro
```

```bash
perl -e "print(crypt('暗号化したいパスワード', '\$6\$salt'));'
```

perlのcryptの引数（16文字と2文字）をランダムに生成する（出力をスペースで区切る）。

```bash
cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 18 | head -n 1 | cut -c 1-16,17-18 --output-delimiter=" "
```

[refs]

- [man useradd](https://linuxjm.osdn.jp/html/shadow/man8/useradd.8.html)
- [useraddコマンドでパスワードも指定する方法](https://www.steponboard.net/linux/756/)
- [ランダム文字列をたくさん生成する](https://qiita.com/Vit-Symty/items/5be5326c9db9de755184)
- [4. パスワードを指定してユーザーを追加](https://qiita.com/yasushi-jp/items/71348799cf6db9759935#4-%E3%83%91%E3%82%B9%E3%83%AF%E3%83%BC%E3%83%89%E3%82%92%E6%8C%87%E5%AE%9A%E3%81%97%E3%81%A6%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%E3%82%92%E8%BF%BD%E5%8A%A0)

## usermod

```bash
sudo usermod -aG telnetd taro
```

## 現在のシェルを知る

```sh
echo $SHELL
```

## chpasswd

- rootのみ可能
- `/etc/passwd` `/etc/shadow` を使っている場合。
- 対話的に変更するには、`passwd` コマンド。

```bash
echo "root:new password" | chpasswd
```

- --encrypted <暗号化パスワード>

```bash
printf 'taro:$6$<SALT>$<SHA-512ハッシュ化パスワード>' | chpasswd --encrypted

# $6$ ハッシュ化にSHA-512を使っていることを示す。
# $<SALT>$ Ubuntu20.4では16桁であった
# /etc/shadowで確認できる。
```

perlで生成できる。

```perl
perl -e 'print crypt("password", "\$6\$<SALT>");'
```

[refs]

- [ユーザ作成・追加の方法](https://www.server-memo.net/centos-settings/system/useradd.html)
- [メモ：シェルスクリプトでパスワードを設定するにはchpasswdが使えるかも](https://notchained.hatenablog.com/entry/2016/09/03/130454)
- [OpenSSLでSHA512のPASSWORDを生成する](https://matoken.org/blog/2019/03/15/generate-a-sha512-password-with-openssl/)
- [【CentOS】/etc/shadowのハッシュ化パスワードについて](https://www.unknownengineer.net/entry/2017/08/16/184537)

## chsh

ログインシェルを変更する。対象ユーザーを指定することもできる。

```sh
chsh -s /bin/bash taro
```

## cut

文字列を区切り文字で切り出す。

```sh
#ファイル末尾のユーザーを切り出す
tail /etc/passwd -n 1|cut -d":" -f 1
```

## kill

```bash
kill -TERM pid
```

## ps

- -A, -e : all processes
- -f : full-format, including command lines
- --help a : 全ヘルプ参照

```sh
ps -Af
```

## tee

標準エラー出力2を標準出力1へとリダイレクトし、この標準出力をパイプでteeの入力とする（-aは追記）。

```bash
command 2>&1 | tee -a stdout_and_err.txt
```

## time

コマンドの処理時間を計る。
