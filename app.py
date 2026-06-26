import streamlit as st
import pandas as pd
import requests
from geopy.geocoders import Nominatim

# --- CONFIGURATION ---
st.set_page_config(page_title="Smart Meal Planner", page_icon="🍲")

# --- FUNCTIONS ---
def get_stores_by_zip(zip_code):
    """Finds grocery stores using Overpass API directly via requests."""
    geolocator = Nominatim(user_agent="smart_meal_planner_app_2026")
    location = geolocator.geocode(f"{zip_code}, USA")
    
    if not location:
        return None

    # Overpass API endpoint
    url = "https://overpass-api.de/api/interpreter"
    
    # Query: Supermarkets in a 25 mile (40km) radius
    query = f"""
    [out:json];
    node["shop"="supermarket"](around:40000, {location.latitude}, {location.longitude});
    out;
    """
    
    try:
        response = requests.post(url, data=query, timeout=10)
        data = response.json()
        
        # Extract names
        stores = [element['tags']['name'] for element in data['elements'] if 'name' in element['tags']]
        return list(set(stores))[:10]
    except Exception as e:
        st.error(f"Error fetching stores: {e}")
        return []

# --- APP FLOW ---
# (Keep the rest of your app.py session state and UI code exactly as it was)
