# rsync daemon on WSL

## Install Ubuntu on WSL

```cmd
wsl -l -v
# List the distributions available for installation
wsl --list --online

wsl --install -d Ubuntu-20.04
#Enter new UNIX username:
#New password:
```

```cmd
# To uninstall
wsl --shutdown 
wsl --unregister Ubuntu-20.04
```

## rsync daemon settings on Ubuntu

```bash
mkdir ${HOME}/rsyncd
vim ${HOME}/rsyncd/rsyncd.conf
```

```text
use chroot = no
#hosts allow = xxx.xxx.x.x
log file = /home/taro/rsyncd/rsyncd.log
port = 8873
secrets file = /home/taro/rsyncd/secrets

[mytmp]
read only = true
path = /mnt/c/mytmp
auth users = <whatever you want>
```

```bash
cat > ${HOME}/rsyncd/secrets
<whatever you want>:<password>
Ctr+C

chmod 600 ${HOME}/rsyncd/secrets
ll ${HOME}/rsyncd/secrets
-rw------- 1 taro taro 10 Dec 10 00:24 /home/taro/rsyncd/secrets
```

## portproxy the host to this Ubuntu

In this Ubuntu, check ip address with this Ubuntu.

```bash
ip a show dev eth0
# For example, 172.19.131.253/20
```

Run Console as Aministrator on the host Windows,

```cmd
netsh.exe interface portproxy add v4tov4 listenaddress=<host ip> listenport=8873 connectaddress=172.19.131.253 connectport=8873

netsh.exe interface portproxy show v4tov4
```

To delete after that.

```cmd
netsh.exe interface portproxy delete v4tov4 listenport=8873 listenaddress=<host ip>
```

## Start rsync as daemon mode

In this Ubuntu,

```bash
rsync --daemon --config=/home/taro/rsyncd/rsyncd.conf --no-detach
```

## rsync client

```bash
rsync -av rsync://<host>:8873/mytmp /root/mytmp/
#Password:
```

## refs

- [rsync server using Windows Subsystem for Linux](https://serverfault.com/questions/878887/rsync-server-using-windows-subsystem-for-linux)
- [man rsyncd.conf](https://man7.org/linux/man-pages/man5/rsyncd.conf.5.html)
