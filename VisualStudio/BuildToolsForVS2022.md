# Build Tools for Visual Studio 2022

## 無人インストールで利用する「インストール構成ファイル」

まず、ブートストラップ（vs_BuildTools.exe）を起動し、GUIを利用して任意のコンポーネントを選択しインストールします。インストール後、再び vs_BuildTools.exe を起動し「インストール構成ファイル」を出力しておきます。その他⇒構成のエクスポート⇒エクスポートから`<任意のファイル名>.vsconfig`として出力できます。

.vsconfigは、//コメントアウトに対応しているようなので、ファイルの先頭にどのようなコンポーネントをインストールしたかなどの情報を追加しておくこともできます。

## 無人アンインストール

```dos
vs_BuildTools.exe uninstall --passive --norestart --installPath "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools" 
```

uninstallコマンドには `--installPath　<dir>` の指定が必須です。

--passiveの代わりに--quietを利用するとUIが表示されません（コマンドは即戻るため進捗が不明になります）。

## 無人インストール（オンライン）

事前に出力もしくは作成しておいた「インストール構成ファイル.vsconfig」のコンポーネントをインストールします。

```dos
vs_BuildTools.exe --locale en-us --passive --norestart --config "O:\BT17.6.4LTSC-BS\custom1.vsconfig"
```

`--config <path>`にはフルパスを指定する必要があります。

--passiveの代わりに--quietを利用するとUIが表示されません（またコマンドは即戻るため進捗が不明になります）。

## オフラインインストーラ用レイアウトの作成

ダウンロードとレイアウトの作成のみが行われます。

```dos
vs_BuildTools.exe --layout o:\BT17.6.4LTSC --lang en-US
```

上記の例では約 44 GBでした。

[command]を空白として最初に--layoutを指定する必要があります。

## TIPS

### インストール先

Visual Studio IDE：  
C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools

ダウンロードキャッシュ：  
C:\ProgramData\Microsoft\VisualStudio\Packages ※保持される

共有コンポーネント、ツール、SDK：  
C:\Program Files (x86)\Microsoft Visual Studio\Shared

### 開発者コンソールの場所

```dos
dir "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Visual Studio 2022\Visual Studio Tools\VC" /B

x64 Native Tools Command Prompt for VS 2022 LTSC 17.6.lnk
x64_x86 Cross Tools Command Prompt for VS 2022 LTSC 17.6.lnk
x86 Native Tools Command Prompt for VS 2022 LTSC 17.6.lnk
x86_x64 Cross Tools Command Prompt for VS 2022 LTSC 17.6.lnk
```

VSインスコによって作成される開発者コンソールとの違い。

```dos
x64 Native Tools Command Prompt for VS 2022 LTSC 17.6
⇒
%comspec% /k "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

x64 Native Tools Command Prompt for VS 2022
⇒
%comspec% /k "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
```

## [command]

[command]を未指定で、インストールORレイアウトメンテナンスです。

## --waitオプション

レイアウトコマンド用であり、インストールとuninstallでは利用できません。

## 参考

- [ローカル インストール用の Visual Studio のオフライン インストール パッケージを作成する](https://learn.microsoft.com/ja-jp/visualstudio/install/create-an-offline-installation-of-visual-studio?view=vs-2022)

- [Visual Studio のネットワーク インストールを作成して維持する](https://learn.microsoft.com/ja-jp/visualstudio/install/create-a-network-installation-of-visual-studio?view=vs-2022)

（おそらく）フォルダ共有によって、複数のクライアントからのオフラインインストーラを作成する場合、フォルダを共有するファイルサーバー上で、次のようにブートストラップ.exeを実行する必要があるようです。

```dos
>vs_enterprise.exe --layout c:\VSLayout
※このVSLayoutを\\fileserver\\VSLayoutとして共有
```

- [Visual Studio のワークロードとコンポーネント ID](https://learn.microsoft.com/ja-jp/visualstudio/install/workload-and-component-ids?view=vs-2022)

- [コマンド ライン パラメーターを使用した、Visual Studio のインストール、更新、管理](https://learn.microsoft.com/ja-jp/visualstudio/install/use-command-line-parameters-to-install-visual-studio?view=vs-2022)

- [インストール構成をインポートまたはエクスポートする](https://learn.microsoft.com/ja-jp/visualstudio/install/import-export-installation-configurations?view=vs-2022)
