# clean_ecommerce.py
# Beginner-friendly CSV cleaning script

import os, sys, re
import pandas as pd
import numpy as np

IN_PATH = 'ecommerce_furniture_dataset_2024.csv'
OUT_PATH = 'ecommerce_furniture_dataset_2024_cleaned.csv'

def clean_price(x):
    """Turn messy price strings into floats (remove $, commas, extra dots)."""
    if pd.isna(x):
        return np.nan
    s = str(x).replace('\n',' ').replace('\r',' ').replace('$','').replace(',','').strip()
    s = re.sub(r'[^0-9.]', '', s)
    if s == '':
        return np.nan
    parts = s.split('.')
    if len(parts) == 1:
        try: return float(parts[0])
        except: return np.nan
    whole = parts[0] if parts[0] != '' else '0'
    frac = ''.join(parts[1:])  # join extra dots into fractional part
    try:
        return float(whole + '.' + frac)
    except:
        return np.nan

def map_col(c):
    """Simple column renaming: productTitle, price, originalPrice, sold, tagText."""
    key = str(c).lower().replace(' ','').replace('_','').replace('.','')
    if 'product' in key or 'title' in key:
        return 'productTitle'
    if 'original' in key and 'price' in key:
        return 'originalPrice'
    if 'price' in key and 'original' not in key:
        return 'price'
    if 'sold' in key:
        return 'sold'
    if 'tag' in key or 'shipping' in key:
        return 'tagText'
    return str(c)

def consolidate_tag(x):
    """Group shipping tags into simple categories."""
    if pd.isna(x):
        return 'Unknown'
    x = str(x).strip()
    if x == 'Free shipping':
        return 'Free shipping'
    if x.startswith('+Shipping:'):
        return x
    return 'others'

def main():
    if not os.path.exists(IN_PATH):
        print(f"ERROR: File not found in this folder: {IN_PATH}")
        sys.exit(1)

    # Try reading CSV (fallback to latin1 if needed)
    try:
        df = pd.read_csv(IN_PATH, low_memory=False)
    except Exception as e:
        print("Normal read failed; retrying with latin1 encoding...", e)
        df = pd.read_csv(IN_PATH, encoding='latin1', low_memory=False)

    print("Original rows:", len(df))
    # Normalize column names
    df.columns = [map_col(c) for c in df.columns]

    # Clean price columns
    if 'price' in df.columns:
        df['price'] = df['price'].apply(clean_price)
    if 'originalPrice' in df.columns:
        df['originalPrice'] = df['originalPrice'].apply(clean_price)

    # Clean 'sold' -> numeric
    if 'sold' in df.columns:
        df['sold'] = pd.to_numeric(df['sold'].astype(str).str.replace(r'[^0-9-]', '', regex=True), errors='coerce')
    else:
        df['sold'] = np.nan

    # discount percent if originalPrice present
    if 'originalPrice' in df.columns:
        df['discount_pct'] = np.where(
            df['originalPrice'].notna() & (df['originalPrice'] > 0),
            ((df['originalPrice'] - df['price']) / df['originalPrice']) * 100,
            np.nan
        )
    else:
        df['discount_pct'] = np.nan

    # Consolidate tagText
    df['tagText'] = df.get('tagText', pd.Series([np.nan]*len(df))).apply(consolidate_tag)

    # Remove duplicates and save
    df_clean = df.drop_duplicates().reset_index(drop=True)
    print("Cleaned rows (after dropping duplicates):", len(df_clean))
    df_clean.to_csv(OUT_PATH, index=False)
    print("Saved cleaned CSV to:", OUT_PATH)
    print("\nPreview (first 5 rows):")
    print(df_clean.head().to_string())

if __name__ == '__main__':
    main()
