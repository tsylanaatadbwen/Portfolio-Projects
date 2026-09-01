import os
import re
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from curl_cffi import requests

# Output folder setup
DATA_DIR = "./data"
os.makedirs(DATA_DIR, exist_ok=True)


def parse_price(price_str: str) -> int:
    """Converts PakWheels price strings ('PKR 69.50 Lac' or 'PKR 1.2 Crore') into integers."""
    if not price_str or "call" in price_str.lower():
        return None

    clean_str = price_str.replace(",", "").strip()

    # Match Crore (10,000,000)
    crore_match = re.search(r"([\d\.]+)\s*Crore", clean_str, re.IGNORECASE)
    if crore_match:
        return int(float(crore_match.group(1)) * 10_000_000)

    # Match Lac (100,000)
    lac_match = re.search(r"([\d\.]+)\s*Lac", clean_str, re.IGNORECASE)
    if lac_match:
        return int(float(lac_match.group(1)) * 100_000)

    # Match direct PKR numbers
    num_match = re.search(r"PKR\s*(\d+)", clean_str, re.IGNORECASE)
    if num_match:
        return int(num_match.group(1))

    return None


def parse_mileage(mileage_str: str) -> int:
    """Strips 'km' and commas, returning integer mileage."""
    if not mileage_str:
        return None
    clean = re.sub(r"[^\d]", "", mileage_str)
    return int(clean) if clean else None


def scrape_pakwheels_page(page_num: int) -> list:
    """Scrapes a single page of PakWheels used cars search results using curl_cffi."""
    url = f"https://www.pakwheels.com/used-cars/search/-/?page={page_num}"

    # Impersonate modern Chrome TLS fingerprint
    response = requests.get(url, impersonate="chrome120", timeout=15)

    if response.status_code != 200:
        print(
            f"[!] Failed page {page_num} with status code {response.status_code}"
        )
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    listings = []

    # Target card elements
    cards = soup.find_all("li", class_="classified-listing")

    for card in cards:
        try:
            # Title & Link
            title_tag = card.find("a", class_="car-name")
            if not title_tag:
                continue

            title = title_tag.get("title", "").strip()
            href = title_tag.get("href", "")
            listing_id = href.split("-")[-1] if href else None

            # Extract Brand (Make)
            make = title.split()[0] if title else "Unknown"

            # Price
            price_tag = card.find(
                "div", class_=re.compile(r"price-details|price-box")
            )
            raw_price = price_tag.text.strip() if price_tag else ""
            asking_price = parse_price(raw_price)

            # Location
            location_tag = card.find("ul", class_="search-vehicle-info")
            location = "Unknown"
            if location_tag:
                loc_li = location_tag.find("li")
                if loc_li:
                    location = loc_li.text.strip()

            # Specs sub-list (Year | Mileage | Fuel | Transmission)
            specs_tag = card.find("ul", class_="search-vehicle-info-2")
            model_year, mileage, fuel_type, transmission = (
                None,
                None,
                "Petrol",
                "Automatic",
            )

            if specs_tag:
                specs = [li.text.strip() for li in specs_tag.find_all("li")]
                for item in specs:
                    if re.match(r"^(19|20)\d{2}$", item):
                        model_year = int(item)
                    elif "km" in item.lower():
                        mileage = parse_mileage(item)
                    elif item in ["Petrol", "Diesel", "Hybrid", "Electric", "CNG", "PHEV"]:
                        fuel_type = item
                    elif item in ["Automatic", "Manual"]:
                        transmission = item

            listings.append({
                "listing_id": listing_id,
                "scrape_date": datetime.now().strftime("%Y-%m-%d"),
                "title": title,
                "make": make,
                "model_year": model_year,
                "asking_price_pkr": asking_price,
                "mileage_km": mileage,
                "fuel_type": fuel_type,
                "transmission": transmission,
                "city": location,
            })
        except Exception as e:
            continue

    return listings


def run_pipeline(pages_to_scrape: int = 5):
    all_data = []
    print(f"[*] Starting extraction across {pages_to_scrape} pages...")

    for page in range(1, pages_to_scrape + 1):
        print(f"    Fetching page {page}...")
        results = scrape_pakwheels_page(page)
        all_data.extend(results)

    df = pd.DataFrame(all_data)

    # Pipeline Transformations (Creating categorical tiers for Power BI visuals)
    # Updated bins with clean executive labels
    df["price_tier"] = pd.cut(
    df["asking_price_pkr"],
    bins=[0, 2_000_000, 5_000_000, 10_000_000, float("inf")],
    labels=["Under 2M PKR", "2M - 5M PKR", "5M - 10M PKR", "Over 10M PKR"],
    )

    df["age_bracket"] = pd.cut(
    df["model_year"],
    bins=[0, 2009, 2015, 2020, 2026],
    labels=["Pre-2010", "2010 to 2015", "2016 to 2020", "2021 to 2026"],
    )

    # Save as timestamped CSV into target folder
    today_str = datetime.now().strftime("%Y_%m_%d")
    output_filename = os.path.join(
        DATA_DIR, f"pakwheels_listings_{today_str}.csv"
    )
    df.to_csv(output_filename, index=False)
    print(f"[✓] Pipeline complete! Saved {len(df)} rows to {output_filename}")


if __name__ == "__main__":
    run_pipeline(pages_to_scrape=20)