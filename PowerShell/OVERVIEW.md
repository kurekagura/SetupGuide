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
CurrentUserAllHosts    : C:\Users\taro\Documents\WindowsPowerShell\profile.ps1
CurrentUserCurrentHost : C:\Users\taro\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1
```

```text
$profile
C:\Users\taro\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1
=> Show only CurrentUserCurrentHost
```

In PowerShell, Host means `$host`. For example of `$host.name`, "Windows PowerShell ISE Host" or "ConsoleHost".

## Reference

- [PowerShellのホストとプロファイルについてまとめ](https://blog.shibata.tech/entry/2016/10/07/225835)
