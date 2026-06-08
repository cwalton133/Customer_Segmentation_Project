#Step 2: Load Clean Datasetclear
import pandas as pd

df = pd.read_csv(
    "data/cleaned/online_retail_clean.csv"
)

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"]
)

print(df.shape)

# Step 3: Find Analysis Date
print(df["InvoiceDate"].max())

# Step 4: Create Snapshot Date
snapshot_date = (
    df["InvoiceDate"].max()
    + pd.Timedelta(days=1)
)

print(snapshot_date)

#Step 5: Build Customer-Level Metrics
rfm = df.groupby("CustomerID").agg({
    "InvoiceDate": lambda x: (
        snapshot_date - x.max()
    ).days,

    "InvoiceNo": "nunique",

    "Revenue": "sum"
})

# Step 6: Renaming columns
rfm.columns = [
    "Recency",
    "Frequency",
    "Monetary"
]

rfm.reset_index(inplace=True)

print(rfm.head())

# Step 7: Explore RFM Metrics
print("\n=== RFM SUMMARY ===")
print(rfm.describe())

#Step 7: Save RFM Dataset
rfm.to_csv(
    "data/rfm/customer_rfm.csv",
    index=False
)

print("RFM dataset saved.")

# Showing RFM Header and description
print(rfm.head())

print(rfm.describe())

# Step 8: Create R Score
rfm["R_Score"] = pd.qcut(
    rfm["Recency"],
    5,
    labels=[5,4,3,2,1]
)