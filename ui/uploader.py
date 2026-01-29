import streamlit as st
import pandas as pd
from services.calculator import DiscrepancyCalculator
from database.db_manager import DatabaseManager

def render_uploader_page():
    st.header("📂 Data Ingestion")
    st.markdown("Upload CSV reports to calculate discrepancies.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Internal Report (GAM)")
        file_int = st.file_uploader("Upload Internal CSV", key="int")
        # Template help
        st.caption("Required cols: Date, Impressions, Revenue")

    with col2:
        st.subheader("2. External Report (SSP)")
        file_ext = st.file_uploader("Upload Vendor CSV", key="ext")
        st.caption("Required cols: Date, Impressions, Revenue")

    if file_int and file_ext:
        if st.button("Run Reconciliation Process"):
            try:
                df_int = pd.read_csv(file_int)
                df_ext = pd.read_csv(file_ext)
                
                # Process
                calculator = DiscrepancyCalculator()
                final_df = calculator.merge_and_calculate(df_int, df_ext)
                
                # Save to DB
                db = DatabaseManager()
                success = db.save_report(final_df)
                
                if success:
                    st.success("✅ Data reconciled and saved to Database!")
                else:
                    st.error("Failed to save to DB.")
                    
            except Exception as e:
                st.error(f"Error processing files: {e}")
