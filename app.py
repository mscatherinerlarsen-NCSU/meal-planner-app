import streamlit as st
import pandas as pd
import random
from geopy.geocoders import Nominatim
import overpy

# --- CONFIGURATION ---
st.set_page_config(page_title="Smart Meal Planner", page_icon="🍲")

# --- DATA ---
DIETS = ["Keto", "Vegan", "Vegetarian", "Gluten-Free", "Paleo", "Cost-Friendly", "Low-Carb"]
ALLERGIES = ["None", "Peanuts", "Dairy", "Eggs", "Wheat", "Tree Nuts", "Soy", "Fish", "Shellfish", "Seafood"]

# --- FUNCTIONS ---
def get_stores_by_zip(zip_code):
    """Finds grocery stores within 25 miles of a zip code using OpenStreetMap."""
    geolocator = Nominatim(user_agent="meal_planner_app")
    location = geolocator.geocode(f"{zip_code}, USA")
    
    if not location:
        return []

    api = overpy.Overpass()
    # Search for supermarkets within approx 40km (~25 miles)
    query = f"""
    node["shop"="supermarket"](around:40000, {location.latitude}, {location.longitude});
    out;
    """
    result = api.query(query)
    stores = [node.tags.get("name", "Unknown Store") for node in result.nodes if "name" in node.tags]
    return list(set(stores))[:10] # Return unique stores, limit to 10

# --- SESSION STATE ---
if 'step' not in st.session_state: st.session_state.step = 1

st.title("🍲 Smart Meal Planner")

# --- STEP 1 ---
if st.session_state.step == 1:
    diets = st.multiselect("Select up to 2 Diets", DIETS, max_selections=2)
    household_size = st.number_input("Household Members", min_value=1, value=2)
    allergies = st.multiselect("Select Allergies", ALLERGIES)
    if "None" in allergies: allergies = ["None"]
    zip_code = st.text_input("Enter Zip Code")

    if st.button("Find Local Stores"):
        with st.spinner("Finding stores near you..."):
            stores = get_stores_by_zip(zip_code)
            if not stores:
                st.error("Could not find stores in this area. Please try a nearby zip.")
            else:
                st.session_state.found_stores = stores
                st.session_state.step = 2
                st.rerun()

# --- STEP 2 ---
elif st.session_state.step == 2:
    selected = st.multiselect("Select exactly 2 stores", st.session_state.found_stores, max_selections=2)
    if st.button("Generate Menu"):
        if len(selected) == 2:
            st.session_state.selected_stores = selected
            st.session_state.step = 3
            st.rerun()
        else:
            st.warning("Please select 2 stores.")

# --- STEP 3 ---
elif st.session_state.step == 3:
    st.write(f"Generating menu for {st.session_state.selected_stores[0]} and {st.session_state.selected_stores[1]}")
    # (Menu logic remains the same)
    if st.button("Start Over"):
        st.session_state.step = 1
        st.rerun()
