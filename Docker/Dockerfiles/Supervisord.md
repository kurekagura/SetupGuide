# [supervisord](http://supervisord.org/)

## Dockerfile

```Dockerfile
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]
```

## telnetd

```conf
[supervisord]
nodaemon=true

[program:telnetd]
command=/usr/sbin/in.telnetd -debug 23
autorestart=true
```

rootでない場合、well-knownポートの23はオープンできないので、それ以外にする。
