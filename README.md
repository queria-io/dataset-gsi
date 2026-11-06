# 国土地理院

国土地理院が公開する、全国の指定緊急避難場所・指定避難所の位置と対応する災害、全国・都道府県・市区町村の面積の推移、自然災害伝承碑の位置と伝承内容を、SQL で検索・集計できるテーブルにしたデータセットです。

## 出典と利用条件

| 原典 | テーブル |
| --- | --- |
| [指定緊急避難場所データ](https://www.gsi.go.jp/bousaichiri/hinanbasho.html)（[全国データ配信](https://hinanmap.gsi.go.jp/)） | `main.emergency_evacuation_site`・`main.designated_shelter` |
| [全国都道府県市区町村別面積調](https://www.gsi.go.jp/KOKUJYOHO/MENCHO-title.htm)（[過去の面積調](https://www.gsi.go.jp/KOKUJYOHO/OLD-MENCHO-title.htm)） | `main.municipality_area` |
| [自然災害伝承碑データ](https://www.gsi.go.jp/bousaichiri/denshouhi_datainfo.html) | `main.disaster_lore_monument` |

- [国土地理院コンテンツ利用規約](https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html)（公共データ利用規約 PDL 1.0）に従います。出典を明記すれば商用利用を含めて利用できます

## テーブル

| テーブル | 内容 |
| --- | --- |
| `main.emergency_evacuation_site` | 指定緊急避難場所。切迫した災害の危険から命を守るために避難する場所で、市区町村が災害種別ごとに指定します |
| `main.designated_shelter` | 指定避難所。災害で住居を失った場合などに一定期間滞在して生活する施設です |
| `main.municipality_area` | 全国・都道府県・郡・市区町村・政令市の区の面積。1 行が 1 地域 × 1 時点 |
| `main.disaster_lore_monument` | 自然災害伝承碑。過去の津波・洪水・火山災害・土砂災害などを伝える石碑やモニュメント |

## 使い方

日野市の洪水に対応する指定緊急避難場所を数える（`site_id` の 2〜6 文字目が市区町村コードです）:

```sql
SELECT count(*) AS sites
FROM gsi.main.emergency_evacuation_site
WHERE substr(site_id, 2, 5) = '13212' AND for_flood;
```

日野市の面積の推移を出す:

```sql
SELECT survey_date, area_km2
FROM gsi.main.municipality_area
WHERE area_code = '13212'
ORDER BY survey_date;
```

津波を伝える伝承碑を申請した市区町村ごとに数える:

```sql
SELECT municipality_code, count(*) AS monuments
FROM gsi.main.disaster_lore_monument
WHERE is_tsunami
GROUP BY ALL
ORDER BY monuments DESC;
```

## 指定緊急避難場所・指定避難所

市区町村が提供したデータを国土地理院が統合した全国版 CSV です。市区町村からの報告に基づいて随時更新されます。位置は経度・緯度のポイント（JGD2011、EPSG:6668 相当）で、緯度・経度が欠損する行は除いています。

`main.emergency_evacuation_site` の列:

- site_id: 共通ID（市区町村コードを含む）
- muni_name: 都道府県名及び市町村名
- site_name: 施設・場所名
- address: 住所
- for_flood / for_landslide / for_storm_surge / for_earthquake / for_tsunami / for_large_fire / for_inland_flooding / for_volcano: 対応災害種別（洪水 / 崖崩れ・土石流・地滑り / 高潮 / 地震 / 津波 / 大規模な火事 / 内水氾濫 / 火山現象）
- same_address_as_shelter: 指定避難所との住所同一
- latitude / longitude: 緯度・経度
- geometry: 避難場所ポイント（EPSG:6668 / JGD2011）
- note: 備考

`main.designated_shelter` の列:

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

## 面積

電子国土基本図の海岸線と市区町村界で囲まれた範囲を測ったもので、河川と湖沼は陸域に含みます。2014 年から 2018 年は年 1 回（10 月 1 日時点）、2019 年 7 月 1 日時点以降は四半期ごとです（2020 年 4 月 1 日時点は中止）。その時点に存在しなかった地域の行はありません。

- survey_date: 時点
- area_code: 標準地域コード（5桁。全国・都道府県の内訳・市区町村外の行は NULL）
- area_type: 地域の種別（全国 / 都道府県 / 都道府県の内訳 / 郡・支庁等 / 市区町村 / 政令市の区 / 市区町村外）
- prefecture_name: 都道府県名
- county_name: 郡・支庁・振興局等
- area_name: 地域名（政令市の区は「札幌市中央区」の形）
- area_km2: 面積（k㎡。公表単位ごとに小数第三位を四捨五入）
- is_reference_value: 参考値（境界未定部を持ち、面積が便宜上の概算であれば TRUE）
- note: 備考（面積から除いている区域や、どの合計に含まれるかの注記）

- 政令市とその区、都道府県とその市部・郡部は別の行として並びます。合計するときは `area_type` で絞ってください
- 「市区町村外」は所属未定の埋立地・島と、市町村の面積に含めない湖沼（然別湖・風蓮湖・八郎潟調整池の一部・本栖湖・児島湖など）です
- 元データに注記の無い時点があり、2026 年 4 月 1 日時点の `note` はすべて NULL です

## 自然災害伝承碑

市区町村からの申請に基づいて地理院地図に掲載された碑です。地理院地図に載っている碑の写真は含みません。

- monument_id: ID（先頭5桁が掲載を申請した市区町村のコード）
- municipality_code: 掲載を申請した市区町村のコード（5桁。碑の所在地の市区町村と違うことがある）
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

- 掲載は市区町村の申請によるため、碑が無い市区町村と申請していない市区町村は区別できません
- `municipality_code` は申請した市区町村のコードで、碑の所在地と違うことがあります（宮古市のコードで所在地が山田町の碑があります）。所在地で数えるときは `address` も確認してください
- 同じ災害でも碑ごとに災害名の表記が違うことがあります。災害で集計するときは `disaster_name` の完全一致に頼らず、`disaster_type` や `is_*` の列を使ってください

## 更新

```bash
uv sync
bash scripts/build.sh
```
