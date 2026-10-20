# GuardBot

[Deutsch](../de/README.md) | [English](../en/README.md) | [Français](../fr/README.md) | [Español](../es/README.md) | [Português](../pt/README.md) | [Русский](../ru/README.md) | [Українська](../uk/README.md) | [Svenska](../sv/README.md) | [Dansk](../da/README.md) | [中文](../zh/README.md) | **日本語** | [한국어](../ko/README.md)

モデレーション、セキュリティ、コミュニティのための自己ホスト型 Discord ボット。オープンソースで無料、データは自分のコンピューターに残ります。

<!-- toc -->

- [プロジェクトについて](#プロジェクトについて)
- [機能](#機能)
  - [セキュリティ](#セキュリティ)
  - [モデレーション](#モデレーション)
  - [ログ](#ログ)
  - [コミュニティ](#コミュニティ)
  - [管理](#管理)
- [プロジェクトの状況](#プロジェクトの状況)
- [動作要件](#動作要件)
- [クイックスタート](#クイックスタート)
- [リポジトリの構成](#リポジトリの構成)
- [コマンド](#コマンド)
- [設定](#設定)
- [ロードマップ](#ロードマップ)
- [プライバシーとセキュリティ](#プライバシーとセキュリティ)
- [サポート](#サポート)
- [ライセンス](#ライセンス)

<!-- tocstop -->

## プロジェクトについて

GuardBot は、多くのサーバーがホスト型ボットで有料利用している機能をまとめています。モデレーション、ログ、Anti-Raid（レイド対策）、Anti-Nuke（サーバー破壊対策）、チケット、レベルなどです。自分のコンピューターか小さな VPS で、自分で運用します。

ホスト型ボットは、サーバーのデータやメンバー ID、場合によってはメールアドレスを第三者に保存します。自分でホストすれば、それらのデータはコンピューターの外に出ません。GuardBot は、誰でもサブスクリプションなしで高機能なボットを運用できることを示すためのものです。

## 機能

### セキュリティ

- 自動モデレーション：単語フィルター、大文字フィルター、メンションスパム、招待リンク、フィッシングドメイン、個人情報、ドキシング、脅迫。すべてのリストを編集できます。
- 短時間の大量参加を検知するレイド対策と、全チャンネルのサーバーロックダウン。
- Anti-Nuke：大量削除や大量 BAN の上限、自動対応、サーバーオーナーへのダイレクトメッセージ。
- グラグチャンネル：詐欺リンクや画像を投稿したメンバーは、アカウント保護の手順が書かれた専用チャンネルだけに移されます。モデレーターは /jail と /unjail も使えます。
- ボタンまたはキャプチャによる認証と、期限内に認証しないメンバーの自動削除。
- Anti-Nuke は、権限の付与、新しい Webhook、追加されたボット、サーバー名の変更も監視します。

### モデレーション

- 警告、ミュート、キック、BAN、ジェイルと、メンション・ユーザー ID・種類で絞り込める履歴。
- 自動エスカレーション。たとえば警告 3 回でタイムアウトにできます。
- 各モデレーションコマンドを使えるロールやユーザーを設定できます。

### ログ

- 送信、編集、削除されたメッセージ（画像、GIF、URL を含む）を、別々のログチャンネルに記録します。
- ロール、ニックネーム、BAN、ボイス、チャンネル、サーバーロールの変更。

### コミュニティ

- ようこそ・さようならメッセージ、自動ロール、ブースター特典。
- チケット、投票、プレゼント企画、提案。
- 好きな絵文字で使えるリアクションロールと、メンバーが自分で切り替えられる通知トピック。
- チャットとボイスの XP とレベル 1〜100、レベルロール、誕生日。
- スターボードと一時ボイスチャンネル。
- 期限付きジェイル、複数選択の投票、画像のランクカード、ロールごとの XP ブースト。

### 管理

- すべてのモジュールと各コマンドをサーバーごとにオン・オフできます。
- 独自のプレフィックス、コマンドのエイリアス、コマンド名の変更。
- ロールとチャンネル構成のバックアップと復元。
- ロール、チャンネル、絵文字、Webhook のスケジュール自動バックアップと、足りないものだけを追加する復元コマンド。

## プロジェクトの状況

GuardBot はまだ新しく、大規模なサーバーでは使われていません。自動テスト（`python -m unittest`）は、ストレージ、個人情報の検出、レベル計算、コマンド登録、権限チェック、ドキュメントのリンクを対象としています。ロックダウン、バックアップの復元、認証、Anti-Nuke、グラグなど、実際の Discord サーバーが必要な機能はテストの対象外です。頼りにする前に、まずテスト用サーバーで試してください。ドキュメントの翻訳はネイティブスピーカーによる確認を受けていません。修正の提案を歓迎します。

## 動作要件

- Python 3.11 以降
- ボットトークンを持つ Discord アプリケーション
- 常時オンラインのコンピューターまたは VPS

## クイックスタート

```
git clone <REPOSITORY_URL>
cd guardbot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

詳しい手順は次のガイドにあります： [GUIDE.md](GUIDE.md).

## リポジトリの構成

```
guardbot/
  main.py                 entry point
  requirements.txt
  settings.example.json   global options
  .env.example            token placeholder
  guardbot/
    core.py               bot class, storage, permission checks
    defaults.py           default settings of every module
    utils.py              helpers
    images.py             rank cards and captcha images
    cogs/                 one file per feature group
  docs/                   documentation in 12 languages, COMMANDS.md, PRIVACY.md
  deploy/                 systemd service, Dockerfile, compose file
  scripts/                maintenance scripts
  tests/                  automated tests (python -m unittest)
  data/                   created at runtime, holds your settings and data
```

## コマンド

ほとんどのコマンドはスラッシュコマンドで、モデレーションコマンドはプレフィックスでも使えます。完全な一覧はコマンドリファレンスにあります： [COMMANDS.md](../COMMANDS.md).

## 設定

全体の設定は settings.json で行います。それ以外はサーバーごとに /module、/command、/perms、/alias、/config などのコマンドで設定します。

コマンド名を変えるには、command_names に追加してボットを再起動します。

```json
{
  "prefix": "!",
  "command_names": {
    "warn": "verwarnen"
  }
}
```

## ロードマップ

- 自分のコンピューターで動くローカルウェブダッシュボード。ホスト型サービスなしで設定を変更できます。
- ボットメッセージの翻訳。
- 設定のエクスポートとインポート。

## プライバシーとセキュリティ

- テレメトリーも外部サービスもありません。ボットは Discord とだけ通信します。
- すべてのデータは、お使いのコンピューターの data フォルダーに保存されます。設定、XP、誕生日（日と月のみ）、モデレーション記録です。
- ボットはメンバーからのダイレクトメッセージを無視します。
- トークンは .env ファイルから読み込まれます。共有したり公開したりしないでください。
- メンバーは /mydata で自分のデータをエクスポートおよび削除できます。管理者は、退出したメンバーのデータを保持する期間を設定できます。
- [PRIVACY.md](../PRIVACY.md)

## サポート

バグ、アイデア、提案は Discord の @justyyin に連絡するか、GitHub で issue を作成してください。

## ライセンス

MIT ライセンスで公開されています。参照： [LICENSE](../../LICENSE).

Copyright (c) Justyn - made in Germany
