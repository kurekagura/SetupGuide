# ssh

良く使うオプションの意味(manより引用)

- -N : Do not execute a remote command
- -f : Requests ssh to go to background just before command execution.

## リモートポートフォワード

sshdhost:23へのリクエストをlocalhost:2323へ転送。

```cmd
ssh -R 23:localhost:2323 taro@sshdhost -N -f
```

## ローカルポートフォワード

localhost:6000へのリクエストをsshdhost:6666へ転送。

```cmd
ssh -L 6000:localhost:6666 taro@sshdhost -N -f
```

[refs]

- [man ssh](https://man7.org/linux/man-pages/man1/ssh.1.html)