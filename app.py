import streamlit as st
import pandas as pd
import random
from geopy.geocoders import Nominatim
from osmpythontools.overpass import Overpass

# --- CONFIGURATION ---
st.set_page_config(page_title="Smart Meal Planner", page_icon="🍲")

# --- DATA ---
DIETS = ["Keto", "Vegan", "Vegetarian", "Gluten-Free", "Paleo", "Cost-Friendly", "Low-Carb"]
ALLERGIES = ["None", "Peanuts", "Dairy", "Eggs", "Wheat", "Tree Nuts", "Soy", "Fish", "Shellfish", "Seafood"]

# --- FUNCTIONS ---
def get_stores_by_zip(zip_code):
    """Finds grocery stores within 25 miles of a zip code using OpenStreetMap."""
    geolocator = Nominatim(user_agent="smart_meal_planner_app_2026")
    location = geolocator.geocode(f"{zip_code}, USA")
    
    if not location:
        return None

    try:
        overpass = Overpass()
        # Querying within 40,000 meters (~25 miles)
        query = f'node["shop"="supermarket"](around:40000, {location.latitude}, {location.longitude});'
        result = overpass.query(query)
        
        stores = [element.tags().get('name') for element in result.nodes() if element.tags().get('name')]
        # Filter for unique names and limit to 10
        return list(set(stores))[:10]
    except Exception as e:
        st.error(f"Error connecting to store database: {e}")
        return []

# --- SESSION STATE ---
if 'step' not in st.session_state: st.session_state.step = 1

st.title("🍲 Smart Meal Planner")

# --- STEP 1: CONSTRAINTS ---
if st.session_state.step == 1:
    diets = st.multiselect("Select up to 2 Diets", DIETS, max_selections=2)
    household_size = st.number_input("Household Members", min_value=1, value=2)
    allergies = st.multiselect("Select Allergies", ALLERGIES)
    
    # Allergy Logic: If 'None' is selected, clear other selections
    if "None" in allergies: allergies = ["None"]
    
    zip_code = st.text_input("Enter Zip Code")

    if st.button("Find Local Stores"):
        if not zip_code:
            st.error("Please enter a zip code.")
        else:
            with st.spinner("Searching for local stores..."):
                stores = get_stores_by_zip(zip_code)
                if stores is None or len(stores) == 0:
                    st.error("No stores found for this zip code. Please try another.")
                else:
                    st.session_state.found_stores = stores
                    st.session_state.step = 2
                    st.rerun()

# --- STEP 2: STORE SELECTION ---
elif st.session_state.step == 2:
    st.subheader("Select exactly 2 stores")
    selected = st.multiselect("Available Stores", st.session_state.found_stores, max_selections=2)
    
    if st.button("Generate Menu"):
        if len(selected) == 2:
            st.session_state.selected_stores = selected
            st.session_state.step = 3
            st.rerun()
        else:
            st.warning("Please select exactly two stores.")
    if st.button("Back"):
        st.session_state.step = 1
        st.rerun()

# --- STEP 3: MENU OUTPUT ---
elif st.session_state.step == 3:
    st.subheader("Your 7-Day Meal Plan")
    st.write(f"Sourcing options from: **{st.session_state.selected_stores[0]}** & **{st.session_state.selected_stores[1]}**")
    
    # Placeholder Logic for menu display
    st.info("Menu generation logic active. Integrate your recipe database here.")
    
    if st.button("Start Over"):
        st.session_state.step = 1
        st.rerun()
