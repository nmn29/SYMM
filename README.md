# SYMM

Discordのチャンネルに送信された直近の画像をシンメトリー化する

## Installation

- `sample.env` を `.env`にリネームし、ファイル内の`DISCORD_TOKEN`に自分のDiscord Botトークンを記述してください

```.env
DISCORD_TOKEN=typing_your_discord_bot_token
```

- `symm`をインストールします

```shellsession
# ソースから
$ git clone https://github.com/nmn29/SYMM && cd SYMM
$ pip install
```

- 実行

```shellsession
# Botが起動する
$ symm
```

## 使い方

- `/syml`
  - チャンネル内で送信された直近の画像の左側を使用したシンメトリー画像の送信
- `/symr`
  - チャンネル内で送信された直近の画像の右側を使用したシンメトリー画像の送信
- `/sym`
  - `/syml`、`/symr`の両方の実行結果を送信
- `/sym <number>`
- `/syml <number>`
- `/symr <number>`
  - 画像の変化量を`1`-`10`の数値で指定（デフォルトは5）
  - 例: `/sym 10`
- `/help sym`
  - コマンドの一覧と説明を表示

## 協力

- maguro869 様
- nyanmi-1828 様
