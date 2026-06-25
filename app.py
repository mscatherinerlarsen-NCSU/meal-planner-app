import streamlit as st
import pandas as pd
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Smart Meal Planner", page_icon="🍲", layout="centered")

# --- MOCK DATABASE ---
# In the future, this will be replaced by your SQLite database and Web Scrapers
DIETS = ["Keto", "Vegan", "Vegetarian", "Gluten-Free", "Paleo", "Cost-Friendly", "Low-Carb"]
ALLERGIES = ["Peanuts", "Dairy", "Eggs", "Wheat", "Tree Nuts", "Soy", "Fish", "Shellfish", "Seafood"]

MOCK_RECIPES = {
    "Breakfast": ["Avocado Toast", "Oatmeal with Berries", "Scrambled Eggs", "Smoothie Bowl", "Protein Pancakes", "Greek Yogurt Parfait", "Keto Bacon & Eggs"],
    "Lunch": ["Quinoa Salad", "Turkey Wrap", "Lentil Soup", "Chicken Caesar Salad", "Veggie Stir Fry", "Tuna Salad", "Black Bean Bowl"],
    "Dinner": ["Grilled Salmon & Asparagus", "Beef Tacos", "Chicken Curry", "Eggplant Parmesan", "Steak & Sweet Potato", "Mushroom Risotto", "Zucchini Noodles & Meatballs"],
    "Snack": ["Apple Slices & Almond Butter", "Mixed Nuts", "Carrot Sticks & Hummus", "Cheese Stick", "Edamame", "Rice Cakes", "Dark Chocolate"]
}

MOCK_STORES = ["Fresh Market", "Value Groceries", "Neighborhood Market", "Organic Co-op"]

# --- SESSION STATE INITIALIZATION ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'selected_stores' not in st.session_state:
    st.session_state.selected_stores = []

# --- APP HEADER ---
st.title("🍲 Smart Meal Planner")
st.markdown("Generate a weekly, allergy-friendly menu based on local grocery sales.")
st.divider()

# --- STEP 1: USER CONSTRAINTS ---
if st.session_state.step == 1:
    st.subheader("Step 1: Your Preferences")
    
    col1, col2 = st.columns(2)
    with col1:
        diets = st.multiselect("Select up to 2 Diets", DIETS, max_selections=2)
        household_size = st.number_input("Household Members", min_value=1, value=2, step=1)
    with col2:
        allergies = st.multiselect("Select Allergies", ALLERGIES)
        zip_code = st.text_input("Zip Code", placeholder="e.g., 90210")
        
    if st.button("Find Local Stores", type="primary"):
        if not zip_code:
            st.error("Please enter a Zip Code to find local stores.")
        else:
            # Save inputs to session state
            st.session_state.household_size = household_size
            st.session_state.diets = diets
            st.session_state.allergies = allergies
            st.session_state.zip_code = zip_code
            st.session_state.step = 2
            st.rerun()

# --- STEP 2: STORE SELECTION ---
elif st.session_state.step == 2:
    st.subheader(f"Step 2: Local Stores near {st.session_state.zip_code}")
    st.markdown("Select exactly **two** stores to compare sales.")
    
    # Generate 4 random stores
    available_stores = random.sample(MOCK_STORES, 4)
    selected_stores = st.multiselect("Available Grocery Stores (Select 2)", available_stores, max_selections=2)
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Generate Menu", type="primary"):
            if len(selected_stores) != 2:
                st.error("You must select exactly two stores.")
            else:
                st.session_state.selected_stores = selected_stores
                st.session_state.step = 3
                st.rerun()

# --- STEP 3: MENU GENERATION ---
elif st.session_state.step == 3:
    st.subheader("Step 3: Your 7-Day Meal Plan")
    st.markdown(f"**Sourced from:** {st.session_state.selected_stores[0]} and {st.session_state.selected_stores[1]}")
    
    # Generate a 7-day menu DataFrame
    days = [f"Day {i}" for i in range(1, 8)]
    menu_data = {
        "Day": days,
        "Breakfast": [random.choice(MOCK_RECIPES["Breakfast"]) for _ in range(7)],
        "Lunch": [random.choice(MOCK_RECIPES["Lunch"]) for _ in range(7)],
        "Dinner": [random.choice(MOCK_RECIPES["Dinner"]) for _ in range(7)],
        "Snack": [random.choice(MOCK_RECIPES["Snack"]) for _ in range(7)]
    }
    
    df_menu = pd.DataFrame(menu_data)
    df_menu.set_index("Day", inplace=True)
    
    # Display the table cleanly
    st.dataframe(df_menu, use_container_width=True)
    
    # Calculate estimated cost
    base_cost_per_person_per_day = random.uniform(8.50, 15.00) 
    total_cost = base_cost_per_person_per_day * st.session_state.household_size * 7
    
    st.success(f"**Estimated Weekly Cost:** ${total_cost:.2f} total for {st.session_state.household_size} people.")
    
    if st.button("Start Over"):
        st.session_state.step = 1
        st.rerun()