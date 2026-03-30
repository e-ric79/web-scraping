import json
import os
import time
import requests
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
import re

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

SCRAPERAPI_URL = "https://api.scraperapi.com"


def extract_content(payload):
    if isinstance(payload, dict):
        # Case 1: payload has "results" as a non-empty list
        if (
            "results" in payload
            and isinstance(payload["results"], list)
            and payload["results"]
        ):
            first = payload["results"][0]
            if isinstance(first, dict) and "content" in first:
                return first["content"] or {}
        # Case 2: payload has "content" directly
        if "content" in payload:
            return payload.get("content", {})
    # Fallback: return payload unchanged
    return payload


def post_query(payload):
    try:
        api_key = st.secrets["SCRAPERAPI_KEY"]
    except Exception:
        api_key = os.getenv("SCRAPERAPI_KEY")

    if not api_key:
        raise ValueError("SCRAPERAPI_KEY not found in .env file")

    amazon_url = f"https://www.amazon.{payload['domain']}/dp/{payload['asin']}"

    response = requests.get(
        SCRAPERAPI_URL,
        params={"api_key": api_key, "url": amazon_url, "autoparse": "true"},
    )

    response.raise_for_status()
    return response.json()


def normalize_product(content):
    category_path = []
    if content.get("category_path"):
        category_path = [cat.strip() for cat in content["category_path"] if cat]

    return {
        "asin": content.get("asin"),
        "url": content.get("url"),
        "brand": content.get("brand"),
        "brand_url": content.get("brand_url"),
        "title": content.get("name"),  # ✅ "name" not "title"
        "price": content.get("pricing"),  # ✅ "pricing" not "price"
        "list_price": content.get("list_price"),
        "shipping_price": content.get("shipping_price"),
        "shipping_time": content.get("shipping_time"),
        "stock": content.get("availability_status"),  # ✅ "availability_status"
        "rating": content.get("average_rating"),  # ✅ "average_rating"
        "total_reviews": content.get("total_reviews"),
        "total_ratings": content.get("total_ratings"),
        "images": content.get("images", []),
        "high_res_images": content.get("highResImages", []),
        "categories": content.get("product_category", []),  # ✅ "product_category"
        "feature_bullets": content.get("feature_bullets", []),
        "full_description": content.get("full_description"),
        "product_overview": content.get(
            "product_information", {}
        ),  # ✅ "product_information"
        "star_breakdown": {
            "5_star": content.get("5_star_percentage"),
            "4_star": content.get("4_star_percentage"),
            "3_star": content.get("3_star_percentage"),
            "2_star": content.get("2_star_percentage"),
            "1_star": content.get("1_star_percentage"),
        },
        "reviews": content.get("reviews", []),
        "sold_by": content.get("sold_by"),
    }


def scrape_product_details(asin, geo_location, domain):
    if not asin:
        raise ValueError("ASIN cannot be empty")
    if not domain:
        raise ValueError("Domain cannot be empty")
    payload = {
        "source": "amazon_product",
        "asin": asin,
        "geo_location": geo_location,
        "domain": domain,
        "parse": True,
    }
    raw = post_query(payload)
    content = extract_content(raw)
    normalized = normalize_product(content)
    if not normalized.get(asin):
        normalized["asin"] = asin

    normalized["amazon_domain"] = domain
    normalized["geo_location"] = geo_location
    return normalized

    ##def clean_product_name(title):
    if "-" in title:
        title = title.split("-")[0]
    if "|" in title:
        title = title.split("|")[0]
    return title.strip()

    ##def extract_search_results(content):
    items = []
    if not isinstance(content, dict):
        return items
    if "results" in content:
        results = content["results"]
        if isinstance(results, dict):
            if "organic" in results:
                items.extend(results["organic"])
            if "paid" in results:
                items.extend(results["paid"])
    elif "products" in content and isinstance(content["products", list]):
        items.extend(content["products"])

    return items


def clean_product_name(title):
    if not title:
        return ""

    # Split on common separators and take first part
    for separator in ["-", "|", ","]:
        if separator in title:
            title = title.split(separator)[0]

    # Remove special characters that break URLs
    title = re.sub(r'["\'/\\()+&]', " ", title)

    # Remove extra whitespace
    title = re.sub(r"\s+", " ", title).strip()

    # Keep only first 5 words — short enough for a clean search
    words = title.split()
    title = " ".join(words[:5])

    return title.strip()


def extract_search_results(content):
    items = []
    if not isinstance(content, dict):
        return items

    results = content.get("results", [])

    # ✅ results is a LIST of products directly
    if isinstance(results, list):
        items.extend(results)

    # also grab explore_more_items if present
    extras = content.get("explore_more_items", [])
    if isinstance(extras, list):
        items.extend(extras)

    return items


def normalize_search_results(item):
    asin = item.get("asin") or item.get("product_asin")
    title = item.get("name") or item.get("title")

    if not (asin and title):
        return None

    return {
        "asin": asin,
        "title": title,
        "category": item.get("category"),
        "price": item.get("price"),
        "rating": item.get("stars"),
        "total_reviews": item.get("total_reviews"),
        "image": item.get("image"),
        "url": item.get("url"),
        "is_best_seller": item.get("is_best_seller"),
        "is_amazon_choice": item.get("is_amazon_choice"),
    }


def search_competitors(query_title, domain, categories, pages=1, geo_location=""):
    st.write("🔎Searching for competitors")
    search_title = clean_product_name(query_title)
    results = []
    seen_asins = set()
    strategies = ["featured", "price_asc", "price_desc", "avg_rating"]

    for sort_by in strategies:
        for page in range(1, max(1, pages) + 1):
            payload = {
                "sources": "amazon_search",
                "query": search_title,
                "parse": True,
                "domain": domain,
                "page": page,
                "sort_by": sort_by,
                "geo_location": geo_location,
            }

            if categories and categories[0]:
                payload["refinements"] = {"categories": categories[0]}

            ##content=extract_content(post_query(payload))
            content = extract_content(post_search_query(payload))
            items = extract_search_results(content)

            for item in items:
                result = normalize_search_results(item)
                if result and result["asin"] not in seen_asins:
                    seen_asins.add(result["asin"])
                    results.append(result)

            time.sleep(0.1)
    st.write(f"✅Found {len(results)} competitors")

    return results


def post_search_query(payload):
    try:
        api_key = st.secrets["SCRAPERAPI_KEY"]  # ✅ Streamlit Cloud
    except Exception:
        api_key = os.getenv("SCRAPERAPI_KEY")

    if not api_key:
        raise ValueError("SCRAPERAPI_KEY not found in .env file")

    # ✅ Build a search URL not a product URL
    query = payload.get("query", "")
    domain = payload.get("domain", "com")
    page = payload.get("page", 1)
    sort_by = payload.get("sort_by", "featured")

    amazon_url = f"https://www.amazon.{domain}/s?k={query}&page={page}&s={sort_by}"

    response = requests.get(
        SCRAPERAPI_URL,
        params={"api_key": api_key, "url": amazon_url, "autoparse": "true"},
    )
    response.raise_for_status()
    return response.json()


def scrape_multiple_products(asins, geo_location, domain):
    st.write("🔎Scraping details")
    products = []

    progress_text = st.empty()
    progress_bar = st.progress(0)
    total = len(asins)

    for idx, a in enumerate(asins, 1):
        try:
            progress_text.write(f"Processing competitor {idx}/{total}: {a}")
            progress_bar.progress(idx / total)

            product = scrape_product_details(a, geo_location, domain)
            products.append(product)
            progress_text.write(f"✅ Found {product.get('title',a)}")
        except Exception as e:
            progress_text.write(f"❌ Failed to scrape {a}")
            continue
        time.sleep(0.1)

    progress_text.empty()
    progress_bar.empty()

    st.write(f"✅ Successfully scraped {len(products)} out of {total} competitors")
    return products
