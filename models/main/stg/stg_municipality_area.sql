WITH src AS (
    SELECT
        survey_date,
        coalesce(prefecture, '') AS prefecture,
        coalesce(county, '') AS county,
        coalesce(municipality, '') AS municipality,
        area_km2,
        coalesce(remark, '') AS remark,
        area_code = '全国面積' AS is_national,
        -- 令和6年以降のファイルは先頭のゼロが落ちている（1000 = 北海道）
        CASE WHEN regexp_full_match(area_code, '\d+') THEN lpad(area_code, 5, '0') END AS code
    FROM {{ ref('raw_municipality_area') }}
    -- 「-」はその時点に存在しなかった地域
    WHERE area_km2 <> '-'
)

SELECT
    survey_date,
    code AS area_code,
    CASE
        WHEN is_national THEN '全国'
        WHEN code IS NULL AND municipality = '' THEN '都道府県の内訳'
        WHEN code IS NULL THEN '市区町村外'
        WHEN code LIKE '__000' THEN '都道府県'
        WHEN municipality = '' THEN '郡・支庁等'
        WHEN municipality LIKE '(%' THEN '政令市の区'
        ELSE '市区町村'
    END AS area_type,
    CASE
        WHEN is_national THEN NULL
        -- 北海道(市部) → 北海道
        ELSE regexp_replace(prefecture, '\(.*\)$', '')
    END AS prefecture_name,
    NULLIF(county, '') AS county_name,
    CASE
        WHEN is_national THEN '全国'
        WHEN code IS NULL AND municipality = '' THEN prefecture
        WHEN code LIKE '__000' THEN prefecture
        WHEN municipality = '' THEN county
        -- (札幌市)中央区 → 札幌市中央区
        ELSE regexp_replace(municipality, '^\((.+)\)', '\1')
    END AS area_name,
    CAST(area_km2 AS DOUBLE) AS area_km2,
    starts_with(remark, '（参考値）') AS is_reference_value,
    NULLIF(trim(regexp_replace(remark, '^（参考値）', '')), '') AS note
FROM src
