
# Neo4jのセットアップ

- OpenJDK：[Microsoft Build of OpenJDK](https://learn.microsoft.com/ja-jp/java/openjdk/download#openjdk-17)

    OpenJDK 17が前提推奨バージョン。5.14は21もサポート。

- [Neo4jダウンロード](https://neo4j.com/deployment-center/#community)

    COMMUNITY　Neo4j 5.24.2/Windows Executable Neo4j 5.24.2(zip)

## インストール

OpenJDKをインストールする

JAVA_HOMEとPATHの状態を確認

```cmd
>echo %JAVA_HOME%
```

```cmd
>java -version
openjdk version "17.0.12" 2024-07-16 LTS
OpenJDK Runtime Environment Microsoft-9889599 (build 17.0.12+7-LTS)
OpenJDK 64-Bit Server VM Microsoft-9889599 (build 17.0.12+7-LTS, mixed mode, sharing)
```

```text
PATH：`O:\sw\jdk-17.0.12.7-hotspot\bin`
JAVA_HOME：`O:\sw\jdk-17.0.12.7-hotspot\`
```

※インストールパッケージを選択して、次へ、戻る、とするとインストールディレクトリを変更できた。PATHは先頭に挿入された。SET JAVA_HOMEをチェックすると既存のJAVA_HOMEは上書きされたが、複数バージョンのJDKを共存させることもできそう。

※`sysdm.cpl`や`SystemPropertiesAdvanced`で環境変数を確認

Neo4jをインストールする

`O:\sw\neo4j-5.24.2`へzipを展開。

起動

```cmd
O:\sw\neo4j-5.24.2>bin\neo4j.bat console
```

`http://localhost:7474`へブラウザアクセス。

初期アカウント（neo4j/neo4j）でログイン⇒パスワードをリセット。

※ Neo4j.Driverからは`bolt://localhost:7687/`

## Windowsサービス登録

[Windows service](https://neo4j.com/docs/operations-manual/current/installation/windows/#windows-service)

デフォルトでは、Windowsサービスは、システムへのフルアクセス権を持つLocalSystemアカウントとして実行される。セキュリティ上のリスク低減のため、LocalSystemではないアカウントでサービスを実行するのが望ましい。

```cmd
bin\neo4j windows-service install
bin\neo4j start
```

サービス名neo4jとして登録される（services.msc）

UACダイアログから推察するとApache Commons Daemon Service Runnerを利用しているようだ。

新バージョンをインストールする場合、事前に旧バージョンをアンインストールする必要があるとのこと。

```cmd
bin\neo4j windows-service uninstall
```

## 構成の変更について

サービスとして登録した時のJavaオプションなどはneo4j.confに保存される。サービス登録後に構成を変更した場合は、反映のための更新とサービス再起動が必要となる。例えば、neo4j.confやNEO4J_CONF環境変数の`server.memory.heap.initial_size`を変更した場合、変更は自動的に適用されない。サービス更新の操作が必要となる。Javaの関連パスやバージョンを変更したい場合も同様である。

```cmd
bin\neo4j windows-service update
# 再起動
bin\neo4j restart
```

管理者権限コンソールで以下でもOKのようだが、UACダイアグがでるので↑のほうが便利。

```cmd
sc stop neo4j
sc start neo4j
```

## [Windows PowerShell module](https://neo4j.com/docs/operations-manual/current/installation/windows/#powershell)

PowerShellモジュールが配布されている（便利そう）

## アンインストール

[Uninstall Neo4j](https://neo4j.com/docs/operations-manual/current/installation/windows/#_uninstall_neo4j)
