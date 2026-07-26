# dataset-gsi

国土地理院「指定緊急避難場所データ」（hinanmap.gsi.go.jp）の指定緊急避難場所・指定避難所を DuckLake カタログ化したデータセット。

## データ出典

国土地理院「指定緊急避難場所データ」サイトが公開する、市区町村提供データを統合した全国版 CSV を使用する。

- 指定緊急避難場所データ: https://www.gsi.go.jp/bousaichiri/hinanbasho.html
- 全国データ配信 (CSV): https://hinanmap.gsi.go.jp/

指定緊急避難場所（災害対策基本法第49条の4）は切迫した災害の危険から命を守るために避難する場所で、洪水・津波等の災害種別ごとに市区町村が指定する。指定避難所（同法第49条の7）は災害により住居を失った場合等に一定期間滞在して生活する施設。位置は経度・緯度のポイント（JGD2011 / EPSG:6668 相当）。

データは市区町村からの報告に基づき随時更新される。

## ライセンス

国土地理院コンテンツ利用規約（公共データ利用規約 PDL 1.0）に基づき、出典を明記することで商用利用を含め自由に利用できる。

- https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html

## テーブル: emergency_evacuation_site

全国の指定緊急避難場所（ポイント）。緯度・経度が欠損する行は除外している。

- site_id: 共通ID（市区町村コードを含む）
- muni_name: 都道府県名及び市町村名
- site_name: 施設・場所名
- address: 住所
- for_flood / for_landslide / for_storm_surge / for_earthquake / for_tsunami / for_large_fire / for_inland_flooding / for_volcano: 対応災害種別（洪水 / 崖崩れ・土石流・地滑り / 高潮 / 地震 / 津波 / 大規模な火事 / 内水氾濫 / 火山現象）
- same_address_as_shelter: 指定避難所との住所同一
- latitude / longitude: 緯度・経度
- geometry: 避難場所ポイント（EPSG:6668 / JGD2011）
- note: 備考

## テーブル: designated_shelter

全国の指定避難所（ポイント）。緯度・経度が欠損する行は除外している。

- site_id: 共通ID（市区町村コードを含む）
- muni_name: 都道府県名及び市町村名
- site_name: 施設・場所名
- address: 住所
- same_address_as_evacuation_site: 指定緊急避難場所との住所同一
- additional_matters: その他市町村長が必要と認める事項
- accepted_evacuees: 受入対象者
- latitude / longitude: 緯度・経度
- geometry: 避難所ポイント（EPSG:6668 / JGD2011）
- note: 備考

## ビルド

```bash
uv sync
bash scripts/build.sh
```

パイプラインは全国統合 CSV（UTF-8 BOM 付き）を `data/` にダウンロードし（既存ファイルはスキップ）、dbt で raw → stg → mart の3層を構築する。
