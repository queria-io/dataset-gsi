{{ config(materialized='table') }}

-- 指定避難所の位置（ポイント）
SELECT
    site_id,
    muni_name,
    site_name,
    address,
    same_address_as_evacuation_site,
    additional_matters,
    accepted_evacuees,
    latitude,
    longitude,
    ST_Point(longitude, latitude) AS geometry,
    note
FROM {{ ref('stg_designated_shelter') }}
