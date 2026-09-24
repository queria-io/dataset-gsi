{# 国土地理院 全国都道府県市区町村別面積調（CSV を縦持ちにしたもの。pipelines/area.py が作る）
   https://www.gsi.go.jp/KOKUJYOHO/OLD-MENCHO-title.htm#csv #}

{{ config(materialized='table') }}

select *
from read_csv(
    'data/municipality_area.csv',
    header=true,
    columns={
        'source_file': 'VARCHAR',
        'survey_label': 'VARCHAR',
        'survey_date': 'DATE',
        'area_code': 'VARCHAR',
        'prefecture': 'VARCHAR',
        'county': 'VARCHAR',
        'municipality': 'VARCHAR',
        'area_km2': 'VARCHAR',
        'remark': 'VARCHAR'
    }
)
