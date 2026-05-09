import streamlit as st
import pandas as pd

# 1. Initialize session state for invoice items
if "items" not in st.session_state:
    st.session_state.items = []

st.title("Retailer Billing System")

# 2. Form to add new items (Manual-first logic)
with st.form("item_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        item_name = st.text_input("Item Name")
    with col2:
        price = st.number_input("Price", min_value=0.0, step=1.0)
    
    submitted = st.form_submit_button("Add to Invoice")
    
    if submitted and item_name:
        st.session_state.items.append({"Item": item_name, "Price": price})
        st.rerun()

st.header("Current Invoice Items")

# 3. Safe DataFrame creation (Fixes the error in image_a11697.png)
if st.session_state.items:
    # Converting the list of dictionaries to a DataFrame
    df = pd.DataFrame(st.session_state.items)
    
    # Display the table
    st.table(df)
    
    # Calculate Total
    total_amount = df["Price"].sum()
    st.subheader(f"Total Amount: ₹{total_amount:,.2f}")
    
    # Option to clear the invoice
    if st.button("Clear Invoice"):
        st.session_state.items = []
        st.rerun()
else:
    st.info("The invoice is currently empty. Add items above to get started.")