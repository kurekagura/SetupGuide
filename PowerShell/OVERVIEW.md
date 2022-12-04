# OVERVIEW

## Check version and basic information

```pwsh
$PSVersionTable
$profile | Format-List -Force
$host.name
$PSHome
```

## About profile

```pwsh
$profile | Format-List -Force
```

```text
AllUsersAllHosts       : C:\Windows\System32\WindowsPowerShell\v1.0\profile.ps1
AllUsersCurrentHost    : C:\Windows\System32\WindowsPowerShell\v1.0\Microsoft.PowerShell_profile.ps1
CurrentUserAllHosts    : %USERPROFILE%\Documents\WindowsPowerShell\profile.ps1
CurrentUserCurrentHost : %USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1
```

\* %USERPROFILE% is, for example, C: \Users\taro.

```text
$profile
C:\Users\taro\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1
=> Show only CurrentUserCurrentHost
```

In PowerShell, Host means `$host`. For example of `$host.name`, "Windows PowerShell ISE Host" or "ConsoleHost".

## About Execution Policies

To get all of the execution policies that affect the current session and display them **in precedence order**:

```pwsh
Get-ExecutionPolicy -List
```

The following command gets the effective execution policy:

```pwsh
Get-ExecutionPolicy
```

```pwsh
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

The default for Scope is LocalMachine. To change the execution policy for LocalMachine, start PowerShell with the Run as administrator.

## How to check if PowerShell is 32-bit or 64-bit

```pwsh
[System.Environment]::Is64BitProcess
$PSHome
$profile|fl -Force
```

On "Windows PowerShell"

```text
True

C:\Windows\System32\WindowsPowerShell\v1.0

AllUsersAllHosts       : C:\Windows\System32\WindowsPowerShell\v1.0\profile.ps1
AllUsersCurrentHost    : C:\Windows\System32\WindowsPowerShell\v1.0\Microsoft.PowerShell_profile.ps1
CurrentUserAllHosts    : C:\Users\taro\Documents\WindowsPowerShell\profile.ps1
CurrentUserCurrentHost : C:\Users\taro\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1
```

On "Developer PowerShell for VS 2019" or "Developer PowerShell for VS 2022"

```text
False

C:\Windows\SysWOW64\WindowsPowerShell\v1.0

AllUsersAllHosts       : C:\Windows\SysWOW64\WindowsPowerShell\v1.0\profile.ps1
AllUsersCurrentHost    : C:\Windows\SysWOW64\WindowsPowerShell\v1.0\Microsoft.PowerShell_profile.ps1
CurrentUserAllHosts    : C:\Users\taro\Documents\WindowsPowerShell\profile.ps1
CurrentUserCurrentHost : C:\Users\taro\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1
```

Note that AllUsers\* profile.ps1 is different, but CurrentUser\* profile.ps1 is shared.

## Reference

- [PowerShellのホストとプロファイルについてまとめ](https://blog.shibata.tech/entry/2016/10/07/225835)
- [管理権限を持っていないユーザーで PowerShell スクリプトを実行する](http://www.vwnet.jp/windows/PowerShell/2020072901/SetExecutionPolicy.htm)
- [WindowsでPowerShellスクリプトの実行セキュリティポリシーを変更する](https://atmarkit.itmedia.co.jp/ait/articles/0805/16/news139.html)
- [64bit版Windowsで32bit版PowerShellを実行する際の問題](https://qiita.com/mnimo/items/01e2d7777b156dac18f6)