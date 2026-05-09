import streamlit as st
import pandas as pd

# 1. Initialize session state at the very top
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

# 3. Final Fix for Line 31 (Referencing your screenshot)
# We check if the list has content BEFORE passing it to pandas
if st.session_state.items:
    df = pd.DataFrame(st.session_state.items)
    st.table(df)
    
    # Financial summary
    total = df["Price"].sum()
    st.success(f"Total Amount: ₹{total:,.2f}")
    
    if st.button("Clear Invoice"):
        st.session_state.items = []
        st.rerun()
else:
    # This prevents the ValueError by providing an alternative to the DataFrame
    st.info("No items added yet. Enter item details above to generate the invoice.")