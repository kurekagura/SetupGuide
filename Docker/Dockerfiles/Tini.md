# [Tini](https://github.com/krallin/tini)

## ENTRYPOINTでの用法

複数のコマンドをシェルにする。

```Dockerfile
COPY DockerEntrypoint.sh /DockerEntrypoint.sh
RUN chmod 744 /DockerEntrypoint.sh

ENTRYPOINT ["tini", "--", "/DockerEntrypoint.sh"]
```

例）DockerEntrypoint.sh

1. supervisord の起動

```sh
#!/usr/bin/env sh

/usr/bin/supervisord
```
