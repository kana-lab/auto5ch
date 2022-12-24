# このリポジトリについて

これは匿名掲示板:`5ch.net`に自動で書き込むプログラムです。**悪用厳禁。保守用に使用して下さい。**
`Selenium`を用いてウェブブラウザから書き込むので、規制を受けにくいかも知れません。UAの偽装にも対応しています。

クラウド上で動かす事を想定して`Dockerfile`を用意していますが、以下ではローカルで動かす方法のみ説明します。

# 使用法

### Dockerを使う場合

まず、dockerをインストールしていない場合は [手順](https://matsuand.github.io/docs.docker.jp.onthefly/engine/install/)
にしたがってインストールします。次に、auto5ch(仮)という名前のdockerイメージを作成します。

```shell
docker build -t auto5ch .
```

次のコマンドでサーバーを起動します。

```shell
docker run -p 8080:8080 -it --rm auto5ch
```

あとはブラウザから http://localhost:8080/ にアクセスし、必要な情報を入力すれば5chに書き込むことができます。

### 自分で環境構築する場合

[Google Chrome](https://www.ubuntuupdates.org/pm/google-chrome-unstable)
と、対応するバージョンの [Chrome Driver](https://chromedriver.chromium.org/downloads)
をインストールしてください。次に、依存するPythonパッケージをインストールします。

```shell
pip install -r requirements.txt
```

次のようにサーバーを起動します。

```shell
python3 app.py
```

あとはブラウザから http://localhost:8080/ にアクセスし、必要な情報を入力すれば5chに書き込むことができます。

# レスの設定について

ブラウザからサーバーにアクセスすると、設定フォームが表示されます。

- `thread`欄にはスレッドのURLの末尾にある数字(恐らくUNIXタイム)を入力します。
- `cycle`欄にはレスを行う間隔を秒で指定します。何も指定しない場合、一度だけレスをします。
- `request`ボタンを押すとレスが`cycle`秒毎に(永遠に)書き込まれます。
- `stop`ボタンを押すと今までの設定がクリアされ、レスが止まります。
