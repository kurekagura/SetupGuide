# Backend Storeのテーブル作成

[シナリオ４](https://mlflow.org/docs/latest/tracking.html#scenario-4-mlflow-with-remote-tracking-server-backend-and-artifact-stores)を参考。

## PostgreSQLの場合

事前にDBを作成しておきます。

```console
pip install psycopg2
```

```console
mlflow server --backend-store-uri postgresql+psycopg2://:@localhost:5432/mlflowdb
#SSPIでテーブル作成できた。user:passwordは空白OK。
```

## MSSQLの場合

事前にDBを作成しておきます。

```console
pip install pyodbc
pip install pymssql
```

### pyodbc

```console
mlflow server --backend-store-uri mssql+pyodbc://:@localhost\INSTA1,11433/mlflowdb?driver=ODBC+Driver+17+for+SQL+Server
#Windows認証でテーブル作成できた。user:passwordは空白OK。
#Port番号は省略できた。
```

### pymssql

```console
mlflow server --backend-store-uri mssql+pymssql://:@localhost:11433/mlflowdb
#Windows認証でテーブル作成できた。user:passwordは空白OK。
#インスタンス名を指定するとエラーになる（localhost\INSTA1）。
#名前付きインスタンスは既定で動的ポートとなるので、当環境ではポートを固定しているからか？
#本来URI表現にはポート番号を含めることは出来ないらしい。
```

## 作成されるテーブル

16テーブルが作成されます。

```sql
SELECT name
FROM sys.tables
WHERE schema_id = SCHEMA_ID('dbo');

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';
```

```console
experiments
runs
tags
metrics
params
alembic_version
experiment_tags
latest_metrics
registered_models
model_versions
registered_model_tags
model_version_tags
registered_model_aliases
datasets
inputs
input_tags
```
