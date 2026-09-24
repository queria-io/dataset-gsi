{{ config(materialized='table') }}

-- 全国・都道府県・市区町村の面積（時点ごと）
SELECT
    survey_date,
    area_code,
    area_type,
    prefecture_name,
    county_name,
    area_name,
    area_km2,
    is_reference_value,
    note
FROM {{ ref('stg_municipality_area') }}
ORDER BY survey_date, area_code NULLS LAST, prefecture_name, area_name
