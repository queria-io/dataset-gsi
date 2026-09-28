{{ config(materialized='table') }}

-- 自然災害伝承碑の位置（ポイント）
SELECT
    monument_id,
    municipality_code,
    monument_name,
    erected_year_label,
    erected_year,
    address,
    disaster_name,
    disaster_type,
    is_flood,
    is_landslide,
    is_storm_surge,
    is_earthquake,
    is_tsunami,
    is_volcano,
    is_other,
    lore,
    latitude,
    longitude,
    ST_Point(longitude, latitude) AS geometry,
    published_date,
    last_revised_date,
    restriction
FROM {{ ref('stg_disaster_lore_monument') }}
