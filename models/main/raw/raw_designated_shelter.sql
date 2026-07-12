{# 国土地理院 指定避難所データ（全国統合 CSV、UTF-8 BOM 付き）
   https://www.gsi.go.jp/bousaichiri/hinanbasho.html #}

{{ config(materialized='table') }}

select *
from read_csv(
    'data/mergeFromCity_1.csv',
    header=true,
    columns={
        'no': 'BIGINT',
        'site_id': 'VARCHAR',
        'muni_name': 'VARCHAR',
        'site_name': 'VARCHAR',
        'address': 'VARCHAR',
        'same_address_as_evacuation_site': 'VARCHAR',
        'additional_matters': 'VARCHAR',
        'accepted_evacuees': 'VARCHAR',
        'latitude': 'VARCHAR',
        'longitude': 'VARCHAR',
        'note': 'VARCHAR'
    }
)
