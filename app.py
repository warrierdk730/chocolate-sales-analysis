import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Chocolate Sales Dashboard",
    page_icon="🍫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #fdf6f0; }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid #e8d5c4;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    [data-testid="metric-container"] label {
        color: #7a5c44 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #3d1f0d !important;
        font-size: 26px !important;
        font-weight: 700 !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricDelta"] {
        font-size: 13px !important;
    }

    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #6b3a2a, #a0522d);
        color: white;
        padding: 10px 20px;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 600;
        margin: 24px 0 16px 0;
        letter-spacing: 0.3px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #3d1f0d 0%, #6b3a2a 100%);
    }
    [data-testid="stSidebar"] * { color: #fdf6f0 !important; }
    [data-testid="stSidebar"] .stMultiSelect > div,
    [data-testid="stSidebar"] .stSelectbox > div { background: #7a4a35 !important; border-radius: 8px; }

    /* Title */
    .main-title {
        font-size: 32px;
        font-weight: 800;
        color: #3d1f0d;
        margin-bottom: 2px;
    }
    .main-sub {
        color: #7a5c44;
        font-size: 14px;
        margin-bottom: 20px;
    }

    /* Chart containers */
    .chart-box {
        background: white;
        border-radius: 12px;
        border: 1px solid #e8d5c4;
        padding: 4px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ── DATA LOADING ────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("Chocolate_Sales.csv")
    df["Amount"] = df["Amount"].replace(r"[\$,]", "", regex=True).astype(float)
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df["Boxes Shipped"] = pd.to_numeric(df["Boxes Shipped"], errors="coerce").fillna(0).astype(int)
    df["Sales Person"] = df["Sales Person"].str.strip()
    df["Product"] = df["Product"].str.strip()
    df["Country"] = df["Country"].str.strip()
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["MonthName"] = df["Date"].dt.strftime("%b")
    df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)
    df["Quarter"] = "Q" + df["Date"].dt.quarter.astype(str)
    return df

df_all = load_data()

# ── COLOUR PALETTE ──────────────────────────────────────────────────────────
CHOCO_COLORS = ["#3d1f0d", "#6b3a2a", "#a0522d", "#c8824a", "#e6a96a",
                "#f5cc99", "#f9e4c8", "#fdf6f0"]
PLOTLY_TEMPLATE = "plotly_white"

# ── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🍫 Filters")
    st.markdown("---")

    all_years = sorted(df_all["Year"].unique())
    sel_years = st.multiselect("📅 Year", all_years, default=all_years)

    all_countries = sorted(df_all["Country"].unique())
    sel_countries = st.multiselect("🌍 Country", all_countries, default=all_countries)

    all_products = sorted(df_all["Product"].unique())
    sel_products = st.multiselect("🍫 Product", all_products, default=all_products)

    all_sp = sorted(df_all["Sales Person"].unique())
    sel_sp = st.multiselect("👤 Salesperson", all_sp, default=all_sp)

    st.markdown("---")
    st.markdown("**📊 Pages**")
    page = st.radio("", ["Overview", "Products", "Salespeople", "Geography", "Trends"], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("<small>Chocolate Sales 2022–2024<br>Dataset: Kaggle<br>Built by: Dileep Kumar Warrier</small>", unsafe_allow_html=True)

# ── FILTERED DATA ────────────────────────────────────────────────────────────
df = df_all[
    df_all["Year"].isin(sel_years) &
    df_all["Country"].isin(sel_countries) &
    df_all["Product"].isin(sel_products) &
    df_all["Sales Person"].isin(sel_sp)
].copy()

if df.empty:
    st.warning("No data matches the selected filters. Please adjust your selections.")
    st.stop()

# ── HEADER ────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🍫 Chocolate Sales Dashboard</div>', unsafe_allow_html=True)
st.markdown(f'<div class="main-sub">Analysing {len(df):,} transactions across {df["Country"].nunique()} countries · {df["Product"].nunique()} products · {df["Sales Person"].nunique()} salespeople</div>', unsafe_allow_html=True)

# ── KPI METRICS (always visible) ─────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

total_rev = df["Amount"].sum()
total_boxes = df["Boxes Shipped"].sum()
avg_deal = df["Amount"].mean()
top_sp_name = df.groupby("Sales Person")["Amount"].sum().idxmax()
top_prod_name = df.groupby("Product")["Amount"].sum().idxmax()

df_valid = df[df["Boxes Shipped"] > 0]
rev_per_box = df_valid["Amount"].sum() / df_valid["Boxes Shipped"].sum() if len(df_valid) > 0 else 0

# YoY delta for total revenue (2022→2023 if both selected)
rev_2022 = df[df["Year"] == 2022]["Amount"].sum()
rev_2023 = df[df["Year"] == 2023]["Amount"].sum()
yoy_delta = ((rev_2023 - rev_2022) / rev_2022 * 100) if rev_2022 > 0 else None

k1.metric("💰 Total Revenue", f"${total_rev/1e6:.2f}M",
          delta=f"{yoy_delta:+.1f}% YoY (22→23)" if yoy_delta else None)
k2.metric("📦 Boxes Shipped", f"{total_boxes:,}")
k3.metric("🧾 Avg Deal Size", f"${avg_deal:,.0f}")
k4.metric("📈 Revenue / Box", f"${rev_per_box:.2f}")
k5.metric("🏅 Top Salesperson", top_sp_name.split()[0])

st.markdown("---")

# ════════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if page == "Overview":
    st.markdown('<div class="section-header">📊 Revenue Overview</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        # Monthly revenue trend
        monthly = df.groupby("YearMonth")["Amount"].sum().reset_index()
        monthly = monthly.sort_values("YearMonth")
        fig = px.area(monthly, x="YearMonth", y="Amount",
                      title="Monthly Revenue Trend",
                      color_discrete_sequence=["#a0522d"],
                      template=PLOTLY_TEMPLATE)
        fig.update_traces(fill="tozeroy", line_width=2.5, fillcolor="rgba(160,82,45,0.15)")
        fig.update_layout(xaxis_title="Month", yaxis_title="Revenue ($)",
                          yaxis_tickprefix="$", yaxis_tickformat=",.0f",
                          title_font_size=15, height=320,
                          margin=dict(t=45, b=10, l=10, r=10))
        fig.update_xaxes(tickangle=45, tickfont_size=10)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Revenue by country donut
        country_rev = df.groupby("Country")["Amount"].sum().reset_index()
        fig2 = px.pie(country_rev, names="Country", values="Amount",
                      title="Revenue by Country",
                      color_discrete_sequence=CHOCO_COLORS,
                      hole=0.45, template=PLOTLY_TEMPLATE)
        fig2.update_traces(textposition="outside", textinfo="percent+label",
                           textfont_size=11)
        fig2.update_layout(showlegend=False, height=320,
                           title_font_size=15,
                           margin=dict(t=45, b=10, l=10, r=10))
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        # Top 10 products by revenue
        prod_rev = df.groupby("Product")["Amount"].sum().sort_values(ascending=True).tail(10).reset_index()
        fig3 = px.bar(prod_rev, x="Amount", y="Product",
                      orientation="h", title="Top 10 Products by Revenue",
                      color="Amount", color_continuous_scale=["#f5cc99", "#a0522d", "#3d1f0d"],
                      template=PLOTLY_TEMPLATE)
        fig3.update_layout(xaxis_tickprefix="$", xaxis_tickformat=",.0f",
                           coloraxis_showscale=False, title_font_size=15,
                           height=340, margin=dict(t=45, b=10, l=10, r=10))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        # Top 10 salespeople by revenue
        sp_rev = df.groupby("Sales Person")["Amount"].sum().sort_values(ascending=True).tail(10).reset_index()
        fig4 = px.bar(sp_rev, x="Amount", y="Sales Person",
                      orientation="h", title="Top 10 Salespeople by Revenue",
                      color="Amount", color_continuous_scale=["#f5cc99", "#6b3a2a", "#3d1f0d"],
                      template=PLOTLY_TEMPLATE)
        fig4.update_layout(xaxis_tickprefix="$", xaxis_tickformat=",.0f",
                           coloraxis_showscale=False, title_font_size=15,
                           height=340, margin=dict(t=45, b=10, l=10, r=10))
        st.plotly_chart(fig4, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE: PRODUCTS
# ════════════════════════════════════════════════════════════════════════════
elif page == "Products":
    st.markdown('<div class="section-header">🍫 Product Performance Analysis</div>', unsafe_allow_html=True)

    df_v = df[df["Boxes Shipped"] > 0].copy()
    prod_stats = (df_v.groupby("Product")
                  .agg(Total_Revenue=("Amount", "sum"),
                       Total_Boxes=("Boxes Shipped", "sum"),
                       Transactions=("Amount", "count"))
                  .reset_index())
    prod_stats["Rev_per_Box"] = prod_stats["Total_Revenue"] / prod_stats["Total_Boxes"]
    prod_stats["Avg_Deal"] = prod_stats["Total_Revenue"] / prod_stats["Transactions"]

    col1, col2 = st.columns(2)

    with col1:
        sort_by = st.selectbox("Sort products by", ["Total Revenue", "Revenue per Box", "Boxes Shipped"])
        sort_col = {"Total Revenue": "Total_Revenue", "Revenue per Box": "Rev_per_Box", "Boxes Shipped": "Total_Boxes"}[sort_by]
        prod_sorted = prod_stats.sort_values(sort_col, ascending=True)
        fig = px.bar(prod_sorted, x=sort_col, y="Product",
                     orientation="h",
                     title=f"Products ranked by {sort_by}",
                     color=sort_col,
                     color_continuous_scale=["#f5cc99", "#a0522d", "#3d1f0d"],
                     template=PLOTLY_TEMPLATE)
        prefix = "$" if sort_by != "Boxes Shipped" else ""
        fig.update_layout(xaxis_tickprefix=prefix, xaxis_tickformat=",.0f",
                          coloraxis_showscale=False, height=480,
                          title_font_size=15, margin=dict(t=45, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Bubble: Revenue vs Rev/box, size = transactions
        fig2 = px.scatter(prod_stats, x="Total_Boxes", y="Rev_per_Box",
                          size="Total_Revenue", color="Total_Revenue",
                          hover_name="Product",
                          hover_data={"Total_Revenue": ":$,.0f",
                                      "Rev_per_Box": ":$.2f",
                                      "Total_Boxes": ":,"},
                          title="Product Strategy Map\n(Bubble size = Total Revenue)",
                          color_continuous_scale=["#f5cc99", "#a0522d", "#3d1f0d"],
                          template=PLOTLY_TEMPLATE)
        fig2.update_layout(xaxis_title="Total Boxes Shipped",
                           yaxis_title="Revenue per Box ($)",
                           yaxis_tickprefix="$",
                           coloraxis_showscale=False,
                           height=480, title_font_size=15,
                           margin=dict(t=45, b=10, l=10, r=10))
        # Add product labels
        for _, row in prod_stats.iterrows():
            fig2.add_annotation(x=row["Total_Boxes"], y=row["Rev_per_Box"],
                                text=row["Product"].split()[0],
                                showarrow=False, font=dict(size=9, color="#5a3020"),
                                yshift=12)
        st.plotly_chart(fig2, use_container_width=True)

    # Heatmap: Product × Country revenue
    st.markdown('<div class="section-header">🗺️ Product × Country Revenue Heatmap</div>', unsafe_allow_html=True)
    pivot = df.pivot_table(index="Product", columns="Country", values="Amount", aggfunc="sum").fillna(0)
    fig3 = px.imshow(pivot, color_continuous_scale=["#fdf6f0", "#c8824a", "#3d1f0d"],
                     title="Revenue Heatmap: Product × Country",
                     aspect="auto", template=PLOTLY_TEMPLATE)
    fig3.update_layout(title_font_size=15, height=520,
                       margin=dict(t=45, b=10, l=10, r=10),
                       coloraxis_colorbar=dict(tickprefix="$", tickformat=",.0f"))
    st.plotly_chart(fig3, use_container_width=True)

    # Summary table
    st.markdown('<div class="section-header">📋 Product Summary Table</div>', unsafe_allow_html=True)
    display = prod_stats.sort_values("Total_Revenue", ascending=False).copy()
    display["Total_Revenue"] = display["Total_Revenue"].apply(lambda x: f"${x:,.2f}")
    display["Rev_per_Box"] = display["Rev_per_Box"].apply(lambda x: f"${x:.2f}")
    display["Avg_Deal"] = display["Avg_Deal"].apply(lambda x: f"${x:,.2f}")
    display["Total_Boxes"] = display["Total_Boxes"].apply(lambda x: f"{x:,}")
    display.columns = ["Product", "Total Revenue", "Total Boxes", "Transactions", "Rev / Box", "Avg Deal Size"]
    st.dataframe(display.reset_index(drop=True), use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE: SALESPEOPLE
# ════════════════════════════════════════════════════════════════════════════
elif page == "Salespeople":
    st.markdown('<div class="section-header">👤 Salesperson Performance Analysis</div>', unsafe_allow_html=True)

    df_v = df[df["Boxes Shipped"] > 0].copy()
    sp_stats = (df_v.groupby("Sales Person")
                .agg(Total_Revenue=("Amount", "sum"),
                     Total_Boxes=("Boxes Shipped", "sum"),
                     Transactions=("Amount", "count"))
                .reset_index())
    sp_stats["Rev_per_Box"] = sp_stats["Total_Revenue"] / sp_stats["Total_Boxes"]
    sp_stats["Avg_Deal"] = sp_stats["Total_Revenue"] / sp_stats["Transactions"]

    # Quadrant segmentation
    rev_med = sp_stats["Total_Revenue"].median()
    box_med = sp_stats["Total_Boxes"].median()
    def segment(row):
        hi_rev = row["Total_Revenue"] >= rev_med
        hi_box = row["Total_Boxes"] >= box_med
        if hi_rev and hi_box: return "🟢 All-Rounder"
        if hi_rev: return "🔵 Premium Seller"
        if hi_box: return "🟠 Volume Seller"
        return "🔴 Needs Development"
    sp_stats["Segment"] = sp_stats.apply(segment, axis=1)

    col1, col2 = st.columns([1, 1])

    with col1:
        # Strategy scatter
        seg_colors = {"🟢 All-Rounder": "#27ae60", "🔵 Premium Seller": "#2980b9",
                      "🟠 Volume Seller": "#e67e22", "🔴 Needs Development": "#c0392b"}
        fig = px.scatter(sp_stats, x="Total_Boxes", y="Total_Revenue",
                         color="Segment", size="Rev_per_Box",
                         hover_name="Sales Person",
                         hover_data={"Total_Revenue": ":$,.0f",
                                     "Total_Boxes": ":,",
                                     "Rev_per_Box": ":$.2f",
                                     "Segment": True},
                         color_discrete_map=seg_colors,
                         title="Salesperson Strategy Map",
                         template=PLOTLY_TEMPLATE)
        # Quadrant lines
        fig.add_hline(y=rev_med, line_dash="dot", line_color="gray", line_width=1)
        fig.add_vline(x=box_med, line_dash="dot", line_color="gray", line_width=1)
        # Name labels
        for _, row in sp_stats.iterrows():
            fig.add_annotation(x=row["Total_Boxes"], y=row["Total_Revenue"],
                               text=row["Sales Person"].split()[0],
                               showarrow=False, font=dict(size=8.5), yshift=11)
        fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",.0f",
                          xaxis_title="Total Boxes Shipped",
                          yaxis_title="Total Revenue ($)",
                          legend_title="Segment", height=420,
                          title_font_size=15,
                          margin=dict(t=45, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Rev per box ranking
        sp_sorted = sp_stats.sort_values("Rev_per_Box", ascending=True)
        fig2 = px.bar(sp_sorted, x="Rev_per_Box", y="Sales Person",
                      orientation="h",
                      color="Segment", color_discrete_map=seg_colors,
                      title="Revenue per Box — Efficiency Ranking",
                      template=PLOTLY_TEMPLATE)
        avg_rpb = sp_stats["Rev_per_Box"].mean()
        fig2.add_vline(x=avg_rpb, line_dash="dash", line_color="#3d1f0d",
                       annotation_text=f"Avg ${avg_rpb:.2f}",
                       annotation_position="top right")
        fig2.update_layout(xaxis_tickprefix="$", xaxis_title="Revenue per Box ($)",
                           showlegend=False, height=420, title_font_size=15,
                           margin=dict(t=45, b=10, l=10, r=10))
        st.plotly_chart(fig2, use_container_width=True)

    # Individual drilldown
    st.markdown('<div class="section-header">🔍 Individual Salesperson Drilldown</div>', unsafe_allow_html=True)
    chosen = st.selectbox("Select a salesperson", sorted(df["Sales Person"].unique()))
    sp_df = df[df["Sales Person"] == chosen]

    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Total Revenue", f"${sp_df['Amount'].sum():,.0f}")
    d2.metric("Transactions", f"{len(sp_df):,}")
    d3.metric("Countries", f"{sp_df['Country'].nunique()}")
    d4.metric("Avg Deal", f"${sp_df['Amount'].mean():,.0f}")

    c1, c2 = st.columns(2)
    with c1:
        prod_mix = sp_df.groupby("Product")["Amount"].sum().sort_values(ascending=False).reset_index()
        fig3 = px.pie(prod_mix, names="Product", values="Amount",
                      title=f"{chosen.split()[0]}'s Product Mix",
                      color_discrete_sequence=CHOCO_COLORS, hole=0.4,
                      template=PLOTLY_TEMPLATE)
        fig3.update_layout(height=340, title_font_size=14,
                           margin=dict(t=45, b=10, l=10, r=10))
        st.plotly_chart(fig3, use_container_width=True)

    with c2:
        country_mix = sp_df.groupby("Country")["Amount"].sum().sort_values(ascending=False).reset_index()
        fig4 = px.bar(country_mix, x="Country", y="Amount",
                      title=f"{chosen.split()[0]}'s Revenue by Country",
                      color="Amount", color_continuous_scale=["#f5cc99", "#a0522d", "#3d1f0d"],
                      template=PLOTLY_TEMPLATE)
        fig4.update_layout(yaxis_tickprefix="$", coloraxis_showscale=False,
                           height=340, title_font_size=14,
                           margin=dict(t=45, b=10, l=10, r=10))
        st.plotly_chart(fig4, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE: GEOGRAPHY
# ════════════════════════════════════════════════════════════════════════════
elif page == "Geography":
    st.markdown('<div class="section-header">🌍 Geographic Analysis</div>', unsafe_allow_html=True)

    country_stats = (df.groupby("Country")
                     .agg(Total_Revenue=("Amount", "sum"),
                          Transactions=("Amount", "count"),
                          Avg_Deal=("Amount", "mean"),
                          Total_Boxes=("Boxes Shipped", "sum"))
                     .reset_index()
                     .sort_values("Total_Revenue", ascending=False))
    country_stats["Revenue_Share"] = (country_stats["Total_Revenue"] /
                                       country_stats["Total_Revenue"].sum() * 100).round(1)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(country_stats.sort_values("Total_Revenue", ascending=True),
                     x="Total_Revenue", y="Country", orientation="h",
                     color="Total_Revenue",
                     color_continuous_scale=["#f5cc99", "#a0522d", "#3d1f0d"],
                     title="Total Revenue by Country",
                     text="Revenue_Share",
                     template=PLOTLY_TEMPLATE)
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        fig.update_layout(xaxis_tickprefix="$", xaxis_tickformat=",.0f",
                          coloraxis_showscale=False, height=380,
                          title_font_size=15,
                          margin=dict(t=45, b=10, l=10, r=60))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.pie(country_stats, names="Country", values="Total_Revenue",
                      title="Revenue Market Share",
                      color_discrete_sequence=CHOCO_COLORS, hole=0.42,
                      template=PLOTLY_TEMPLATE)
        fig2.update_traces(textposition="outside", textinfo="percent+label",
                           textfont_size=11)
        fig2.update_layout(showlegend=False, height=380, title_font_size=15,
                           margin=dict(t=45, b=10, l=10, r=10))
        st.plotly_chart(fig2, use_container_width=True)

    # Product preference by country
    st.markdown('<div class="section-header">🍫 Product Preference by Country</div>', unsafe_allow_html=True)

    pivot = df.pivot_table(index="Country", columns="Product", values="Amount",
                           aggfunc="sum").fillna(0)
    # Normalize to % within each country
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100

    fig3 = px.imshow(pivot_pct.round(1),
                     color_continuous_scale=["#fdf6f0", "#c8824a", "#3d1f0d"],
                     title="Product Revenue Share (%) by Country",
                     aspect="auto", template=PLOTLY_TEMPLATE)
    fig3.update_layout(title_font_size=15, height=300,
                       margin=dict(t=45, b=10, l=10, r=10),
                       coloraxis_colorbar=dict(ticksuffix="%"))
    st.plotly_chart(fig3, use_container_width=True)

    # Country summary table
    st.markdown('<div class="section-header">📋 Country Summary</div>', unsafe_allow_html=True)
    disp = country_stats.copy()
    disp["Total_Revenue"] = disp["Total_Revenue"].apply(lambda x: f"${x:,.2f}")
    disp["Avg_Deal"] = disp["Avg_Deal"].apply(lambda x: f"${x:,.2f}")
    disp["Total_Boxes"] = disp["Total_Boxes"].apply(lambda x: f"{x:,}")
    disp["Revenue_Share"] = disp["Revenue_Share"].apply(lambda x: f"{x}%")
    disp.columns = ["Country", "Total Revenue", "Transactions", "Avg Deal", "Boxes Shipped", "Revenue Share"]
    st.dataframe(disp.reset_index(drop=True), use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE: TRENDS
# ════════════════════════════════════════════════════════════════════════════
elif page == "Trends":
    st.markdown('<div class="section-header">📈 Revenue Trend Analysis</div>', unsafe_allow_html=True)

    # Full monthly trend
    monthly = df.groupby("YearMonth")["Amount"].sum().reset_index().sort_values("YearMonth")
    fig = px.line(monthly, x="YearMonth", y="Amount",
                  title="Monthly Revenue — Full Timeline (2022–2024)",
                  color_discrete_sequence=["#a0522d"],
                  markers=True, template=PLOTLY_TEMPLATE)
    fig.update_traces(line_width=2.5, marker_size=5)
    fig.update_layout(xaxis_title="Month", yaxis_title="Revenue ($)",
                      yaxis_tickprefix="$", yaxis_tickformat=",.0f",
                      title_font_size=15, height=320,
                      margin=dict(t=45, b=10, l=10, r=10))
    fig.update_xaxes(tickangle=45, tickfont_size=9)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        # YoY bar — full years only
        yoy = df.groupby("Year")["Amount"].sum().reset_index()
        yoy_full = yoy[yoy["Year"] < 2024].copy()
        if len(yoy_full) >= 2:
            growth = (yoy_full.iloc[-1]["Amount"] - yoy_full.iloc[-2]["Amount"]) / yoy_full.iloc[-2]["Amount"] * 100
        else:
            growth = None

        fig2 = px.bar(yoy, x=yoy["Year"].astype(str), y="Amount",
                      title="Revenue by Year (2024 = Jan–Aug only)",
                      color=yoy["Year"].astype(str),
                      color_discrete_sequence=["#c8824a", "#a0522d", "#3d1f0d"],
                      template=PLOTLY_TEMPLATE, text="Amount")
        fig2.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig2.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",.0f",
                           showlegend=False, title_font_size=15,
                           xaxis_title="Year", yaxis_title="Revenue ($)",
                           height=360, margin=dict(t=45, b=10, l=10, r=10))
        if growth:
            fig2.add_annotation(x=0.5, y=0.92, xref="paper", yref="paper",
                                text=f"YoY Growth (22→23): +{growth:.1f}%",
                                showarrow=False, font=dict(size=12, color="#27ae60"),
                                bgcolor="white", bordercolor="#27ae60", borderwidth=1,
                                borderpad=6)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        # Seasonal pattern (monthly average across all years)
        month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        seasonal = (df.groupby("MonthName")["Amount"].mean()
                    .reindex(month_order).dropna().reset_index())
        peak_month = seasonal.loc[seasonal["Amount"].idxmax(), "MonthName"]
        colors = ["#3d1f0d" if m == peak_month else "#c8824a" for m in seasonal["MonthName"]]
        fig3 = go.Figure(go.Bar(x=seasonal["MonthName"], y=seasonal["Amount"],
                                marker_color=colors,
                                hovertemplate="<b>%{x}</b><br>Avg: $%{y:,.0f}<extra></extra>"))
        fig3.update_layout(title=f"Seasonal Pattern — Avg Revenue by Month<br><sup>Peak: {peak_month}</sup>",
                           xaxis_title="Month", yaxis_title="Avg Revenue ($)",
                           yaxis_tickprefix="$", yaxis_tickformat=",.0f",
                           template=PLOTLY_TEMPLATE, title_font_size=15,
                           height=360, margin=dict(t=55, b=10, l=10, r=10))
        st.plotly_chart(fig3, use_container_width=True)

    # Quarterly breakdown
    st.markdown('<div class="section-header">📅 Quarterly Revenue Breakdown</div>', unsafe_allow_html=True)
    quarterly = (df.groupby(["Year", "Quarter"])["Amount"]
                 .sum().reset_index()
                 .sort_values(["Year", "Quarter"]))
    fig4 = px.bar(quarterly, x="Quarter", y="Amount", color=quarterly["Year"].astype(str),
                  barmode="group",
                  color_discrete_sequence=["#c8824a", "#a0522d", "#3d1f0d"],
                  title="Quarterly Revenue by Year",
                  template=PLOTLY_TEMPLATE)
    fig4.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",.0f",
                       legend_title="Year", title_font_size=15,
                       height=360, margin=dict(t=45, b=10, l=10, r=10))
    st.plotly_chart(fig4, use_container_width=True)

    # Rolling 3-month average
    monthly_roll = monthly.copy()
    monthly_roll["Rolling_3M"] = monthly_roll["Amount"].rolling(3, min_periods=1).mean()
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(x=monthly_roll["YearMonth"], y=monthly_roll["Amount"],
                          name="Monthly Revenue", marker_color="#e6a96a", opacity=0.7))
    fig5.add_trace(go.Scatter(x=monthly_roll["YearMonth"], y=monthly_roll["Rolling_3M"],
                              name="3-Month Rolling Avg", line=dict(color="#3d1f0d", width=2.5),
                              mode="lines"))
    fig5.update_layout(title="Monthly Revenue with 3-Month Rolling Average",
                       xaxis_title="Month", yaxis_title="Revenue ($)",
                       yaxis_tickprefix="$", yaxis_tickformat=",.0f",
                       template=PLOTLY_TEMPLATE, title_font_size=15,
                       legend=dict(orientation="h", y=1.08),
                       height=340, margin=dict(t=55, b=10, l=10, r=10))
    fig5.update_xaxes(tickangle=45, tickfont_size=9)
    st.plotly_chart(fig5, use_container_width=True)
