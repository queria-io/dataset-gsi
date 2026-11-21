{{ config(materialized='table') }}

-- 日本の主な山岳の山頂の位置と標高（ポイント）
SELECT
    mountain_id,
    index_number,
    mountain_index,
    mountain_name,
    peak_name,
    mountain_name_kana,
    peak_name_kana,
    elevation_m,
    point_type,
    prefectures,
    prefecture_names,
    latitude,
    longitude,
    ST_Point(longitude, latitude) AS geometry
FROM {{ ref('stg_mountain') }}
