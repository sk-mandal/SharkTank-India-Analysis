# ---------------------------------------------------------
# SHARK TANK INDIA — FINAL DATA CLEANING SCRIPT
# ---------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel("EDA_Shark_Tank_India.xlsx")

raw_df = df.copy()

# Clean Column Names
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Removing Duplicates
df = df.drop_duplicates()


# 4. Handling Missing Values
missing_summary = df.isnull().sum()

# Find columns that contain numeric values stored as text.
numeric_like_cols = [
    col for col in df.columns
    if any(key in col for key in ["amount", "valuation", "equity", "ask", "deal"])
]

for col in numeric_like_cols:
    # Removing symbols like ₹, %, commas
    df[col] = (
        df[col]
        .astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "")
        .str.replace("%", "")
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")

# # Converting all deal values to 0/1.
if "deal" in df.columns:
    df["deal_flag"] = pd.to_numeric(df["deal"], errors="coerce").fillna(0).astype(int)
else:
    df["deal_flag"] = np.where(df["deal_amount"].notnull(), 1, 0)

print("CLEANING DONE!")
print(df.head())

# Count total pitches
total_pitches = len(df)

# Count successful deals
successful_deals = df["deal_flag"].sum()

# Percentage
deal_percentage = round((successful_deals / total_pitches) * 100, 2)
print("Total Pitches:", total_pitches)
print("Successful Deals:", successful_deals)
print("Percentage of Deals:", deal_percentage, "%")

# Filter only those rows where a deal actually happened
deals_df = df[df["deal_flag"] == 1]

# Calculate average & median deal amount
average_deal_amount = deals_df["deal_amount"].mean()
median_deal_amount = deals_df["deal_amount"].median()
print("Average Deal Amount:", round(average_deal_amount, 2))
print("Median Deal Amount:", round(median_deal_amount, 2))

# Identify shark deal columns (columns ending with "_deal")
shark_cols = [col for col in df.columns if col.endswith("_deal")]

# Sum investments for each shark
shark_investments = df[shark_cols].sum().sort_values(ascending=False)

# Top 3 sharks
top_3 = shark_investments.head(3)
print("Investments by each shark:\n")
print(shark_investments)
print("\nTop 3 Sharks:")
print(top_3)

plt.figure(figsize=(8,5))
top_3.plot(kind="bar")
plt.title("Top 3 Sharks by Number of Investments")
plt.xlabel("Shark")
plt.ylabel("Number of Deals")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

total_amount_invested = df[df["deal_flag"] == 1]["deal_amount"].sum()
print("Total Amount Invested in the Season:", total_amount_invested)

deal_equity = df[df["deal_flag"] == 1]["deal_equity"]
print(deal_equity.describe())

plt.figure(figsize=(6,4))
plt.boxplot(deal_equity.dropna())
plt.title("Deal Equity Distribution")
plt.ylabel("Equity (%)")
plt.show()

correlation = df["deal_valuation"].corr(df["ask_valuation"])
print("Correlation between Ask Valuation and Deal Valuation:", correlation)


# Only consider deals where deal_flag = 1
equity_given = df[df["deal_flag"] == 1]["deal_equity"]

average_equity_given = equity_given.mean()
print("Average Equity Given per Deal:", round(average_equity_given, 2), "%")

# Count deals per episode
episode_deals = df[df["deal_flag"] == 1].groupby("episode_number")["deal_flag"].count()

highest_episode = episode_deals.idxmax()
highest_deals = episode_deals.max()
print("Episode with highest deals:", highest_episode)
print("Number of deals in that episode:", highest_deals)

plt.figure(figsize=(8,4))
episode_deals.plot(kind="bar")
plt.title("Number of Deals per Episode")
plt.xlabel("Episode Number")
plt.ylabel("Total Deals")
plt.tight_layout()
plt.show()

# Filter pitches asking for more than 1 Crore (1 Crore = 10000000)
high_ask_df = df[df["pitcher_ask_amount"] > 10000000]

total_high_ask = len(high_ask_df)
high_ask_and_deal = high_ask_df["deal_flag"].sum()
print("Total pitches asking > 1 Crore:", total_high_ask)
print("Those pitches that received investment:", high_ask_and_deal)

# Detect shark-deal columns automatically
shark_deal_cols = [col for col in df.columns if col.endswith("_deal")]

# Sum shark participation per pitch
df["sharks_invested_count"] = df[shark_deal_cols].sum(axis=1)

# Pitches with >1 shark investing
multi_shark_pitches = df[df["sharks_invested_count"] > 1]

total_multi_shark = len(multi_shark_pitches)
percentage_multi = round((total_multi_shark / len(df)) * 100, 2)
print("Pitches with more than one shark:", total_multi_shark)
print("Percentage of total pitches:", percentage_multi, "%")

# For each shark, multiply deal_amount by their deal flag
ashneer_total = (df["ashneer_deal"] * df["deal_amount"]).sum()
peyush_total = (df["peyush_deal"] * df["deal_amount"]).sum()
print("Total Amount Invested by Ashneer Grover:", ashneer_total)
print("Total Amount Invested by Peyush Bansal:", peyush_total)

amount_per_shark = df["amount_per_shark"].dropna()
print(amount_per_shark.describe())

plt.figure(figsize=(6,4))
plt.boxplot(amount_per_shark)
plt.title("Distribution of Amount Per Shark")
plt.ylabel("Amount (₹)")
plt.tight_layout()
plt.show()

# Filter rows where deal amount is greater than what pitcher asked
higher_deal_df = df[df["deal_amount"] > df["pitcher_ask_amount"]]
print("Number of cases where deal amount > ask amount:", len(higher_deal_df))

if len(higher_deal_df) > 0:
    print("\nDetails of such cases:")
    display_columns = ["episode_number", "pitch_number", "brand_name", 
                       "pitcher_ask_amount", "deal_amount"]
    existing_cols = [c for c in display_columns if c in df.columns]
    print(higher_deal_df[existing_cols].to_string(index=False))

roi_results = {}
# Loop through each shark
for shark in [col.replace("_deal", "") for col in df.columns if col.endswith("_deal")]:
    deal_flag_col = f"{shark}_deal"
    
    # For deals the shark participated in:
    shark_deals = df[df[deal_flag_col] == 1]
    
    if len(shark_deals) > 0:
        # ROI = total equity received / total amount invested
        total_equity = shark_deals["deal_equity"].sum()
        total_amount = shark_deals["deal_amount"].sum()
        
        roi = total_equity / total_amount if total_amount > 0 else 0
        roi_results[shark] = roi

# Sort sharks by ROI
roi_sorted = dict(sorted(roi_results.items(), key=lambda x: x[1], reverse=True))
print("Shark ROI Rankings (Higher is better):")
for name, roi_value in roi_sorted.items():
    print(f"{name}: {roi_value:.6f}")

# Only consider successful deals
equity_trend = df[df["deal_flag"] == 1].groupby("episode_number")["deal_equity"].mean()
print("Average equity per episode:")
print(equity_trend)

plt.figure(figsize=(8,4))
equity_trend.plot(marker="o")
plt.title("Episode-wise Average Deal Equity")
plt.xlabel("Episode Number")
plt.ylabel("Average Equity (%)")
plt.grid(True)
plt.tight_layout()
plt.show()

# Correlation between ask amount and final deal amount
correlation = df["pitcher_ask_amount"].corr(df["deal_amount"])

# Compare asks: deals vs no deals
ask_with_deal = df[df["deal_flag"] == 1]["pitcher_ask_amount"].mean()
ask_without_deal = df[df["deal_flag"] == 0]["pitcher_ask_amount"].mean()
print("Correlation between Ask Amount and Deal Amount:", correlation)
print("Average Ask Amount (Deals Won):", round(ask_with_deal, 2))
print("Average Ask Amount (No Deal):", round(ask_without_deal, 2))

if ask_with_deal < ask_without_deal:
    print("\nInsight: Startups asking for LOWER amounts tend to secure more deals.")
else:
    print("\nInsight: Asking amount does NOT show a clear pattern toward deal success.")

episode_wise_deals = df.groupby("episode_number")["deal_flag"].sum()
print("Deals per Episode:")
print(episode_wise_deals)

plt.figure(figsize=(8,4))
episode_wise_deals.plot(kind="line", marker="o")
plt.title("Episode-wise Deal Closures")
plt.xlabel("Episode Number")
plt.ylabel("Number of Deals")
plt.grid(True)
plt.tight_layout()
plt.show()

# Correlation between equity asked and final deal valuation
equity_valuation_corr = df["ask_equity"].corr(df["deal_valuation"])

# Compare groups (equity <= 10% vs > 10%)
low_equity = df[df["ask_equity"] <= 10]["deal_valuation"].mean()
high_equity = df[df["ask_equity"] > 10]["deal_valuation"].mean()
print("Correlation between Ask Equity and Deal Valuation:", equity_valuation_corr)
print("Avg Deal Valuation (Low Equity <= 10%):", round(low_equity, 2))
print("Avg Deal Valuation (High Equity > 10%):", round(high_equity, 2))

if low_equity > high_equity:
    print("\nInsight: Lower equity asks tend to result in HIGHER deal valuations.")
else:
    print("\nInsight: Higher equity asks do NOT necessarily result in lower valuations.")
