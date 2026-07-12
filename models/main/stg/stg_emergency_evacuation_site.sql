SELECT
    site_id,
    muni_name,
    site_name,
    address,
    COALESCE(flood = '1', FALSE) AS for_flood,
    COALESCE(landslide = '1', FALSE) AS for_landslide,
    COALESCE(storm_surge = '1', FALSE) AS for_storm_surge,
    COALESCE(earthquake = '1', FALSE) AS for_earthquake,
    COALESCE(tsunami = '1', FALSE) AS for_tsunami,
    COALESCE(large_fire = '1', FALSE) AS for_large_fire,
    COALESCE(inland_flooding = '1', FALSE) AS for_inland_flooding,
    COALESCE(volcano = '1', FALSE) AS for_volcano,
    COALESCE(same_address_as_shelter = '1', FALSE) AS same_address_as_shelter,
    TRY_CAST(latitude AS DOUBLE) AS latitude,
    TRY_CAST(longitude AS DOUBLE) AS longitude,
    note
FROM {{ ref('raw_emergency_evacuation_site') }}
WHERE TRY_CAST(latitude AS DOUBLE) IS NOT NULL
  AND TRY_CAST(longitude AS DOUBLE) IS NOT NULL
