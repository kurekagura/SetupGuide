# SSPIの構成

## 環境

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

ASP.NET Core IdentiyのWebアプリをVSから実行（アカウントwinuser1）、接続確認した接続文字列。

```json
"ConnectionStrings": {
  "DefaultConnection": "Host=localhost;Port=5432;Database=WebDB;Integrated Security=True;Username=postgres"
},
```

## 参考

- [Integrated Security with Npgsql](https://github.com/npgsql/npgsql/issues/3083)
