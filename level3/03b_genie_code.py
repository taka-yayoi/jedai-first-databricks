# Databricks notebook source
# MAGIC %md
# MAGIC # レベル3b: Genie Codeで自動化を試す
# MAGIC
# MAGIC Genie Codeは、コードを書く相棒というより、複数ステップのデータ作業を自分で計画・実行する「エージェント」です。パイプライン構築、デバッグ、ダッシュボード作成などをまとめて任せられます。
# MAGIC
# MAGIC Free EditionでもAgentモードが使えます。画面右上のGenie Codeパネルを開き、入力欄の下にある「Agent」を選んでください。
# MAGIC
# MAGIC 一点だけ: Agentモードでは「信頼できるコードとデータを使うエージェントを使ってください」という確認が表示されます。今日触るのは `samples` の安全なデータだけなので問題ありません。自分のデータや外部のコードを扱うときは、エージェントが実行する内容を確認してから進める習慣をつけましょう。

# COMMAND ----------

# MAGIC %md
# MAGIC ## 試し方
# MAGIC
# MAGIC 1. 画面右上のGenie Codeアイコンを開く
# MAGIC 2. パネル下部のモードセレクターで「Agent」を選ぶ
# MAGIC 3. 日本語で依頼を入力する
# MAGIC
# MAGIC Genie Codeは、いま開いている画面(ノートブック、SQLエディタ、Lakeflowパイプラインエディタ)に応じてできることを切り替えます。ノートブックなら探索的分析、パイプラインエディタならパイプライン編集に強くなります。

# COMMAND ----------

# MAGIC %md
# MAGIC ## 依頼の例(複数ステップを任せる)
# MAGIC
# MAGIC Agentモードの本領は、一度の依頼で複数の工程をまとめて進められることです。少し欲張った依頼を投げてみましょう。
# MAGIC
# MAGIC ノートブックでの分析依頼:
# MAGIC
# MAGIC > samples.nyctaxi.trips を使って、時間帯ごとの平均料金を計算し、もっとも高い時間帯と低い時間帯を特定して、その差が統計的に意味のある差かどうかも確認したうえで、結果を可視化して
# MAGIC
# MAGIC データエンジニアリングの依頼(Lakeflowパイプラインエディタで):
# MAGIC
# MAGIC > samples.nyctaxi.trips から、料金と距離が0より大きい行だけを残すシルバーテーブルと、曜日ごとに集計するゴールドテーブルを持つ宣言型パイプラインを作って、データ品質チェックも入れて
# MAGIC
# MAGIC ダッシュボードの依頼:
# MAGIC
# MAGIC > 曜日ごとの乗車件数と平均料金、時間帯ごとの傾向を示すダッシュボードを作って

# COMMAND ----------

# MAGIC %md
# MAGIC ## 観察ポイント
# MAGIC
# MAGIC - Genie Codeが「計画 → コード生成 → 実行 → 検証」をどう進めるか
# MAGIC - 途中で人間が確認・修正できる箇所(humanがコントロールを握る設計)
# MAGIC - レベル2で自分が手で書いたPySparkと、Genie Codeの生成コードの違い
# MAGIC - レベル3aで手作業で組んだパイプラインを、Agentがどこまで自動で再現できるか
# MAGIC
# MAGIC 生成されたコードは必ず中身を確認してから採用してください。エージェントはスクリプトを大きく書き換えることがあるので、Git連携などのバージョン管理と相性がよいです。
