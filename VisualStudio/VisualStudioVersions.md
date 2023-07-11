# Visual StudioとBuild Tools for Visual Studio

## Versions

| Ver.          | Full Ver. | Build Ver.      | リリース日  |
|---------------|-----------|-----------------|------------|
| 2017          | 15.8.9    |-                |-           |
| 2019          | 16.11.27  | 16.11.33801.447 | 2023/6/13  |
| 2022LTSC17.6  | 17.6.4    | 17.6.33815.320  | 2023/6/20  |

- [Visual Studio 2017 リリース履歴](https://learn.microsoft.com/ja-jp/visualstudio/releasenotes/vs2017-relnotes-history)

- [Visual Studio 2019 リリース](https://learn.microsoft.com/ja-jp/visualstudio/releases/2019/history)

- [Visual Studio 2022 リリース履歴](https://learn.microsoft.com/ja-jp/visualstudio/releases/2022/release-history)

## ブートストラップ

ダウンロードできるのはブートストラップファイル（.exe）のため、これを利用してオフラインインストールすることはできません。オフラインインストールに対応するためには、ブートストラップを実行して、事前にダウンロード（レイアウト）を作成しておく必要があります。

「オフラインインストーラの作成」と「無人インストール」は別の操作で行います。作成したオフラインインストーラを利用して、無人インストールすると理解しておくと良いと思います。もちろんネットワーク経由での無人インストールも可能です。

ブートストラップファイルのプロパティの詳細から、このブートストラップを利用してインストールされるバージョンを確認できます。 [製品バージョン] フィールドに、ブートストラップでインストールされるチャネルとバージョンが記載されています。

## メモ

CI等、オフィシャルビルドには「Build Tools for Visual Studio」のみを利用すれば良いと思います。また英語のみのインストールでも構わないと思われます。
