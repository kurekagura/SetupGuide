# Linuxについて忘れてた事

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
perl -e "print(crypt('暗号化したいパスワード', '英数字2文字'));"
```

perlのcryptの引数（16文字と2文字）をランダムに生成する（出力をスペースで区切る）。

```bash
cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 18 | head -n 1 | cut -c 1-16,17-18 --output-delimiter=" "
```

[refs]

- [man useradd](https://linuxjm.osdn.jp/html/shadow/man8/useradd.8.html)
- [useraddコマンドでパスワードも指定する方法](https://www.steponboard.net/linux/756/)
- [ランダム文字列をたくさん生成する](https://qiita.com/Vit-Symty/items/5be5326c9db9de755184)

## 現在のシェルを知る

```sh
echo $SHELL
```

## chpasswd

- rootのみ可能
- `/etc/passwd` `/etc/shadow` を使っている場合。

```bash
echo "root:new password" | chpasswd
```

対話的に変更するには、`passwd` コマンド。

## kill

```bash
kill -TERM pid
```
