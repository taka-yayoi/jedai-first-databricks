# Databricks notebook source
# MAGIC %md
# MAGIC # レベル2: AI支援で分析する
# MAGIC
# MAGIC このノートブックのゴールは「Genie Code(旧Databricksアシスタント)やGenieを使って、コードを全部自分で書かずに分析を進められた」という体験です。
# MAGIC
# MAGIC 使うデータは `samples.nyctaxi.trips`(ニューヨークのタクシー乗車データ)です。乗車時刻・距離・料金などがあり、自然言語での質問が作りやすいデータです。
# MAGIC
# MAGIC 参考記事: [Databricks Free Editionで学ぶAI/BI Genie](https://qiita.com/taka_yayoi/items/d2d7b74f0806975a8d63)
# MAGIC
# MAGIC メモ: 2026年3月にDatabricksアシスタントはGenie Codeに置き換わりました。画面右上のアイコンから開けます。Free EditionでもAgentモードが使えます。

# COMMAND ----------

# MAGIC %md
# MAGIC ## ステップ1: まずデータを眺める
# MAGIC
# MAGIC どんなデータかを把握します。

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM samples.nyctaxi.trips LIMIT 100

# COMMAND ----------

# MAGIC %md
# MAGIC ## ステップ2: Genie Codeにコードを書いてもらう
# MAGIC
# MAGIC 次の空のセルにカーソルを置き、`Cmd + I`(Mac)または `Ctrl + I`(Windows)を押すと、その場でGenie Codeを呼び出せます。
# MAGIC
# MAGIC 試しに、日本語でこう入力してみてください。
# MAGIC
# MAGIC > samples.nyctaxi.trips を使って、乗車距離(trip_distance)の帯ごとに平均料金(fare_amount)を計算して
# MAGIC
# MAGIC 生成されたコードを確認し、問題なければ採用して実行します。意図と違えば、追加の指示を出して直してもらいましょう。

# COMMAND ----------

# ここでGenie Codeを呼び出してコードを生成してみてください(Cmd+I / Ctrl+I)


# COMMAND ----------

# MAGIC %md
# MAGIC ## ステップ3: SQLとPySparkを行き来する
# MAGIC
# MAGIC 同じ集計を、まずSQLで書いてみます。曜日ごとの乗車件数と平均料金を出します。

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   date_format(tpep_pickup_datetime, "E") AS day_of_week,
# MAGIC   count(*) AS trips,
# MAGIC   round(avg(fare_amount), 2) AS avg_fare
# MAGIC FROM samples.nyctaxi.trips
# MAGIC GROUP BY day_of_week
# MAGIC ORDER BY trips DESC

# COMMAND ----------

# MAGIC %md
# MAGIC 同じ処理をPySparkで書くと次のようになります。pandas経験者の方は「方言が少し違うだけ」と感じられるはずです。
# MAGIC
# MAGIC 結果テーブルの「+」→「可視化」で、曜日ごとの件数を棒グラフにしてみましょう。

# COMMAND ----------

from pyspark.sql import functions as F

trips = spark.table("samples.nyctaxi.trips")
result = (
    trips.withColumn("day_of_week", F.date_format("tpep_pickup_datetime", "E"))
    .groupBy("day_of_week")
    .agg(
        F.count("*").alias("trips"),
        F.round(F.avg("fare_amount"), 2).alias("avg_fare"),
    )
    .orderBy(F.desc("trips"))
)

display(result)

# COMMAND ----------

# MAGIC %md
# MAGIC ## ステップ4: Genie Codeのエージェント挙動を試す
# MAGIC
# MAGIC Genie Codeのパネルを開き、下部のモードセレクターで「Agent」を選んで、複数ステップの依頼をしてみましょう。
# MAGIC
# MAGIC > 乗車距離が長いほど料金が高くなるか、相関を調べて、散布図で可視化して
# MAGIC
# MAGIC エージェントが探索・コード生成・実行・可視化まで自動で進めてくれます。さらに踏み込んだ自動化はレベル3bで試せます。

# COMMAND ----------

# MAGIC %md
# MAGIC ## まとめと次のステップ
# MAGIC
# MAGIC - Genie Codeで日本語からコードを生成できた
# MAGIC - SQLとPySparkで同じ集計を書き、可視化できた
# MAGIC - エージェントモードで分析を一括実行できた
# MAGIC
# MAGIC 次は:
# MAGIC
# MAGIC - `genie_space_setup.md` の手順でGenie Spaceを作り、SQLを一切書かずに日本語だけでデータに質問してみましょう
# MAGIC - 経験者の方はレベル3で、Lakeflowなどの新機能に進めます
