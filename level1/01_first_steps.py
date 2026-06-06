# Databricks notebook source
# MAGIC %md
# MAGIC # レベル1: はじめてのDatabricks
# MAGIC
# MAGIC このノートブックのゴールは「ノートブックでコードを実行し、データをクエリして可視化し、自分のテーブルに保存できた」という最初の成功体験を得ることです。
# MAGIC
# MAGIC 進め方:
# MAGIC
# MAGIC 1. 右上のコンピュートで「Serverless」を選ぶ
# MAGIC 2. 上から順にセルを実行する(セル左上の実行ボタン、または Shift+Enter)
# MAGIC 3. 詰まったら運営に質問するか、Genie Code(画面右上のアシスタント)に聞く
# MAGIC
# MAGIC 参考記事: [はじめてのDatabricks](https://qiita.com/taka_yayoi/items/8dc72d083edb879a5e5d)

# COMMAND ----------

# MAGIC %md
# MAGIC ## ステップ1: 計算資源の確認とHello実行
# MAGIC
# MAGIC Databricksでコードを実行するには計算資源(コンピュート)が必要です。Free Editionでは「Serverless」のみ利用でき、クラスターの起動を待たずに数秒で実行できます。
# MAGIC
# MAGIC 右上のコンピュートセレクターが「Serverless」になっていることを確認したら、次のセルを実行してみましょう。

# COMMAND ----------

print("Hello Databricks!")

# COMMAND ----------

# MAGIC %md
# MAGIC 出力が表示されれば成功です。これでDatabricksでプログラムを実行できるようになりました。
# MAGIC
# MAGIC エラーが出る場合は、ノートブック名の右にある言語が Python になっているか確認してください。

# COMMAND ----------

# MAGIC %md
# MAGIC ## ステップ2: データを見る
# MAGIC
# MAGIC Free Editionには `samples` というカタログに最初からサンプルデータが入っています。ここでは受注データ `samples.tpch.orders` をSQLで見てみます。
# MAGIC
# MAGIC このノートブックの言語はPythonですが、セルの先頭に `%sql` を付けるとそのセルだけSQLとして実行できます。これもDatabricksの便利なところです。

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM samples.tpch.orders LIMIT 1000

# COMMAND ----------

# MAGIC %md
# MAGIC テーブル名を `samples.tpch.orders` と3つの部分で指定していることに注目してください。
# MAGIC
# MAGIC Databricksでは `カタログ.スキーマ.テーブル` の3階層でデータを管理します(これをUnity Catalogの3階層名前空間と呼びます)。データを読み書きするときは、つねに「どのデータを対象にしているか」を意識するのが大切です。

# COMMAND ----------

# MAGIC %md
# MAGIC ## ステップ3: 可視化する
# MAGIC
# MAGIC 上のクエリ結果の表の上にある「+」ボタンをクリックし、「可視化」を選ぶと、コードを書かずにグラフを作れます。
# MAGIC
# MAGIC やってみましょう:
# MAGIC
# MAGIC 1. 上のSQLセルの結果テーブルで「+」→「可視化」をクリック
# MAGIC 2. 棒グラフを選び、X軸に `o_orderpriority`、Y軸に件数を設定
# MAGIC 3. 「保存」をクリック
# MAGIC
# MAGIC Jupyterなどではmatplotlibでコードを書かないとグラフになりませんが、Databricksならワンクリックです。もちろんmatplotlibも使えます。

# COMMAND ----------

# MAGIC %md
# MAGIC ## ステップ4: データを加工する(フィルタリング)
# MAGIC
# MAGIC 必要な列と行だけに絞り込んでみます。ここでは特定の日付かつ金額が大きい受注だけを取り出します。

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   o_orderkey,
# MAGIC   o_custkey,
# MAGIC   o_orderstatus,
# MAGIC   o_totalprice,
# MAGIC   o_orderdate,
# MAGIC   o_orderpriority
# MAGIC FROM
# MAGIC   samples.tpch.orders
# MAGIC WHERE
# MAGIC   o_orderdate = "1998-07-01"
# MAGIC   AND o_totalprice >= 100000

# COMMAND ----------

# MAGIC %md
# MAGIC ## ステップ5: 自分のテーブルに保存する
# MAGIC
# MAGIC 加工した結果を自分用のテーブルとして保存してみます。Free Editionでは `workspace` カタログの `default` スキーマに書き込めます。
# MAGIC
# MAGIC ここでは CTAS(Create Table As Select)という構文で、クエリ結果をそのままテーブルにします。
# MAGIC
# MAGIC 書き込みのときは「どこに書き込むか」をつねに意識してください。なお、Databricksの標準テーブル形式 Delta Lake では更新履歴が自動で記録されるので、間違えてもロールバックできます。安心して試してください。

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.default.orders_199807 AS
# MAGIC SELECT
# MAGIC   o_orderkey,
# MAGIC   o_custkey,
# MAGIC   o_orderstatus,
# MAGIC   o_totalprice,
# MAGIC   o_orderdate,
# MAGIC   o_orderpriority
# MAGIC FROM
# MAGIC   samples.tpch.orders
# MAGIC WHERE
# MAGIC   o_orderdate = "1998-07-01"
# MAGIC   AND o_totalprice >= 100000

# COMMAND ----------

# MAGIC %md
# MAGIC 左メニューの「カタログ」を開き、`workspace` → `default` とたどると、作成した `orders_199807` テーブルが見つかります(表示されない場合は更新ボタンを押してください)。
# MAGIC
# MAGIC これでデータを永続化できました。

# COMMAND ----------

# MAGIC %md
# MAGIC ## おまけ: 同じ処理をPythonで書くと
# MAGIC
# MAGIC SQLだけでなくPythonでも同じことができます。Databricksの処理エンジンであるApache SparkのPython API(PySpark)を使います。
# MAGIC
# MAGIC 次のセルは上のSQLと同じ意味です。SQLとPythonをどう使い分けるかは、ループや条件分岐が必要かどうかで決めるとよいです。

# COMMAND ----------

sdf = spark.table("samples.tpch.orders")
(
    sdf.select(
        "o_orderkey",
        "o_custkey",
        "o_orderstatus",
        "o_totalprice",
        "o_orderdate",
        "o_orderpriority",
    )
    .filter("o_orderdate = '1998-07-01' AND o_totalprice >= 100000")
    .write.mode("overwrite")
    .saveAsTable("workspace.default.orders_199807")
)

display(spark.table("workspace.default.orders_199807"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## まとめと次のステップ
# MAGIC
# MAGIC おつかれさまでした。ここまでで以下ができるようになりました。
# MAGIC
# MAGIC - サーバーレスでノートブックを実行する
# MAGIC - `samples` のデータをSQLでクエリする
# MAGIC - ワンクリックで可視化する
# MAGIC - データを加工して自分のテーブルに保存する
# MAGIC
# MAGIC 次に進みたい方へ:
# MAGIC
# MAGIC - レベル2で、Genie Code(AI支援)を使った分析を体験できます
# MAGIC - 会のあとの学習ロードマップは [Databricks初心者のための完全学習ガイド](https://qiita.com/taka_yayoi/items/1fe076a0f87a7442d39a) が便利です
