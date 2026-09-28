# dataset-gsi

国土地理院「指定緊急避難場所データ」（hinanmap.gsi.go.jp）の指定緊急避難場所・指定避難所、「全国都道府県市区町村別面積調」の面積、「自然災害伝承碑データ」の伝承碑を DuckLake カタログ化したデータセット。

## データ出典

国土地理院「指定緊急避難場所データ」サイトが公開する、市区町村提供データを統合した全国版 CSV を使用する。

- 指定緊急避難場所データ: https://www.gsi.go.jp/bousaichiri/hinanbasho.html
- 全国データ配信 (CSV): https://hinanmap.gsi.go.jp/

指定緊急避難場所（災害対策基本法第49条の4）は切迫した災害の危険から命を守るために避難する場所で、洪水・津波等の災害種別ごとに市区町村が指定する。指定避難所（同法第49条の7）は災害により住居を失った場合等に一定期間滞在して生活する施設。位置は経度・緯度のポイント（JGD2011 / EPSG:6668 相当）。

データは市区町村からの報告に基づき随時更新される。

面積は国土地理院「全国都道府県市区町村別面積調」が公開する CSV 3ファイル（平成26年〜平成30年 / 令和元年〜令和5年 / 令和6年4月以降）を使用する。

- 全国都道府県市区町村別面積調: https://www.gsi.go.jp/KOKUJYOHO/MENCHO-title.htm
- 過去の面積調（CSV）: https://www.gsi.go.jp/KOKUJYOHO/OLD-MENCHO-title.htm

電子国土基本図の海岸線と市区町村界で囲まれた範囲を測ったもので、河川と湖沼は陸域に含む。2018年までは年1回（10月1日時点）、2019年7月1日時点以降は四半期ごとに測っている（2020年4月1日時点は中止）。

自然災害伝承碑は国土地理院が配布する全国1ファイルの CSV（ZIP、版ごとにファイル名が変わる）を使用する。市区町村からの申請に基づいて地理院地図に掲載された、過去の自然災害を伝える石碑・モニュメントの位置と伝承内容。地理院地図に載っている碑の写真は配布データに含まれない。

- 自然災害伝承碑データの提供について: https://www.gsi.go.jp/bousaichiri/denshouhi_datainfo.html

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

## テーブル: municipality_area

全国・都道府県・郡・市区町村・政令市の区の面積。1行 = 1地域 × 1時点で、2014年10月1日時点から32時点を持つ。その時点に存在しなかった地域の行は含まない。

- survey_date: 時点
- area_code: 標準地域コード（5桁。全国・都道府県の内訳・市区町村外の行は NULL）
- area_type: 地域の種別（全国 / 都道府県 / 都道府県の内訳 / 郡・支庁等 / 市区町村 / 政令市の区 / 市区町村外）
- prefecture_name: 都道府県名
- county_name: 郡・支庁・振興局等
- area_name: 地域名（政令市の区は「札幌市中央区」の形）
- area_km2: 面積（k㎡。公表単位ごとに小数第三位を四捨五入）
- is_reference_value: 参考値（境界未定部を持ち、面積が便宜上の概算であれば TRUE）
- note: 備考（面積から除いている区域や、どの合計に含まれるかの注記）

政令市とその区、都道府県とその市部・郡部は別の行として並ぶので、合計するときは area_type で絞る。「市区町村外」は所属未定の埋立地・島と、市町村の面積に含めない湖沼（然別湖・風蓮湖・八郎潟調整池の一部・本栖湖・児島湖など）。

## テーブル: disaster_lore_monument

全国の自然災害伝承碑（ポイント）。緯度・経度が欠損する行は除外している。

- monument_id: ID（先頭5桁が市区町村コード）
- municipality_code: 市区町村コード（5桁）
- monument_name: 碑名
- erected_year_label: 建立年（原文。「不明」「1940頃」なども含む）
- erected_year: 建立年（原文が西暦4桁のときだけ。それ以外は NULL）
- address: 所在地
- disaster_name: 災害名（同じ災害でも碑ごとに表記が違うことがある）
- disaster_type: 災害種別（洪水・土砂災害・高潮・地震・津波・火山災害・その他 を「・」でつないだ文字列）
- is_flood / is_landslide / is_storm_surge / is_earthquake / is_tsunami / is_volcano / is_other: 災害種別に洪水 / 土砂災害 / 高潮 / 地震 / 津波 / 火山災害 / その他 を含む
- lore: 伝承内容
- latitude / longitude: 緯度・経度
- geometry: 伝承碑ポイント
- published_date: 公開日
- last_revised_date: 最終修正公開日（修正していない碑は NULL）
- restriction: 制限事項（写真の二次利用の申請先や、建立場所への立ち入りの許可）

掲載は市区町村の申請によるので、碑が無い市区町村と申請していない市区町村は区別できない。

## ビルド

```bash
uv sync
bash scripts/build.sh
```

パイプラインは避難場所の全国統合 CSV（UTF-8 BOM 付き）と面積調の CSV（Shift_JIS、時点が横に並ぶ）を `data/` にダウンロードし（既存ファイルはスキップ）、dbt で raw → stg → mart の3層を構築する。面積調は取得時に縦持ちの `data/municipality_area.csv` にまとめる。自然災害伝承碑はダウンロードページから最新版の ZIP を探し、中の CSV を `data/disaster_lore.csv` に置く。
