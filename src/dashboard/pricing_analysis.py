# src/pricing_analysis.py
import pandas as pd


# --- Precio justo por capacidad (percentiles) ---
def fair_price_range(storage_lt, df):
    """Dado capacidad en litros, retorna rango competitivo de precio"""
    margin = 30  # litros de tolerancia
    subset = df[
        (df["storage_lt"] >= storage_lt - margin) &
        (df["storage_lt"] <= storage_lt + margin) &
        (df["price"].notna())
    ]["price"]
    if len(subset) < 5:
        return None
    return {
        "p25": int(subset.quantile(0.25)),
        "p50": int(subset.quantile(0.50)),
        "p75": int(subset.quantile(0.75)),
        "n": len(subset)
    }

# --- Price recommendation for a specific refrigerator ---
def price_recommendation(brand, capacity_liters, retailer, df):
    """Recommends whether the price is well positioned"""
    
    fridge_price = df[
        (df["brand"] == brand) &
        (df["seller"] == retailer) &
        (df["storage_lt"].between(capacity_liters - 30, capacity_liters + 30))
    ]["price"].median()

    market_range = fair_price_range(capacity_liters, df)
    
    if not market_range or pd.isna(fridge_price):
        return "Insufficient data"

    p50 = market_range["p50"]
    diff_pct = (fridge_price - p50) / p50 * 100

    if diff_pct > 15:
        return f"⚠️ {brand} at {retailer} is {diff_pct:.1f}% above market for {capacity_liters}L"
    elif diff_pct < -15:
        return f"✅ {brand} at {retailer} is {abs(diff_pct):.1f}% below market — competitive advantage"
    else:
        return f"✓ {brand} at {retailer} is competitively priced for {capacity_liters}L"