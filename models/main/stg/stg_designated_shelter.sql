SELECT
    site_id,
    muni_name,
    site_name,
    address,
    COALESCE(same_address_as_evacuation_site = '1', FALSE) AS same_address_as_evacuation_site,
    additional_matters,
    accepted_evacuees,
    TRY_CAST(latitude AS DOUBLE) AS latitude,
    TRY_CAST(longitude AS DOUBLE) AS longitude,
    note
FROM {{ ref('raw_designated_shelter') }}
WHERE TRY_CAST(latitude AS DOUBLE) IS NOT NULL
  AND TRY_CAST(longitude AS DOUBLE) IS NOT NULL
