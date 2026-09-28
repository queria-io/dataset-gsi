SELECT
    monument_id,
    LEFT(monument_id, 5) AS municipality_code,
    monument_name,
    erected_year AS erected_year_label,
    CASE WHEN regexp_matches(erected_year, '^[0-9]{4}$') THEN erected_year::INTEGER END AS erected_year,
    address,
    disaster_name,
    disaster_type,
    list_contains(string_split(disaster_type, '・'), '洪水') AS is_flood,
    list_contains(string_split(disaster_type, '・'), '土砂災害') AS is_landslide,
    list_contains(string_split(disaster_type, '・'), '高潮') AS is_storm_surge,
    list_contains(string_split(disaster_type, '・'), '地震') AS is_earthquake,
    list_contains(string_split(disaster_type, '・'), '津波') AS is_tsunami,
    list_contains(string_split(disaster_type, '・'), '火山災害') AS is_volcano,
    list_contains(string_split(disaster_type, '・'), 'その他') AS is_other,
    lore,
    TRY_CAST(latitude AS DOUBLE) AS latitude,
    TRY_CAST(longitude AS DOUBLE) AS longitude,
    strptime(published_date, '%Y/%-m/%-d')::DATE AS published_date,
    -- 修正等公開日は「2019/9/1、2019/12/5」のように修正のたびに日付が足されていくので、最後の日付を取る
    list_max(list_transform(
        regexp_extract_all(revised_dates, '[0-9]{4}/[0-9]{1,2}/[0-9]{1,2}'),
        d -> strptime(d, '%Y/%-m/%-d')::DATE
    )) AS last_revised_date,
    restriction
FROM {{ ref('raw_disaster_lore_monument') }}
WHERE TRY_CAST(latitude AS DOUBLE) IS NOT NULL
  AND TRY_CAST(longitude AS DOUBLE) IS NOT NULL
