import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# Use local backend if available, otherwise fallback to Render URL
API_URL = "http://localhost:8000"
try:
    if not requests.get(f"{API_URL}/health", timeout=0.5).ok:
        API_URL = "https://ticket-api.onrender.com"
except Exception:
    API_URL = "https://ticket-api.onrender.com"


st.set_page_config(
    page_title="Support Routing Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 1. CSS Stylesheet (Bespoke Professional Black Mode Layout)
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=Source+Sans+3:ital,wght@0,200..900;1,200..900&family=Fira+Code:wght@300..700&display=swap');

    /* Global layout adjustments */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Source Sans 3', sans-serif !important;
        background-color: #090503 !important; /* Deep warm black background */
        color: #FAFAF9 !important; /* Warm white text */
    }
    
    /* Remove padding around the main block */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    /* Headings styling */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        color: #FAFAF9 !important;
        margin-top: 0 !important;
    }

    /* Custom sidebar style */
    section[data-testid="stSidebar"] {
        background-color: #17120F !important; /* Dark warm brown surface */
        border-right: 1px solid #3C312B !important; /* Dark brown border */
        padding: 2.5rem 1.5rem 1.5rem 1.5rem !important;
    }
    
    section[data-testid="stSidebar"] h2 {
        font-size: 20px !important;
        color: #FAFAF9 !important;
    }

    /* Form Fields and Inputs styling */
    textarea {
        background-color: #17120F !important; /* Surface */
        border: 1px solid #3C312B !important; /* Dark brown border */
        border-radius: 8px !important;
        color: #FAFAF9 !important;
        font-size: 15px !important;
        line-height: 1.5 !important;
        padding: 14px !important;
        transition: border-color 150ms, box-shadow 150ms !important;
    }
    
    textarea:focus {
        border-color: #C2410C !important; /* Terracotta focus border */
        box-shadow: 0 0 0 3px rgba(194,65,12,0.15) !important;
    }

    /* Primary CTA Button (Terracotta) */
    div.stButton > button[kind="primary"] {
        background-color: #C2410C !important;
        color: #FAFAF9 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        letter-spacing: 0.02em !important;
        height: 42px !important;
        padding: 0 28px !important;
        box-shadow: 0 2px 4px rgba(194,65,12,0.2) !important;
        transition: all 150ms ease !important;
    }
    
    div.stButton > button[kind="primary"]:hover {
        background-color: #9A3412 !important;
        box-shadow: 0 4px 12px rgba(194,65,12,0.3) !important;
        transform: translateY(-1px);
    }
    
    div.stButton > button[kind="primary"]:active {
        transform: translateY(0);
    }

    /* Secondary Button style */
    div.stButton > button[kind="secondary"] {
        background-color: transparent !important;
        color: #FAFAF9 !important;
        border: 1px solid #3C312B !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        height: 38px !important;
        padding: 0 20px !important;
        transition: all 150ms ease !important;
    }
    
    div.stButton > button[kind="secondary"]:hover {
        background-color: #261E1A !important; /* Hover state raised */
        border-color: #78716C !important;
    }

    /* File Uploader styling */
    div[data-testid="stFileUploader"] {
        background-color: #17120F !important;
        border: 1px dashed #3C312B !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }

    /* Spinner colors custom */
    div[data-testid="stSpinner"] > div {
        border-top-color: #C2410C !important;
    }
    
    /* Header label separator */
    .divider-line {
        border-bottom: 1px solid #3C312B;
        padding-bottom: 24px;
        margin-bottom: 32px;
    }
</style>
""", unsafe_allow_html=True)

# ── 2. Top Navigation & Brand Header
st.markdown("""
<div class="divider-line">
    <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.15em; color: #A8A29E; margin-bottom: 6px; font-weight: 600;">Workflow Intelligence</div>
    <div style="font-family: 'Playfair Display', serif; font-size: 42px; font-weight: 700; color: #FAFAF9; line-height: 1.1;">Support Ticket Routing System</div>
    <div style="font-size: 15px; color: #A8A29E; margin-top: 8px; font-family: 'Source Sans 3', sans-serif; max-width: 750px;">
        Automate incoming ticket categorization, prioritize operational urgency, and intelligently route incidents to correct departments under tight SLA windows.
    </div>
</div>
""", unsafe_allow_html=True)

# ── 3. Sidebar: Batch Upload & Automation Settings
with st.sidebar:
    st.markdown("## Batch Classification")
    st.markdown(
        "<div style='font-size: 13px; color: #A8A29E; margin-bottom: 16px;'>"
        "Upload a batch of tickets in CSV format. The file must contain a column named <code>text</code>."
        "</div>", 
        unsafe_allow_html=True
    )
    uploaded = st.file_uploader("Choose CSV File", type="csv")
    
    if uploaded:
        df_up = pd.read_csv(uploaded)
        if st.button("Process Batch", type="secondary"):
            if 'text' in df_up.columns:
                tickets = [{"text": str(t)} for t in df_up['text'].tolist()]
                with st.spinner("Classifying tickets..."):
                    try:
                        res = requests.post(f"{API_URL}/classify/batch", json=tickets)
                        if res.ok:
                            results = pd.DataFrame(res.json())
                            st.markdown("### Classified Results")
                            st.dataframe(results, use_container_width=True)
                            
                            csv = results.to_csv(index=False)
                            st.download_button(
                                label="Download CSV Results",
                                data=csv,
                                file_name="classified_tickets_export.csv",
                                mime="text/csv",
                                type="primary"
                            )
                        else:
                            st.error(f"API Error: Failed to process batch request.")
                    except Exception as e:
                        st.error(f"Connection failure: {e}")
            else:
                st.error("Missing column: 'text' column is required.")

# ── 4. Main Panel Layout
col1, col2 = st.columns([1.6, 1])

with col1:
    st.markdown("### Interactive Classification")
    st.markdown(
        "<div style='font-size: 13px; color: #A8A29E; margin-bottom: 12px;'>"
        "Enter raw customer inquiries or support emails to evaluate category and urgency labels."
        "</div>", 
        unsafe_allow_html=True
    )
    
    ticket_text = st.text_area(
        label="Ticket Input",
        placeholder="e.g. I am getting a database timeout error when attempting to sync records over our office VPN connection...",
        height=160,
        label_visibility="collapsed"
    )
    
    # Primary Terracotta classification trigger
    if st.button("Analyze Ticket", type="primary") and ticket_text:
        with st.spinner("Running classification model..."):
            try:
                res = requests.post(f"{API_URL}/classify", json={"text": ticket_text})
                if res.ok:
                    r = res.json()
                    
                    # Compute custom semantic styles for Urgency level badge
                    urg_label = r['urgency'].upper()
                    urgency_colors = {
                        'high': ('#451A1A', '#F87171', '🔴', 'Critical Response Required'),
                        'medium': ('#452A1A', '#FBBF24', '🟡', 'Standard Response Window'),
                        'low': ('#143A24', '#34D399', '🟢', 'General Resolution SLA')
                    }
                    bg_col, text_col, icon, badge_lbl = urgency_colors.get(r['urgency'], ('#17120F', '#A8A29E', '⚪', 'No Priority'))
                    
                    # We output the HTML with ZERO leading indent inside triple quotes to ensure markdown parser
                    # treats it as HTML blocks instead of raw code blocks.
                    html_content = f"""<div style="background-color: #17120F; border: 1px solid #3C312B; border-radius: 12px; padding: 24px; margin-top: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 8px;">
        <span style="background-color: #261E1A; color: #FAFAF9; font-size: 12px; font-weight: 600; padding: 6px 14px; border-radius: 9999px; letter-spacing: 0.04em;">
            📁 CATEGORY: {r['category'].upper()}
        </span>
        <span style="background-color: {bg_col}; color: {text_col}; font-size: 12px; font-weight: 600; padding: 6px 14px; border-radius: 9999px; display: inline-flex; align-items: center; gap: 6px;">
            {icon} {urg_label} URGENCY
        </span>
    </div>
    <div style="margin-bottom: 24px;">
        <div style="font-size: 11px; color: #A8A29E; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px; font-weight: 600;">Routed Operations Team</div>
        <div style="font-family: 'Playfair Display', serif; font-size: 26px; font-weight: 700; color: #FAFAF9;">{r['department']}</div>
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; border-top: 1px solid #3C312B; padding-top: 20px;">
        <div>
            <div style="font-size: 11px; color: #A8A29E; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px; font-weight: 600;">Response SLA Window</div>
            <div style="font-size: 18px; font-weight: 600; color: #FAFAF9; display: flex; align-items: center; gap: 6px;">
                ⏳ {r['sla_hours']} Hours
            </div>
        </div>
        <div>
            <div style="font-size: 11px; color: #A8A29E; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px; font-weight: 600;">Model Classification Confidence</div>
            <div style="font-size: 18px; font-weight: 600; color: #C2410C;">
                🎯 {r['cat_confidence']}%
            </div>
        </div>
    </div>
</div>"""
                    st.markdown(html_content, unsafe_allow_html=True)
                else:
                    st.error("Inference failed: The classification API returned an error.")
            except Exception as e:
                st.error(f"Inference Connection Error: Is the API server running? Details: {e}")

with col2:
    st.markdown("### Department Workload")
    st.markdown(
        "<div style='font-size: 13px; color: #A8A29E; margin-bottom: 16px;'>"
        "Active ticket queue allocations and average cycle response times by department."
        "</div>", 
        unsafe_allow_html=True
    )
    
    # Realistically mapped columns and workloads
    workload = pd.DataFrame({
        'Team': ['Finance Team', 'Security Ops', 'IT Hardware Desk', 'Network Ops', 'Software Support'],
        'Open Tickets': [11, 8, 15, 23, 31],
        'Avg Resolution (hrs)': [12, 6, 24, 18, 9]
    })
    
    # Custom dark theme color scaling
    fig = px.bar(
        workload, 
        x='Open Tickets', 
        y='Team', 
        orientation='h',
        color='Open Tickets', 
        color_continuous_scale=[
            [0.0, '#3C312B'],   # Dark brown
            [0.5, '#F59E0B'],   # Accent Amber
            [1.0, '#C2410C']    # Terracotta
        ]
    )
    
    # Clean layout that blends perfectly in the dark theme
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Source Sans 3, sans-serif", size=11, color="#FAFAF9"),
        margin=dict(t=0, b=0, l=10, r=10),
        height=220,
        coloraxis_showscale=False,
        xaxis=dict(
            title="", 
            gridcolor="#261E1A", 
            zerolinecolor="#3C312B", 
            tickfont=dict(color="#A8A29E")
        ),
        yaxis=dict(
            title="", 
            gridcolor="rgba(0,0,0,0)", 
            zerolinecolor="#3C312B", 
            tickfont=dict(color="#A8A29E")
        )
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ── 5. Bottom: volume trend chart
st.divider()
st.markdown("### Weekly Routing Volume Trends")
st.markdown(
    "<div style='font-size: 13px; color: #A8A29E; margin-bottom: 12px;'>"
    "Daily rolling counts of classified support requests across key operational categories."
    "</div>", 
    unsafe_allow_html=True
)

dates = pd.date_range(end=datetime.today(), periods=7)
trend = pd.DataFrame({
    'Date': dates,
    'Billing': [12, 15, 9, 18, 14, 11, 16],
    'Access/Security': [8, 6, 11, 9, 7, 10, 8],
    'Hardware': [15, 18, 12, 21, 17, 14, 19],
    'Network': [20, 22, 16, 25, 22, 19, 23],
    'Software': [24, 28, 19, 31, 26, 22, 29],
})

trend_melted = trend.melt(id_vars='Date', var_name='Category', value_name='Count')
color_sequence = ['#C2410C', '#F59E0B', '#A8A29E', '#9A3412', '#78716C']

fig2 = px.line(
    trend_melted, 
    x='Date', 
    y='Count', 
    color='Category', 
    markers=True,
    color_discrete_sequence=color_sequence
)

fig2.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Source Sans 3, sans-serif", size=11, color="#FAFAF9"),
    margin=dict(t=5, b=0, l=10, r=10),
    height=220,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        title="",
        font=dict(color="#FAFAF9")
    ),
    xaxis=dict(
        title="", 
        gridcolor="#261E1A", 
        zerolinecolor="#3C312B", 
        tickfont=dict(color="#A8A29E")
    ),
    yaxis=dict(
        title="", 
        gridcolor="#261E1A", 
        zerolinecolor="#3C312B", 
        tickfont=dict(color="#A8A29E")
    )
)

st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
