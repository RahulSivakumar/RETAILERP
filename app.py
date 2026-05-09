import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Business Billing System", layout="wide")

## --- UI HEADER ---
st.title("📄 New Sales Invoice")
col1, col2, col3 = st.columns(3)

with col1:
    customer_name = st.text_input("Customer Name", value="Cash Sale")
with col2:
    invoice_date = st.date_input("Invoice Date", datetime.now())
with col3:
    invoice_no = st.text_input("Invoice #", value="INV-1001")

st.divider()

## --- ITEM INPUT SECTION ---
### Using session_state to track "Manual" line items
if 'items' not in st.session_state:
    st.session_state.items = []

with st.expander("➕ Add Product to Invoice", expanded=True):
    row1_col1, row1_col2, row1_col3, row1_col4 = st.columns([3, 1, 1, 1])
    
    with row1_col1:
        item_name = st.selectbox("Select Product", ["Product A", "Product B", "Custom Item"])
    with row1_col2:
        qty = st.number_input("Qty", min_value=1, value=1)
    with row1_col3:
        # Manual Price Override
        unit_price = st.number_input("Unit Price (₹)", min_value=0.0, value=0.0, step=1.0)
    with row1_col4:
        tax_rate = st.selectbox("GST %", [0, 5, 12, 18, 28], index=3)

    if st.button("Add to Bill"):
        total = qty * unit_price
        st.session_state.items.append({
            "Product": item_name,
            "Qty": qty,
            "Price": unit_price,
            "GST %": tax_rate,
            "Total": total + (total * tax_rate / 100)
        })

## --- INVOICE TABLE ---
if st.session_state.items:
    st.subheader("Invoice Summary")
    df = pd.DataFrame(st.session_state.items)
    st.table(df)

    ## --- CALCULATIONS ---
    subtotal = df['Total'].sum()
    
    st.divider()
    c1, c2 = st.columns([2, 1])
    with c2:
        st.write(f"### Grand Total: ₹{subtotal:,.2f}")
        if st.button("Generate & Save Invoice", type="primary"):
            st.success(f"Invoice {invoice_no} saved and Inventory updated!")
            # Logic for Database saving will go here
            st.session_state.items = [] # Clear for next bill