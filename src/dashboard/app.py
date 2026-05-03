# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
import os
from dashboard.pricing_analysis import fair_price_range, price_recommendation

st.set_page_config(
    page_title="Pricing Intelligence — Refrigerators Colombia",
    page_icon="🧊", layout="wide"
)

@st.cache_data(ttl=600)
def load_data():
    try:
        conn = psycopg2.connect(
            host=os.environ.get("POSTGRES_SERVER", "localhost"),
            database=os.environ.get("POSTGRES_DB", "your_db"),
            user=os.environ.get("DB_USER", "postgres"),
            password=os.environ.get("POSTGRES_PASSWORD", "your_password")
        )
        df = pd.read_sql("SELECT * FROM fridges_clean", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()

df = load_data()

# --- Header ---
st.title("🧊 Pricing Intelligence — Refrigerators Colombia")
st.caption("Competitive pricing analysis across Éxito, Falabella, Alkosto, and Sodimac")

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Products analyzed", len(df))
col2.metric("Median market price",
            f"${df['price'].median():,.0f}")
col3.metric("Minimum price",
            f"${df['price'].min():,.0f}")
col4.metric("Maximum price",
            f"${df['price'].max():,.0f}")

st.divider()

# --- Row 1: Distribution and competitive positioning ---
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Price distribution by seller")
    fig1 = px.box(
        df.dropna(subset=["price", "seller"]),
        x="seller", y="price", color="seller",
        labels={"price": "Price (COP)", "seller": "Retailer"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig1.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("💡 Insight: The most expensive retailer does not always have a premium catalog — it may indicate pricing inefficiency.")

with col_b:
    st.subheader("Average price by brand")
    brand_avg = (df.groupby("brand")["price"]
                 .median().sort_values(ascending=True)
                 .reset_index())
    fig2 = px.bar(
        brand_avg, x="price", y="brand",
        orientation="h", color="price",
        color_continuous_scale="Blues",
        labels={"price": "Median price (COP)", "brand": "Brand"}
    )
    fig2.update_layout(height=350, coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

# --- Row 2: Price per liter and segments ---
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Price per liter — true value by capacity")

    filtered_df = df[
        (df["storage_lt"] > 1) &
        df["storage_lt"].notna() &
        df["price"].notna() &
        df["brand"].notna()
    ]

    fig3 = px.scatter(
        filtered_df,
        x="storage_lt", y="price", color="brand",
        size="price_per_liter", hover_data=["seller", "product"],
        labels={
            "storage_lt": "Capacity (liters)",
            "price": "Price (COP)",
            "brand": "Brand"
        },
        trendline="ols"
    )
    fig3.update_layout(height=380)
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("💡 Points above the line = overpriced relative to capacity.")

with col_d:
    st.subheader("Price segment share")
    seg_counts = df["segment"].value_counts().reset_index()
    fig4 = px.pie(
        seg_counts, names="segment", values="count",
        color_discrete_map={
            "Económico": "#6BCB77",
            "Mid-range": "#4D96FF",
            "Premium": "#FF6B6B"
        }
    )
    fig4.update_layout(height=380)
    st.plotly_chart(fig4, use_container_width=True)

# --- Row 3: Price recommender ---
st.divider()
st.subheader("🎯 Competitive price recommender")
st.caption("Select a brand, capacity, and retailer to evaluate pricing positioning")

rc1, rc2, rc3 = st.columns(3)
brand_sel = rc1.selectbox("Brand", sorted(df["brand"].dropna().unique()))
storage_sel = rc2.slider(
    "Capacity (liters)",
    int(df["storage_lt"].min() or 100),
    int(1000),
    300, step=10
)
seller_sel = rc3.selectbox("Retailer", sorted(df["seller"].dropna().unique()))

recommendation = price_recommendation(brand_sel, storage_sel, seller_sel, df)
market = fair_price_range(storage_sel, df)

st.info(recommendation)

if market:
    m1, m2, m3 = st.columns(3)
    m1.metric("Low market price", f"${market['p25']:,}")
    m2.metric("Median market price", f"${market['p50']:,}")
    m3.metric("High market price", f"${market['p75']:,}")