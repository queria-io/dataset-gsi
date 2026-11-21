{# 国土地理院 日本の主な山岳標高（CSV。取得時に UTF-8 にして data/mountain.csv に置く）
   https://www.gsi.go.jp/kihonjohochousa/kihonjohochousa41139.html #}

{{ config(materialized='table') }}

select *
from read_csv(
    'data/mountain.csv',
    header=true,
    columns={
        'serial_number': 'VARCHAR',
        'index_number': 'VARCHAR',
        'mountain_label': 'VARCHAR',
        'mountain_label_kana': 'VARCHAR',
        'elevation_m': 'VARCHAR',
        'point_type': 'VARCHAR',
        'prefectures': 'VARCHAR',
        'latitude': 'VARCHAR',
        'longitude': 'VARCHAR'
    }
)
