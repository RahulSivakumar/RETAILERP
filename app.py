import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="RETAIL ERP", layout="wide")

# --- SESSION STATE INITIALIZATION ---
if 'items' not in st.session_state:
    st.session_state.items = []

# --- UI HEADER ---
st.title("📄 RETAIL ERP - Billing & Ledger")

col1, col2, col3 = st.columns(3)
with col1:
    customer_name = st.text_input("Customer/Party Name", value="Cash Sale")
with col2:
    invoice_date = st.date_input("Transaction Date", datetime.now())
with col3:
    payment_type = st.selectbox("Payment Mode", ["Cash", "Online", "Credit (Payable Later)"])

st.divider()

# --- ITEM INPUT SECTION (Manual-First Logic) ---
with st.expander("➕ Add Items / Manual Entry", expanded=True):
    row1_col1, row1_col2, row1_col3, row1_col4 = st.columns([3, 1, 1, 1])
    
    with row1_col1:
        item_name = st.text_input("Product Name") # Manual entry for flexibility
    with row1_col2:
        qty = st.number_input("Qty", min_value=1, value=1)
    with row1_col3:
        unit_price = st.number_input("Unit Price (₹)", min_value=0.0, value=0.0, step=1.0)
    with row1_col4:
        tax_rate = st.selectbox("GST %", [0, 5, 12, 18, 28], index=0)

    if st.button("Add to Bill"):
        if item_name and unit_price > 0:
            total_before_tax = qty * unit_price
            tax_amount = total_before_tax * (tax_rate / 100)
            st.session_state.items.append({
                "Product": item_name,
                "Qty": qty,
                "Price": unit_price,
                "GST %": tax_rate,
                "Total": total_before_tax + tax_amount
            })
            st.rerun()
        else:
            st.warning("Please enter a product name and price.")

# --- INVOICE SUMMARY & TABLE ---
if st.session_state.items:
    st.subheader("Current Invoice Items")
    df = pd.DataFrame(st.session_state.items)
    
    # Display table with an index so user can identify rows to remove
    st.table(df)

    # --- MANUAL REMOVE FEATURE ---
    remove_idx = st.number_input("Enter Row Index to Remove", min_value=0, max_value=len(st.session_state.items)-1, step=1)
    if st.button("❌ Remove Selected Row"):
        st.session_state.items.pop(remove_idx)
        st.rerun()

    # --- TOTALS ---
    grand_total = df['Total'].sum()
    st.divider()
    
    c1, c2 = st.columns([2, 1])
    with c2:
        st.write(f"### Grand Total: ₹{grand_total:,.2f}")
        if payment_type == "Credit (Payable Later)":
            st.warning(f"This will be added to {customer_name}'s Credit Ledger.")
            
        if st.button("Finalize & Save", type="primary"):
            # Placeholder for Database Save Logic
            st.success(f"Transaction saved successfully!")
            st.session_state.items = [] 
            st.rerun()
else:
    st.info("No items added yet. Use the section above to start billing.")