# レベル3c: Lakebaseを触ってみる

Lakebase は、レイクハウスに統合されたフルマネージドのサーバーレスPostgres(OLTPデータベース)です。分析用のレイクハウスと、アプリやAIエージェント向けのトランザクションDBを、同じプラットフォームで扱えます。使わないときはゼロにスケールするのが特徴です。

公式の制限ページ上は「サポート対象外」と書かれていますが、実機のFree Editionではコンピュート > Lakebase からデータベースプロジェクトを作成できます。クォータの範囲で各自試せます(挙動が不安定な場合は運営のデモに切り替えてください)。

参考: 運営はLakebase Autoscaling + LangGraphでステートフルなAIエージェントを構築した経験があるので、実運用のイメージも当日聞けます。

## 一言で言うと

- レイクハウス(列指向・大規模バッチ)と、アプリ/エージェント用のPostgres(行指向・低レイテンシ)を同じ基盤で扱える
- 使わないときはゼロにスケールするので待機コストがかからない
- ブランチを切ったり、瞬時にリストアしたりできる
- AIエージェントが「会話の記憶」や「タスクの状態」を保存する先として使える

## ハンズオン手順

### 1. データベースプロジェクトを作る

1. 左メニューの「コンピュート」を開き、「Lakebase」タブを選ぶ
2. 「データベースプロジェクトを作成」をクリック
3. プロジェクト名を付けて作成する

作成すると、production ブランチと databricks_postgres というデータベースが自動で用意されます。Lakebase Autoscalingは「プロジェクト → ブランチ → データベース」という構成です。

### 2. SQLエディタでPostgresを触る

Lakebaseプロジェクトの画面にあるSQLエディタから、そのままPostgresを操作できます。普通のPostgres SQLが使えます。

```sql
CREATE TABLE memo (id serial PRIMARY KEY, name text, created_at timestamptz DEFAULT now());
INSERT INTO memo (name) VALUES ('JEDAI'), ('Databricks'), ('Lakebase');
SELECT * FROM memo;
```

ここはSpark SQLではなくPostgresである点に注目してください。同じDatabricksの中に、レイクハウスとは別の本物のPostgresがいる、という感覚をつかむのが狙いです。

### 3. scale-to-zeroを体感する

しばらく操作せずに放置したあと、もう一度クエリを実行してみてください。アイドル中はコンピュートがゼロになっているため、最初の1回だけ起動に数秒かかります。使っていないときにリソースを消費しない仕組みが体感できます。

### 4.(発展)Unity Catalogに登録してレイクハウスと一緒に使う

Step2でLakebaseに作ったテーブルをUnity Catalogに登録すると、Databricks SQLからレイクハウスのDeltaテーブルと同じSQLでクエリできるようになります。「運用データ(Lakebase)」と「分析データ(レイクハウス)」を1つの場所で扱える、というLakebaseの価値が見えるところです。

前提:

- メタストアへの `CREATE CATALOG` 権限
- クエリ用のサーバーレスSQLウェアハウス(Free Editionで1つ使えます)

登録はLakebaseの画面ではなく、Catalog Explorerから行う点に注意してください。

1. アプリスイッチャーで「Lakehouse」に移動する
2. Catalog Explorerでプラスアイコンをクリックし、「カタログを作成」を選ぶ
3. カタログ名を入力する(例: `lakebase_catalog`)
4. カタログタイプで「Lakebase Postgres」を選び、「Autoscaling」を選ぶ
5. プロジェクト・ブランチ・Postgresデータベースを選ぶ
6. 「作成」をクリックする

登録すると、Step2で作った memo テーブルが `lakebase_catalog.public.memo` のようにDatabricks SQLから見えます。作られるカタログは読み取り専用で、データの変更はLakebase側(SQLエディタ)で行います。

```sql
SELECT * FROM lakebase_catalog.public.memo;
```

このカタログは通常のUnity Catalogテーブルと同じように扱えるので、共通キーがあればレイクハウスのDeltaテーブルと同じSQL内でJOINできます。運用データと分析データをAPI連携なしで突き合わせられるのが狙いどころです。

メタデータの反映に1点注意です。Unity Catalogはメタデータをキャッシュするため、Lakebaseで作ったばかりのテーブルがカタログにすぐ現れないことがあります。その場合はスキーマの更新(リフレッシュ)をクリックして再取得してください。

## 運営がデモで見せたいポイント

- スケールトゥーゼロの挙動(アイドル→初回クエリの待ち)
- ブランチを切って隔離した環境で試す流れ
- AIエージェントの記憶ストアとして使うユースケース(LangGraphとの組み合わせ)
- 逆方向の同期テーブル(UC→Lakebase): レイクハウスのテーブルをLakebaseに同期して低レイテンシで参照する流れ(Step4のUC登録はLakebase→UCで向きが逆)

## 注意

- 新規インスタンスは2026年3月以降オートスケーリング版で作成されます。プロビジョニング済みの既存インスタンスも順次オートスケーリングへ移行中です。
- Free Editionのクォータを消費します。重い操作は避け、小さなテーブルで試してください。
- フルに使い込みたい方は無料トライアル環境がおすすめです。