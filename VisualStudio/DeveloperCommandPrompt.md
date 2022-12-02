# 「Visual Studio開発者コマンドプロンプト」関係

英語では「Developer Command Prompt for VS 20XX」です（Google検索で使う）

## 「x64 Developer PowerShell for VS 2019」を作る

何故か以下のx86用のものしか提供されていない。

"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Visual Studio 2019\Visual Studio Tools\Developer PowerShell for VS 2019.lnk"

```cmd
(gcm cl).Source
C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\bin\HostX86\x86\cl.exe
```

これをコピーし「x64 Dev PowerShell VS2019」などの名前に変更し、リンク先を書き換える。

```text
C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe -noe -c "&{Import-Module """C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\Tools\Microsoft.VisualStudio.DevShell.dll"""; Enter-VsDevShell ●●●●●●●●}"
↓
C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe -noe -c "&{Import-Module """C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\Tools\Microsoft.VisualStudio.DevShell.dll"""; Enter-VsDevShell ●●●●●●●● -DevCmdArguments -arch=x64}"
```

参考

-[Developer PowerShell for VS 2019をx64に切り替える方法](http://mklearning.blogspot.com/2019/12/developer-powershell-for-vs-2019x64.html)