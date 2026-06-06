# レベル3a(発展): コードでパイプラインを書く版
#
# このレベルのメイン題材はノーコードの Lakeflow Designer です(03a_lakeflow_designer.md)。
# このファイルは「コードで書きたい経験者向けの発展」です。Designerが裏側で生成するのと
# 同種のパイプラインを、Spark宣言型パイプライン(SDP・旧Delta Live Tables)のコードで
# 書いたものです。Designerと見比べると、ノーコードとコードの対応が見えてきます。
#
# 重要: これはノートブックでも「取り込むファイル」でもありません。
# 新しいLakeflow Pipelines Editorには、外部ファイルをソースに指定する導線はありません。
# パイプライン内に「変換(transformation)ファイル」を新規作成し、そこにコードを書きます。
# 下のコードは、その新規ファイルに貼り付ける中身です。
#
# 手順:
#   1. 左メニューの「+新規」→「ETLパイプライン」を選ぶ(エディタが開く)
#   2. 上部のヘッダーをクリックしてパイプライン名を付ける
#   3. 名前の下で、出力先のデフォルトカタログ/スキーマを選ぶ(例: workspace / default)
#   4. 「Start with sample code in Python」を選ぶ(既定のフォルダ構成とサンプルが作られる)
#   5. 左のアセットブラウザで「+」→「変換(Transformation)」をクリック
#        言語: Python / ファイル名: trips_pipeline など / データセットタイプ: 選択なしでOK
#   6. 作成されたファイルに、下の import 以降をすべて貼り付ける
#   7. transformations フォルダの既定サンプル2ファイルは、紛らわしければ削除してよい
#   8. 右上の「パイプラインを実行」をクリック
#
# 構文は推奨の pyspark.pipelines を使用しています(旧 import dlt でも動作します)。

from pyspark import pipelines as dp
from pyspark.sql import functions as F


# ブロンズ: 生データをほぼそのまま取り込む
@dp.table
def trips_bronze():
    return spark.read.table("samples.nyctaxi.trips")


# シルバー: データ品質チェック(expectation)で料金・距離が0以下の行を除外し、
# 使いやすい列に整える。同一パイプライン内のテーブルは名前(trips_bronze)で参照できる。
@dp.table
@dp.expect_or_drop("valid_fare", "fare_amount > 0")
@dp.expect_or_drop("valid_distance", "trip_distance > 0")
def trips_silver():
    return (
        spark.read.table("trips_bronze")
        .withColumn("pickup_date", F.to_date("tpep_pickup_datetime"))
        .withColumn("day_of_week", F.date_format("tpep_pickup_datetime", "E"))
        .select(
            "pickup_date",
            "day_of_week",
            "trip_distance",
            "fare_amount",
            "pickup_zip",
            "dropoff_zip",
        )
    )


# ゴールド: 曜日ごとの乗車件数・平均距離・平均料金
@dp.table
def trips_gold_by_dow():
    return (
        spark.read.table("trips_silver")
        .groupBy("day_of_week")
        .agg(
            F.count("*").alias("trips"),
            F.round(F.avg("trip_distance"), 2).alias("avg_distance"),
            F.round(F.avg("fare_amount"), 2).alias("avg_fare"),
        )
    )
