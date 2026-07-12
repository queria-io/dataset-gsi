{# 国土地理院 指定緊急避難場所データ（全国統合 CSV、UTF-8 BOM 付き）
   https://www.gsi.go.jp/bousaichiri/hinanbasho.html #}

{{ config(materialized='table') }}

select *
from read_csv(
    'data/mergeFromCity_2.csv',
    header=true,
    columns={
        'no': 'BIGINT',
        'site_id': 'VARCHAR',
        'muni_name': 'VARCHAR',
        'site_name': 'VARCHAR',
        'address': 'VARCHAR',
        'flood': 'VARCHAR',
        'landslide': 'VARCHAR',
        'storm_surge': 'VARCHAR',
        'earthquake': 'VARCHAR',
        'tsunami': 'VARCHAR',
        'large_fire': 'VARCHAR',
        'inland_flooding': 'VARCHAR',
        'volcano': 'VARCHAR',
        'same_address_as_shelter': 'VARCHAR',
        'latitude': 'VARCHAR',
        'longitude': 'VARCHAR',
        'note': 'VARCHAR'
    }
)
