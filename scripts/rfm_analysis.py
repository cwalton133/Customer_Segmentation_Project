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

# Step 3: Create Monetary Score
rfm["M_Score"] = pd.qcut(
    rfm["Monetary"],
    5,
    labels=[1,2,3,4,5]
)

# Step 4: Convert Scores to Integers
# =========================
# RFM SCORING
# =========================

# Recency
rfm["R_Score"] = pd.qcut(
    rfm["Recency"],
    q=5,
    labels=[5, 4, 3, 2, 1]
)

# Frequency
rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    q=5,
    labels=[1, 2, 3, 4, 5]
)

# Monetary
rfm["M_Score"] = pd.qcut(
    rfm["Monetary"],
    q=5,
    labels=[1, 2, 3, 4, 5]
)

print(rfm.columns)

# Convert to integers
rfm["R_Score"] = rfm["R_Score"].astype(int)
rfm["F_Score"] = rfm["F_Score"].astype(int)
rfm["M_Score"] = rfm["M_Score"].astype(int)

# Step 3: Verify Scores Were Created
print(
    rfm[
        [
            "Recency",
            "Frequency",
            "Monetary",
            "R_Score",
            "F_Score",
            "M_Score"
        ]
    ].head()
)

# Then
def segment_customer(score):

    if score >= 13:
        return "Champions"

    elif score >= 10:
        return "Loyal Customers"

    elif score >= 7:
        return "Potential Loyalists"

    elif score >= 5:
        return "At Risk"

    else:
        return "Lost Customers"

# Better Segmentation
rfm["RFM_Total"] = (
    rfm["R_Score"] +
    rfm["F_Score"] +
    rfm["M_Score"]
)

# Next
rfm["Segment"] = rfm["RFM_Total"].apply(
    segment_customer
)

# Create Total RFM Score
rfm["RFM_Total"] = (
    rfm["R_Score"]
    + rfm["F_Score"]
    + rfm["M_Score"]
)

# Create Segment Logic
def segment_customer(score):

    if score >= 13:
        return "Champions"

    elif score >= 10:
        return "Loyal Customers"

    elif score >= 7:
        return "Potential Loyalists"

    elif score >= 5:
        return "At Risk"

    else:
        return "Lost Customers"
    
    # Apply it
    rfm["Segment"] = (
        rfm["RFM_Total"]
        .apply(segment_customer)
    )
    
    ## Apply 
    
    # =====================================
# CREATE RFM TOTAL
# =====================================

rfm["RFM_Total"] = (
    rfm["R_Score"]
    + rfm["F_Score"]
    + rfm["M_Score"]
)

# =====================================
# CUSTOMER SEGMENT FUNCTION
# =====================================

def segment_customer(score):

    if score >= 13:
        return "Champions"

    elif score >= 10:
        return "Loyal Customers"

    elif score >= 7:
        return "Potential Loyalists"

    elif score >= 5:
        return "At Risk"

    else:
        return "Lost Customers"


# =====================================
# APPLY SEGMENTS
# =====================================

rfm["Segment"] = rfm["RFM_Total"].apply(
    segment_customer
)

# =====================================
# SEGMENT SUMMARY
# =====================================

segment_summary = (
    rfm["Segment"]
    .value_counts()
)

print("\n=== CUSTOMER SEGMENTS ===")
print(segment_summary)

# =====================================
# REVENUE BY SEGMENT
# =====================================

segment_revenue = (
    rfm.groupby("Segment")["Monetary"]
       .sum()
       .sort_values(ascending=False)
)

print("\n=== REVENUE BY SEGMENT ===")
print(segment_revenue)

# =====================================
# SAVE FINAL DATASET
# =====================================

rfm.to_csv(
    "data/final/customer_segments_final.csv",
    index=False
)

print("\nFinal dataset saved.")