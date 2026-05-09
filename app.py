import streamlit as st
import pandas as pd

# 1. Initialize session state at the very start
# This ensures 'items' exists as soon as the app loads
if "items" not in st.session_state:
    st.session_state.items = []

st.title("Retailer Billing System")

# 2. Input Form for Manual Entry
# Using a form helps maintain the "manual-first" logic you prefer
with st.form("billing_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        item_name = st.text_input("Item Name")
    with col2:
        price = st.number_input("Price", min_value=0.0, step=1.0)
    
    add_button = st.form_submit_button("Add to Invoice")
    
    if add_button and item_name:
        st.session_state.items.append({"Item": item_name, "Price": price})
        st.rerun()

st.header("Current Invoice Items")

# 3. The "Safety Gate" (Fixes the error in image_a1082c.png)
# Only attempt to create a DataFrame if there is data to display
if st.session_state.items:
    df = pd.DataFrame(st.session_state.items)
    st.table(df)
    
    # Calculate and display total
    total = df["Price"].sum()
    st.markdown(f"**Total Amount: ₹{total:,.2f}**")
    
    if st.button("Clear All"):
        st.session_state.items = []
        st.rerun()
else:
    # This replaces the red error box with a clean notification
    st.info("No items added yet. Please use the form above to start the invoice.")