{# 国土地理院 自然災害伝承碑データ（全国 CSV、UTF-8 BOM 付き）
   https://www.gsi.go.jp/bousaichiri/denshouhi_datainfo.html #}

{{ config(materialized='table') }}

select *
from read_csv(
    'data/disaster_lore.csv',
    header=true,
    columns={
        'monument_id': 'VARCHAR',
        'monument_name': 'VARCHAR',
        'erected_year': 'VARCHAR',
        'address': 'VARCHAR',
        'disaster_name': 'VARCHAR',
        'disaster_type': 'VARCHAR',
        'lore': 'VARCHAR',
        'latitude': 'VARCHAR',
        'longitude': 'VARCHAR',
        'published_date': 'VARCHAR',
        'revised_dates': 'VARCHAR',
        'restriction': 'VARCHAR'
    }
)
