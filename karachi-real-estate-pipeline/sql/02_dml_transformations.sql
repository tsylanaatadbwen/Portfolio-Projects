-- Clean & Transform Listings Data into Fact Table
INSERT INTO `karachi_real_estate.fact_listings` (listing_id, location_id, bedrooms, area_sqft, price_pkr, listing_date)
SELECT 
    raw.id AS listing_id,
    loc.location_id,
    raw.bedrooms,
    raw.area_sqft,
    raw.price AS price_pkr,
    CURRENT_DATE() AS listing_date
FROM `karachi_real_estate.raw_scrape` raw
JOIN `karachi_real_estate.dim_location` loc 
  ON raw.neighborhood = loc.neighborhood
WHERE raw.area_sqft > 0 
  AND raw.price > 0;