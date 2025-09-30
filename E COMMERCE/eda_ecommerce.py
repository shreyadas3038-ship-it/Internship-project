# eda_ecommerce.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned CSV
df = pd.read_csv("ecommerce_furniture_dataset_2024_cleaned.csv")

print("Dataset shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())

# --- Example 1: Price distribution ---
plt.figure(figsize=(8,5))
sns.histplot(df['price'], bins=50, kde=True)
plt.title("Price Distribution")
plt.xlabel("Price")
plt.ylabel("Count")
plt.show()

# --- Example 2: Top 10 most sold products ---
top10 = df.groupby("productTitle")['sold'].sum().sort_values(ascending=False).head(10)
print("\nTop 10 products by units sold:\n", top10)

plt.figure(figsize=(10,5))
top10.plot(kind='bar')
plt.title("Top 10 Products by Units Sold")
plt.xlabel("Product Title")
plt.ylabel("Units Sold")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# --- Example 3: Free shipping vs Paid shipping ---
shipping_summary = df.groupby("tagText")['sold'].sum().sort_values(ascending=False)
print("\nSales by Shipping Type:\n", shipping_summary)

plt.figure(figsize=(6,4))
shipping_summary.plot(kind='bar', color='teal')
plt.title("Units Sold by Shipping Type")
plt.ylabel("Units Sold")
plt.xticks(rotation=0)
plt.show()

# --- Example 4: Discounts effect ---
plt.figure(figsize=(8,5))
sns.scatterplot(x='discount_pct', y='sold', data=df, alpha=0.5)
plt.title("Discount % vs Units Sold")
plt.xlabel("Discount Percentage")
plt.ylabel("Units Sold")
plt.show()
