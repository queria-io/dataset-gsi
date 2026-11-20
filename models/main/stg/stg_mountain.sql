SELECT
    serial_number::INTEGER AS mountain_id,
    index_number,
    split_part(index_number, '-', 1)::INTEGER AS mountain_index,
    -- 「山名＜山頂名＞」の「＜山頂名＞」は付かない行もある
    trim(regexp_replace(mountain_label, '＜.*＞$', '')) AS mountain_name,
    nullif(regexp_extract(mountain_label, '＜(.*)＞$', 1), '') AS peak_name,
    trim(regexp_replace(mountain_label_kana, '＜.*＞$', '')) AS mountain_name_kana,
    nullif(regexp_extract(mountain_label_kana, '＜(.*)＞$', 1), '') AS peak_name_kana,
    elevation_m::INTEGER AS elevation_m,
    point_type,
    prefectures,
    string_split(prefectures, ' ') AS prefecture_names,
    latitude::DOUBLE AS latitude,
    longitude::DOUBLE AS longitude
FROM {{ ref('raw_mountain') }}
