import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="Smartphone Sales Dashboard", layout="wide")

# Custom CSS for Colorful Miniso Aesthetic (Light Grey Filter Theme)
st.markdown("""
    <style>
        /* Overall Page Background */
        [data-testid="stAppViewContainer"] {
            background-color: #faf8f5 !important;
        }
        /* Sidebar Background */
        [data-testid="stSidebar"] {
            background-color: #f5f0eb !important;
            border-right: 1px solid #efe8e1 !important;
        }
        /* Top Navigation Header */
        [data-testid="stHeader"] {
            background-color: rgba(250, 248, 245, 0.8) !important;
            backdrop-filter: blur(10px);
        }
        /* Main Block Container Padding */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        /* Metric Typography Override */
        div[data-testid="stMetricValue"] {
            font-size: 32px;
            font-weight: 800;
            color: #2b1f1d !important;
            font-family: 'Outfit', 'Inter', sans-serif;
            margin-top: 4px;
        }
        div[data-testid="stMetricLabel"] {
            font-size: 11px;
            color: #6a5e52;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }
        /* Miniso-Style Colorful Cards */
        .kpi-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 16px;
            border: 1px solid #efe8e1;
            box-shadow: 0 6px 16px rgba(139, 115, 85, 0.04);
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }
        .kpi-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 24px rgba(139, 115, 85, 0.08);
        }
        /* Unique Accent Colors for KPI Cards */
        .kpi-red { border-top: 4px solid #ff253a !important; }
        .kpi-blue { border-top: 4px solid #339af0 !important; }
        .kpi-gold { border-top: 4px solid #fcc419 !important; }
        .kpi-teal { border-top: 4px solid #2ec4b6 !important; }

        /* Filters Section Styling Overrides (Light Grey, No Red) */
        [data-testid="stSidebar"] [data-baseweb="tag"] {
            background-color: #e6e0d8 !important;
            color: #42302e !important;
        }
        [data-testid="stSidebar"] div[data-baseweb="select"] > div {
            border-color: #efe8e1 !important;
        }
        [data-testid="stSidebar"] div[data-baseweb="select"]:focus-within > div {
            border-color: #ccc5b9 !important;
        }
        [data-testid="stSidebar"] div[data-baseweb="input"] {
            border-color: #efe8e1 !important;
        }
        [data-testid="stSidebar"] div[data-baseweb="input"]:focus-within {
            border-color: #ccc5b9 !important;
        }
        [data-testid="stSidebar"] {
            --primary-color: #ccc5b9 !important;
        }

        /* Button overrides */
        div.stButton > button {
            background-color: #ffffff !important;
            color: #6a5e52 !important;
            border: 1px solid #efe8e1 !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            width: 100%;
        }
        div.stButton > button:hover {
            border-color: #ccc5b9 !important;
            color: #42302e !important;
            background-color: #fcfbf9 !important;
        }
        /* Primary Button (Apply Filters) - Light Grey Style */
        div.stButton > button[kind="primary"] {
            background-color: #ccc5b9 !important;
            color: #42302e !important;
            border: 1px solid #bcae9e !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 12px rgba(204, 197, 185, 0.15) !important;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #bcae9e !important;
            color: #2b1f1d !important;
            border-color: #a89a8a !important;
            box-shadow: 0 6px 18px rgba(188, 174, 158, 0.3) !important;
        }
        /* Typography headings */
        h1 {
            color: #2b1f1d !important;
            font-family: 'Outfit', sans-serif;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
        }
        h2, h3, h4 {
            color: #42302e !important;
            font-family: 'Outfit', sans-serif;
            font-weight: 700 !important;
            letter-spacing: -0.2px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📱 Smartphone Sales & Analytics Dashboard")
st.markdown("A premium, colorful Miniso-themed analytics dashboard for multi-brand smartphone sales data across India.")

# Set global Matplotlib and Seaborn styles for Miniso Light Theme
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'figure.facecolor': '#ffffff',
    'axes.facecolor': '#ffffff',
    'text.color': '#42302e',
    'axes.labelcolor': '#6a5e52',
    'xtick.color': '#6a5e52',
    'ytick.color': '#6a5e52',
    'font.family': 'sans-serif'
})

# Miniso Pastel Color Palette
MINISO_COLORS = ['#ff6b6b', '#339af0', '#fcc419', '#2ec4b6', '#da77f2', '#ff922b']
MINISO_COLORS_EXTENDED = ['#ff6b6b', '#4dabf7', '#37b24d', '#f59e0b', '#b197fc', '#fcc419',
                          '#ff922b', '#2ec4b6', '#e64980', '#20c997']

# 2. Load CSV Data
@st.cache_data
def load_data():
    df = pd.read_csv('smartphone_dashboard_dataset.csv')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading file: {e}. Please make sure 'smartphone_dashboard_dataset.csv' is in the same directory.")
    st.stop()

# 3. Sidebar Filter Section
st.sidebar.header("🎛️ Dashboard Filters")

# Initialize session state for applied filters
if 'applied_filters' not in st.session_state:
    st.session_state.applied_filters = None

# Filter 1: Brand Multiselect
all_brands = sorted(df['Brand'].dropna().unique())
selected_brands = st.sidebar.multiselect(
    "1. Select Brands",
    options=all_brands,
    default=all_brands
)

# Filter 2: Cascading Model Filter (updates dynamically based on selected brands)
if selected_brands:
    filtered_models_pool = df[df['Brand'].isin(selected_brands)]
else:
    filtered_models_pool = df
all_models = sorted(filtered_models_pool['Model_Name'].dropna().unique())

selected_models = st.sidebar.multiselect(
    "2. Select Models",
    options=all_models,
    default=all_models
)

# Filter 3: Complaint Reason Multiselect
all_complaints = sorted(df['Main_Complaint_Reason'].dropna().unique())
selected_complaints = st.sidebar.multiselect(
    "3. Complaint Reason",
    options=all_complaints,
    default=all_complaints
)

# Filter 4: Price Range Slider
min_price = int(df['Price_INR'].min())
max_price = int(df['Price_INR'].max())
selected_price_range = st.sidebar.slider(
    "4. Price Range (₹)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price),
    step=1000,
    format="₹%d"
)

# Filter 5: Rating Range Slider
min_rating = float(df['Avg_Rating'].min())
max_rating = float(df['Avg_Rating'].max())
selected_rating_range = st.sidebar.slider(
    "5. Rating Range",
    min_value=min_rating,
    max_value=max_rating,
    value=(min_rating, max_rating),
    step=0.1,
    format="%.1f"
)

# Sidebar Action Buttons
col_btn1, col_btn2 = st.sidebar.columns(2)
with col_btn1:
    apply_clicked = st.button("Apply Filters", type="primary", use_container_width=True)
with col_btn2:
    reset_clicked = st.button("Reset Filters", use_container_width=True)

# Default filter values mapping
default_filters = {
    'brands': all_brands,
    'models': all_models,
    'complaints': all_complaints,
    'price_range': (min_price, max_price),
    'rating_range': (min_rating, max_rating)
}

# On first load or reset, apply defaults
if st.session_state.applied_filters is None or reset_clicked:
    st.session_state.applied_filters = default_filters
    if reset_clicked:
        st.rerun()

# Save user filters on Apply click
if apply_clicked:
    st.session_state.applied_filters = {
        'brands': selected_brands,
        'models': selected_models,
        'complaints': selected_complaints,
        'price_range': selected_price_range,
        'rating_range': selected_rating_range
    }

# Read filters from applied state to render metrics and graphs
af = st.session_state.applied_filters
filtered_df = df[
    (df['Brand'].isin(af['brands'])) &
    (df['Model_Name'].isin(af['models'])) &
    (df['Main_Complaint_Reason'].isin(af['complaints'])) &
    (df['Price_INR'] >= af['price_range'][0]) &
    (df['Price_INR'] <= af['price_range'][1]) &
    (df['Avg_Rating'] >= af['rating_range'][0]) &
    (df['Avg_Rating'] <= af['rating_range'][1])
]

# 4. KPI Metrics Summary Bar
st.markdown("### 📈 Key Metrics Summary")
if filtered_df.empty:
    st.warning("⚠️ No data available matching current filters. Please adjust selections in the sidebar and click 'Apply Filters'.")
else:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="kpi-card kpi-red">', unsafe_allow_html=True)
        st.metric("Total Units Sold", f"{filtered_df['Units_Sold'].sum():,}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="kpi-card kpi-blue">', unsafe_allow_html=True)
        revenue_cr = filtered_df['Total_Revenue_INR'].sum() / 1e7
        st.metric("Total Revenue (₹ Cr)", f"₹{revenue_cr:,.1f}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="kpi-card kpi-gold">', unsafe_allow_html=True)
        st.metric("Avg. Rating ⭐", f"{filtered_df['Avg_Rating'].mean():.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="kpi-card kpi-teal">', unsafe_allow_html=True)
        st.metric("Total Complaints", f"{filtered_df['Complaint_Count'].sum():,}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── 5. Visualizations Layout (2 columns grid) ──

    # Row 1: Revenue & Brand Analysis
    st.markdown("#### Phase 1: Revenue & Brand Analysis")
    r1c1, r1c2 = st.columns(2)

    with r1c1:
        st.subheader("1. Revenue by Brand")
        brand_rev = filtered_df.groupby('Brand')['Total_Revenue_INR'].sum().reset_index()
        brand_rev['Revenue_Cr'] = brand_rev['Total_Revenue_INR'] / 1e7
        brand_rev = brand_rev.sort_values('Revenue_Cr', ascending=True)
        fig1, ax1 = plt.subplots(figsize=(5, 3.5))
        sns.barplot(data=brand_rev, x='Revenue_Cr', y='Brand', hue='Brand', ax=ax1, palette=MINISO_COLORS, legend=False)
        ax1.set_xlabel("Revenue (₹ Crores)")
        ax1.set_ylabel("")
        ax1.set_title("Total Revenue by Brand", fontsize=10, color='#42302e')
        plt.tight_layout()
        st.pyplot(fig1)
        plt.close()

    with r1c2:
        st.subheader("2. Units Sold by Brand")
        brand_units = filtered_df.groupby('Brand')['Units_Sold'].sum().reset_index()
        brand_units = brand_units.sort_values('Units_Sold', ascending=False)
        fig2 = px.bar(brand_units, x='Brand', y='Units_Sold', color='Brand',
                      color_discrete_sequence=MINISO_COLORS, title="Total Units Sold by Brand")
        fig2.update_layout(template="plotly_white", margin=dict(t=30, b=10, l=10, r=10),
                          paper_bgcolor='#ffffff', plot_bgcolor='#ffffff', showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # Row 2: Model & Price Analysis
    st.markdown("#### Phase 2: Model & Price Analysis")
    r2c1, r2c2 = st.columns(2)

    with r2c1:
        st.subheader("3. Top 10 Models by Revenue")
        model_rev = filtered_df.groupby('Model_Name')['Total_Revenue_INR'].sum().reset_index()
        model_rev['Revenue_Cr'] = model_rev['Total_Revenue_INR'] / 1e7
        model_rev = model_rev.sort_values('Revenue_Cr', ascending=False).head(10)
        model_rev = model_rev.sort_values('Revenue_Cr', ascending=True)
        fig3 = px.bar(model_rev, x='Revenue_Cr', y='Model_Name', orientation='h',
                      color='Revenue_Cr', color_continuous_scale='Sunset',
                      title="Top 10 Revenue Generating Models")
        fig3.update_layout(template="plotly_white", margin=dict(t=30, b=10, l=10, r=10),
                          paper_bgcolor='#ffffff', plot_bgcolor='#ffffff',
                          xaxis_title="Revenue (₹ Crores)", yaxis_title="")
        st.plotly_chart(fig3, use_container_width=True)

    with r2c2:
        st.subheader("4. Price Distribution by Brand")
        fig4 = px.box(filtered_df, x='Brand', y='Price_INR', color='Brand',
                      color_discrete_sequence=MINISO_COLORS, title="Price Spread Across Brands")
        fig4.update_layout(template="plotly_white", margin=dict(t=30, b=10, l=10, r=10),
                          paper_bgcolor='#ffffff', plot_bgcolor='#ffffff', showlegend=False,
                          yaxis_title="Price (₹)")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # Row 3: Ratings & Reviews
    st.markdown("#### Phase 3: Ratings & Reviews")
    r3c1, r3c2 = st.columns(2)

    with r3c1:
        st.subheader("5. Rating Tier Distribution")
        # Create rating buckets
        bins = [3.8, 4.0, 4.3, 4.6, 4.9]
        labels = ['3.9-4.0', '4.1-4.3', '4.4-4.6', '4.7-4.8']
        filtered_df_copy = filtered_df.copy()
        filtered_df_copy['Rating_Tier'] = pd.cut(filtered_df_copy['Avg_Rating'], bins=bins, labels=labels, include_lowest=True)
        rating_counts = filtered_df_copy['Rating_Tier'].value_counts().reset_index()
        rating_counts.columns = ['Rating Tier', 'Count']
        pie_colors = ['#ff6b6b', '#339af0', '#fcc419', '#2ec4b6']
        fig5 = px.pie(rating_counts, values='Count', names='Rating Tier', hole=0.35,
                      color_discrete_sequence=pie_colors, title="Product Ratings Distribution")
        fig5.update_layout(template="plotly_white", margin=dict(t=30, b=10, l=10, r=10),
                          paper_bgcolor='#ffffff')
        st.plotly_chart(fig5, use_container_width=True)

    with r3c2:
        st.subheader("6. Reviews vs Rating (Bubble)")
        fig6 = px.scatter(filtered_df, x='Avg_Rating', y='Total_Reviews', color='Brand',
                          size='Units_Sold', hover_name='Model_Name',
                          color_discrete_sequence=MINISO_COLORS,
                          title="Reviews vs Rating Correlation")
        fig6.update_layout(template="plotly_white", margin=dict(t=30, b=10, l=10, r=10),
                          paper_bgcolor='#ffffff', plot_bgcolor='#ffffff',
                          xaxis_title="Average Rating", yaxis_title="Total Reviews")
        st.plotly_chart(fig6, use_container_width=True)

    st.markdown("---")

    # Row 4: Complaints & Returns
    st.markdown("#### Phase 4: Complaints & Returns")
    r4c1, r4c2 = st.columns(2)

    with r4c1:
        st.subheader("7. Complaint Breakdown")
        complaint_counts = filtered_df['Main_Complaint_Reason'].value_counts().reset_index()
        complaint_counts.columns = ['Complaint Reason', 'Count']
        fig7 = px.pie(complaint_counts, values='Count', names='Complaint Reason', hole=0.3,
                      color_discrete_sequence=MINISO_COLORS, title="Complaint Reason Distribution")
        fig7.update_layout(template="plotly_white", margin=dict(t=30, b=10, l=10, r=10),
                          paper_bgcolor='#ffffff')
        st.plotly_chart(fig7, use_container_width=True)

    with r4c2:
        st.subheader("8. Avg Return Rate by Brand")
        brand_return = filtered_df.groupby('Brand')['Return_Rate_Percentage'].mean().reset_index()
        brand_return = brand_return.sort_values('Return_Rate_Percentage', ascending=False)
        fig8 = px.bar(brand_return, x='Brand', y='Return_Rate_Percentage', color='Brand',
                      color_discrete_sequence=MINISO_COLORS,
                      title="Average Return Rate (%) by Brand")
        fig8.update_layout(template="plotly_white", margin=dict(t=30, b=10, l=10, r=10),
                          paper_bgcolor='#ffffff', plot_bgcolor='#ffffff', showlegend=False,
                          yaxis_title="Return Rate (%)")
        st.plotly_chart(fig8, use_container_width=True)

    st.markdown("---")

    # Row 5: Heatmap & Info
    r5c1, r5c2 = st.columns(2)

    with r5c1:
        st.subheader("9. Complaints vs Brand (Heatmap)")
        pivot_data = pd.crosstab(filtered_df['Main_Complaint_Reason'], filtered_df['Brand'])
        fig9, ax9 = plt.subplots(figsize=(6, 4))
        sns.heatmap(pivot_data, annot=True, fmt='d', cmap='YlGnBu', ax=ax9, cbar=True,
                    linewidths=0.5, linecolor='#efe8e1')
        ax9.set_title("Complaint × Brand Density Matrix", fontsize=10, color='#42302e')
        ax9.set_xlabel("")
        ax9.set_ylabel("")
        plt.tight_layout()
        st.pyplot(fig9)
        plt.close()

    with r5c2:
        st.info("ℹ️ Filters in the sidebar update all 9 visual representations and metrics dynamically. Click **'Apply Filters'** to refresh the dashboard.")
        st.markdown("---")
        # Bonus: Quick brand comparison table
        st.markdown("##### 📊 Quick Brand Summary")
        brand_summary = filtered_df.groupby('Brand').agg(
            Models=('Model_Name', 'nunique'),
            Avg_Price=('Price_INR', 'mean'),
            Avg_Rating=('Avg_Rating', 'mean'),
            Total_Units=('Units_Sold', 'sum'),
            Avg_Return=('Return_Rate_Percentage', 'mean')
        ).reset_index()
        brand_summary['Avg_Price'] = brand_summary['Avg_Price'].apply(lambda x: f"₹{x:,.0f}")
        brand_summary['Avg_Rating'] = brand_summary['Avg_Rating'].apply(lambda x: f"{x:.2f}")
        brand_summary['Total_Units'] = brand_summary['Total_Units'].apply(lambda x: f"{x:,}")
        brand_summary['Avg_Return'] = brand_summary['Avg_Return'].apply(lambda x: f"{x:.1f}%")
        brand_summary.columns = ['Brand', 'Models', 'Avg Price', 'Rating', 'Units Sold', 'Return %']
        st.dataframe(brand_summary, use_container_width=True, hide_index=True)

st.sidebar.markdown("---")
st.sidebar.info("📱 Smartphone Sales Dashboard — Miniso Style")
