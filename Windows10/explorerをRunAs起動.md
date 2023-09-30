# エクスプローラをRunAs起動

Windows7以降（？）、Elevated-Unelevated Explorer Factoryという仕組みが入っているらしく、"C:\windows\explorer.exe"をRunAs（Shift+右クリック→「別のユーザーとして実行」）出来なくなっています。

## 設定方法

regeditで以下を変更します（昇格プロンプトが表示される）。

HKEY_CLASSES_ROOT\AppID\{CDCBCFCA-3CDC-436f-A4E2-0E02075250C2}

右クリック→アクセス許可より、

所有者をTrustedInstallerからAdministratorsに変更します。そしてAdministratorsのフルコントロールにチェックします。名前「RunAs」を（名前は何でもよい）「_RunAs」に変更します。

これでExplorerファクトリが無効になるようです。

## 実行

以下のようにコマンドラインからrunas実行します。

※「管理者として実行」をする必要はありません。  
※ /noprofileを付けないとエクスプローラが起動しません。

```console
runas /noprofile /user:yakumo\test-user1 "c:\windows\explorer.exe /separate"
```

## 参考

[Runas Windows Explorer in Windows 7](https://superuser.com/questions/55013/runas-windows-explorer-in-windows-7)

[robderickson/RunAsExplorer.md](https://gist.github.com/robderickson/8260f6d28f29fc123c63d18b43d12ba4)
