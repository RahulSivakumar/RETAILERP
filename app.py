import streamlit as st
import pandas as pd

# 1. Initialize the list in session state
if "items" not in st.session_state:
    st.session_state.items = []

st.title("Retailer Billing System")

# 2. Input Form
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

# 3. THE FIX: Guard line 30 (Referencing your screenshot)
# Only create the DataFrame if the list has items in it
if st.session_state.items:
    df = pd.DataFrame(st.session_state.items)
    st.table(df)
    
    # Optional: Display the total for the retailer
    total = df["Price"].sum()
    st.success(f"Total Amount: ₹{total:,.2f}")
    
    if st.button("Clear Invoice"):
        st.session_state.items = []
        st.rerun()
else:
    # This replaces the red error box with a clean notification
    st.info("The invoice is currently empty. Add an item above to get started.")