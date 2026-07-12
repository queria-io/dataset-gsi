{{ config(materialized='table') }}

-- 指定緊急避難場所の位置（ポイント）
SELECT
    site_id,
    muni_name,
    site_name,
    address,
    for_flood,
    for_landslide,
    for_storm_surge,
    for_earthquake,
    for_tsunami,
    for_large_fire,
    for_inland_flooding,
    for_volcano,
    same_address_as_shelter,
    latitude,
    longitude,
    ST_Point(longitude, latitude) AS geometry,
    note
FROM {{ ref('stg_emergency_evacuation_site') }}
