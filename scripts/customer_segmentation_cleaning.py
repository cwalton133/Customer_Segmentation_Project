# Step 1: Cleaning_Feature_Engineering
import pandas as pd

df = pd.read_excel(
    "data/raw/online_retail.xlsx"
)

print(df.shape)
print(df.head())
print(df.info())

# Step 2: Data Quality Assessment
print("\n=== Missing Values ===")
print(df.isnull().sum())

print("\n=== Duplicate Rows ===")
print(df.duplicated().sum())

print("\n=== Dataset Shape ===")
print(df.shape)

# Step 3: Create a Data Cleaning Section
# =========================
# DATA CLEANING
# =========================

print("\n=== STARTING CLEANING ===")

# Remove missing Customer IDs
df = df.dropna(subset=["CustomerID"])

print("After removing missing Customer IDs:")
print(df.shape)

# Remove cancelled orders
df = df[
    ~df["InvoiceNo"].astype(str).str.startswith("C")
]

print("After removing cancellations:")
print(df.shape)

# Remove negative quantities
df = df[df["Quantity"] > 0]

print("After removing negative quantities:")
print(df.shape)

# Remove invalid prices
df = df[df["UnitPrice"] > 0]

print("After removing zero or negative prices:")
print(df.shape)

# Remove duplicates
df = df.drop_duplicates()

print("After removing duplicates:")
print(df.shape)

# Create Revenue column
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

print("\nRevenue column created.")

#Step 5: Then Run This Summary
print("\n=== BUSINESS SUMMARY ===")

print("Transactions:", len(df))
print("Customers:", df["CustomerID"].nunique())
print("Orders:", df["InvoiceNo"].nunique())
print("Countries:", df["Country"].nunique())

print(
    "Total Revenue: £{:,.2f}".format(
        df["Revenue"].sum()
    )
)

# Step 6: Save the Clean Dataset
df.to_csv(
    "data/cleaned/online_retail_clean.csv",
    index=False
)

print("\nClean dataset saved successfully.")
