import streamlit as st
import plotly.express as px
from database.db_manager import DatabaseManager
from config.settings import DISCREPANCY_THRESHOLD

def render_dashboard_page():
    st.header("📊 Executive Dashboard")
    
    db = DatabaseManager()
    df = db.get_all_data()
    
    if df.empty:
        st.info("No data in database. Please upload files in the 'Upload' tab.")
        return

    # --- KPI CARDS ---
    avg_disc = df['discrepancy_imps'].mean()
    total_rev_loss = df['internal_rev'].sum() - df['external_rev'].sum()
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Avg Imps Discrepancy", f"{avg_disc:.2f}%")
    kpi2.metric("Total Revenue Gap", f"${total_rev_loss:,.2f}")
    kpi3.metric("Data Points", len(df))

    st.divider()

    # --- CHARTS ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Daily Discrepancy Trend (%)")
        fig_line = px.line(df, x='date', y='discrepancy_imps', 
                           title="Impression Discrepancy over Time")
        # Add a red line for threshold
        fig_line.add_hline(y=DISCREPANCY_THRESHOLD, line_dash="dot", line_color="red", annotation_text="Threshold")
        st.plotly_chart(fig_line, use_container_width=True)
        
    with col2:
        st.subheader("Revenue Comparison")
        # Melt for side-by-side bars
        melted = df.melt(id_vars=['date'], value_vars=['internal_rev', 'external_rev'], var_name='Source', value_name='Revenue')
        fig_bar = px.bar(melted, x='date', y='Revenue', color='Source', barmode='group')
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- DATA TABLE ---
    st.subheader("Detailed Recon Report")
    
    # Conditional Formatting logic
    def highlight_high_disc(val):
        color = 'red' if val > DISCREPANCY_THRESHOLD else 'black'
        return f'color: {color}'

    st.dataframe(
        df.style.applymap(highlight_high_disc, subset=['discrepancy_imps', 'discrepancy_rev']),
        use_container_width=True
    )
