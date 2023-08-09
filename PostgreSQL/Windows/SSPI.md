# SSPIの構成

## 環境①

- Windows 10 Pro
- postgresql-15.3-4-windows-x64.exe
- pgadmin4-7.5-x64.exe（上記同梱はインスコせずに、こちらを単体インスコ）

```plaintext
host  all  postgres  127.0.0.1/32  sspi map=MapForSSPI
host  all  winuser1  127.0.0.1/32  sspi map=MapForSSPI
host  all  postgres  ::1/128  sspi map=MapForSSPI
host  all  winuser1  ::1/128  sspi map=MapForSSPI

host  all  all  127.0.0.1/32  scram-sha-256
host  all  all  ::1/128  scram-sha-256
```

【重要】scram-sha-256の行をsspiよりも上に記述するとダメだった。

```plaintext
# MAPNAME     SYSTEM-USERNAME PG-USERNAME
MapForSSPI    winuser1@pc1    winuser1
MapForSSPI    winuser1@pc1    postgres
```

ASP.NET Core IdentiyのWebアプリをVSから実行（アカウント: winuser1）、接続確認した接続文字列。

```json
"ConnectionStrings": {
  "DefaultConnection": "Host=localhost;Port=5432;Database=WebDB;Integrated Security=True;Username=postgres"
},
```

winuser1というロールをPgSQLに作成しておくと、接続文字列の`Username=winuser1`を省略できる。

```sql
CREATE ROLE "winuser1" WITH
  LOGIN
  SUPERUSER
  CREATEDB
  CREATEROLE
  INHERIT
  REPLICATION
  CONNECTION LIMIT -1;
```

```sql
CREATE ROLE "winuser1" WITH
  LOGIN
  SUPERUSER
  CONNECTION LIMIT -1;
```

【トラブル】外部からの接続がエラーになる。そもそもtelnetで応答が無いのでSSPIとも関係ない気もする。v15をアンインスコして、v14をインスコしたら疎通した。最終的に原因不明。

## 環境②

- postgresql-14.8-4-windows-x64.exe

```plaintext
# MAPNAME   SYSTEM-USERNAME PG-USERNAME
MapForSSPI  winuser1@pc1    winuser1
#PG-USERNAMEのwinuser1をPgSQLに作成
```

```plaintext
# TYPE  DATABASE  USER  ADDRESS METHOD
# "local" is for Unix domain socket connections only
local all all scram-sha-256
# IPv4 local connections:
# USER allでヒットすると下に行かないようだ
host  all winuser1  192.168.0.0/16  sspi map=MapForSSPI
host  all all       192.168.0.0/16  scram-sha-256
# IPv6 local connections:
host  all winuser1  ::1/128   sspi map=MapForSSPI
host  all all       ::1/128   scram-sha-256
```

## トラブル集

### 暗号化なし用のエントリがありません

psqlからの接続時に`暗号化なし用のエントリがありません`エラーで接続できない。

ipv6は無効にしててあるPCであるが、pg_hba.confにipv6のエントリが必須のよう。ipv6のエントリを削除するとこのエラーが出る。SSPIとの関連があるかは不明。

## 参考

- [Integrated Security with Npgsql](https://github.com/npgsql/npgsql/issues/3083)
- [Windows Authentication In Postgres](https://sqlrob.com/2022/02/28/windows-authentication-in-postgres/)
- [Postgres : Using Integrated Security or ‘passwordless’ login on Windows on localhost or AD Domains](https://www.cafe-encounter.net/p2034/postgres-using-integrated-security-on-windows-on-localhost)
