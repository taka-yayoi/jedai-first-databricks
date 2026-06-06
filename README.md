# はじめてのDatabricks もくもく会 サンプルノートブック

JEDAI(Japan Enduser Group | Databricks Innovation)もくもく会「はじめてのDatabricks」で使うサンプルノートブック一式です。すべて Databricks Free Edition で動くように作られています(一部の経験者向け機能を除く。後述)。

## 進め方

各レベルとも、運営が冒頭に実例デモを行ったあと、このリポジトリのノートブックを各自インポートして追体験する流れです。詰まったところはいつでも質問してください。

自分のレベルに合わせて、対応するフォルダを開いてください。

- `level1/` 完全初心者向け。Databricksを初めて触る方
- `level2/` 少し触ったことがある方。AI支援(Genie / Genie Code)での分析体験
- `level3/` 経験者向け。最近の新機能キャッチアップ

未経験の方は level1 を完走できれば大成功です。経験のある方は level2 や level3 から、興味のあるテーマを選んでください。

## ノートブックのインポート手順

1. Databricksワークスペースの左メニューから「ワークスペース」を開く
2. 自分のホームフォルダを選び、右上の「インポート」をクリック
3. 「ファイル」を選び、このリポジトリからダウンロードした `.py` ファイルをアップロード
   - GitHubから取り込む場合は、各ファイルの Raw URL を「URL」に貼り付けてもOKです
4. インポートされたノートブックを開き、右上のコンピュートで「Serverless」を選択

Git Reposを使っている方は、このリポジトリをまるごとクローンしても構いません。

なお level3 の 03a 系は扱いが異なります。メインの `03a_lakeflow_designer.md` はノーコードのLakeflow Designerをブラウザ上で操作する手順書です(インポート不要)。発展の `03a_lakeflow_pipeline_code.py` はノートブックではなくパイプライン用のコードで、パイプラインエディタで変換ファイルを新規作成し、中身を貼り付けて使います。詳しい手順はそれぞれのファイル冒頭を参照してください。

## 前提データ

すべてのノートブックは Free Edition に最初から入っている `samples` カタログのデータを使います。CSVのアップロードは不要です。

- `samples.tpch.orders` 受注データ(level1)
- `samples.nyctaxi.trips` ニューヨークのタクシー乗車データ(level2 / level3)

## 各レベルの内容

### level1: はじめてのDatabricks

- `01_first_steps.py` ノートブック作成からSQLクエリ、可視化、テーブル保存まで

### level2: AI支援で分析する

- `02_genie_assistant.py` Genie Code(旧Databricksアシスタント)でのコード生成とPySpark書き換え
- `genie_space_setup.md` Genie Spaceを作って日本語で質問する手順

### level3: 新機能キャッチアップ

- `03a_lakeflow_designer.md` Lakeflow Designerでノーコードにパイプラインを作る(このレベルのメイン)
- `03a_lakeflow_pipeline_code.py` (発展)同じパイプラインをSDPコードで書く版
- `03b_genie_code.py` Genie Codeのエージェント(Agent)モードで自動化を試す
- `03c_lakebase_handson.md` Lakebaseのデータベースプロジェクトを作って触る手順

## Free Editionでの注意点

- Lakebase は公式の制限ページ上は「サポート対象外」と記載されていますが、実機のFree Editionではコンピュート > Lakebase からデータベースプロジェクトを作成できます。クォータの範囲で試せますが、挙動が不安定な場合は運営のデモに切り替えてください。フルに使い込みたい方は無料トライアル環境がおすすめです。
- Genie Code のエージェント(Agent)モードは Free Edition でも利用できます。Agentモードでは「信頼できるコードとデータを使うエージェントを使ってください」という確認が表示されます。当日は安全な `samples` データのみ扱うので問題ありません。
- Free Edition はサーバーレスのみ・1日あたりのクォータ制限があります。R / Scala は使えません。

## 参考記事

- はじめてのDatabricks: https://qiita.com/taka_yayoi/items/8dc72d083edb879a5e5d
- Databricks初心者のための完全学習ガイド: https://qiita.com/taka_yayoi/items/1fe076a0f87a7442d39a
- Databricks Free Edition: https://qiita.com/taka_yayoi/items/33e9cfa7ca9ca9febe72
- Databricks Free Editionで学ぶAI/BI Genie: https://qiita.com/taka_yayoi/items/d2d7b74f0806975a8d63
- Databricks Free Editionで始めるApache Spark: https://qiita.com/taka_yayoi/items/c12a9ab6b6f75f95bc04
