param(
    [parameter(mandatory=$true)][int32]$InterfaceIndex,
    [int32]$Port=873,
    [ValidateSet("Ubuntu-20.04","Ubuntu-22.04")][String]$Distro="Ubuntu-20.04")

$HOSTIP = (Get-NetIPConfiguration|Where-Object {$_.InterfaceIndex -eq $InterfaceIndex}|Select-Object -ExpandProperty IPv4Address).IPAddress
$UBUNTUIP = wsl -d $Distro -e hostname -I
Invoke-Expression "netsh.exe interface portproxy add v4tov4 listenaddress=$HOSTIP listenport=$Port connectaddress=$UBUNTUIP connectport=$Port"
#If($LastExitCode -gt 0) {throw}
#If InterfaceIndex is invalid, netsh.exe just shows help.

netsh.exe interface portproxy show v4tov4

if([string]::IsNullOrEmpty($HOSTIP)){
    $HOSTIP = "<SRC IP>"
}
Write-Host "If you want to delete, use the following command with run as Administrator."
Write-Host "> netsh.exe interface portproxy delete v4tov4 listenaddress=$HOSTIP listenport=$PORT"
Write-Host "and you can check it."
Write-Host "> netsh.exe interface portproxy show v4tov4`n"
