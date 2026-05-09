import streamlit as st
import pandas as pd

# 1. Initialize 'items' if it doesn't exist yet
# This must happen before you try to .append() to it
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
        # Now this will work because 'items' was initialized above
        st.session_state.items.append({"Item": item_name, "Price": price})
        st.rerun()

st.header("Current Invoice Items")

# 3. Check if there's data before showing the table
if st.session_state.items:
    df = pd.DataFrame(st.session_state.items)
    st.table(df)
    
    total = df["Price"].sum()
    st.success(f"Total Amount: ₹{total:,.2f}")
    
    if st.button("Clear Invoice"):
        st.session_state.items = []
        st.rerun()
else:
    st.info("No items added yet. Enter details above to start.")