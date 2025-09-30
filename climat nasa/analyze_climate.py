import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === 1. Load the cleaned dataset ===
df = pd.read_csv("climate_nasa_cleaned.csv", parse_dates=["date"])

# === 2. Pie chart: distribution of comments availability ===
if "commentscount" in df.columns:
    # counts of rows with and without comments
    has_comments = df["commentscount"].notna().sum()
    no_comments = df["commentscount"].isna().sum()

    plt.figure(figsize=(5,5))
    plt.pie([has_comments, no_comments],
            labels=["With Comments", "No Comments"],
            autopct="%1.1f%%",
            startangle=90,
            colors=["#66b3ff","#ff9999"])
    plt.title("Comments Availability")
    plt.show()

# === 3. Line plot: likes over time ===
if "date" in df.columns and "likescount" in df.columns:
    plt.figure(figsize=(10,5))
    plt.plot(df["date"], df["likescount"], color="blue", alpha=0.7)
    plt.xlabel("Date")
    plt.ylabel("Likes Count")
    plt.title("Likes Trend Over Time")
    plt.tight_layout()
    plt.show()

# === 4. Correlation heatmap ===
num_df = df.select_dtypes(include=["number"])
if not num_df.empty:
    plt.figure(figsize=(8,6))
    sns.heatmap(num_df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.show()
