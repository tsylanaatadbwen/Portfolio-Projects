-- Create Dimension Table: Location
CREATE TABLE IF NOT EXISTS `karachi_real_estate.dim_location` (
    location_id INT64,
    neighborhood STRING,
    city STRING
);

-- Create Fact Table: Property Listings
CREATE TABLE IF NOT EXISTS `karachi_real_estate.fact_listings` (
    listing_id INT64,
    location_id INT64,
    bedrooms INT64,
    area_sqft FLOAT64,
    price_pkr FLOAT64,
    listing_date DATE
);