import pandas as pd
import numpy as np

print(" Starting Data Cleaning Process...\n")

# ============= CLEAN HEALTH CAMPAIGN DATA =============
print("1️ Cleaning Health Campaign Data...")
health_campaign = pd.read_csv('Health_Campaign_Dataset_50.csv')

print(f"   Original rows: {len(health_campaign)}")

# Remove duplicates
health_campaign = health_campaign.drop_duplicates()

# Remove rows with missing critical values
health_campaign = health_campaign.dropna(subset=['Campaign Name', 'Channel'])

# Fill missing numeric values with median
numeric_cols = ['Impressions', 'Engagements', 'Behavior Change (%)', 'Feedback Score']
for col in numeric_cols:
    if col in health_campaign.columns:
        health_campaign[col].fillna(health_campaign[col].median(), inplace=True)

# Remove outliers (values beyond 3 standard deviations)
for col in numeric_cols:
    if col in health_campaign.columns:
        mean = health_campaign[col].mean()
        std = health_campaign[col].std()
        health_campaign = health_campaign[
            (health_campaign[col] >= mean - 3*std) & 
            (health_campaign[col] <= mean + 3*std)
        ]

print(f"   Cleaned rows: {len(health_campaign)}")
health_campaign.to_csv('Health_Campaign_Dataset_50_cleaned.csv', index=False)
print("    Saved: Health_Campaign_Dataset_50_cleaned.csv\n")


# ============= CLEAN DISABILITY DISTRICT DATA =============
print("2️⃣ Cleaning Disability District Data...")
disability_district = pd.read_csv('HH_Disability_District.csv')

print(f"   Original rows: {len(disability_district)}")

# Remove duplicates
disability_district = disability_district.drop_duplicates()

# Remove rows with missing location data
disability_district = disability_district.dropna(subset=['State', 'District'])

# Fill missing numeric values with 0
numeric_cols = disability_district.select_dtypes(include=[np.number]).columns
disability_district[numeric_cols] = disability_district[numeric_cols].fillna(0)

print(f"   Cleaned rows: {len(disability_district)}")
disability_district.to_csv('HH_Disability_District_cleaned.csv', index=False)
print("   ✅ Saved: HH_Disability_District_cleaned.csv\n")


# ============= CLEAN DISABILITY STATE DATA =============
print("3️⃣ Cleaning Disability State Data...")
disability_state = pd.read_csv('HH_Disability_State.csv')

print(f"   Original rows: {len(disability_state)}")

# Remove duplicates
disability_state = disability_state.drop_duplicates()

# Remove rows with missing state data
disability_state = disability_state.dropna(subset=['State'])

# Fill missing numeric values with 0
numeric_cols = disability_state.select_dtypes(include=[np.number]).columns
disability_state[numeric_cols] = disability_state[numeric_cols].fillna(0)

print(f"   Cleaned rows: {len(disability_state)}")
disability_state.to_csv('HH_Disability_State_cleaned.csv', index=False)
print("   ✅ Saved: HH_Disability_State_cleaned.csv\n")


# ============= CLEAN AWARENESS DATA =============
print("4️⃣ Cleaning Awareness Data...")
awareness = pd.read_csv('XX_Awareness_On_HIV_AIDS_RTI_STI_HAF_ORS_ORT_ZINC_And_ARI_Pneumonia_District.csv')

print(f"   Original rows: {len(awareness)}")

# Remove duplicates
awareness = awareness.drop_duplicates()

# Remove rows with missing location data
awareness = awareness.dropna(subset=['State', 'District'])

# Fill missing numeric values with median
numeric_cols = awareness.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    awareness[col].fillna(awareness[col].median(), inplace=True)

print(f"   Cleaned rows: {len(awareness)}")
awareness.to_csv('XX_Awareness_cleaned.csv', index=False)
print("   ✅ Saved: XX_Awareness_cleaned.csv\n")


# ============= SUMMARY REPORT =============
print("=" * 50)
print("📊 DATA CLEANING SUMMARY")
print("=" * 50)
print(f"✅ All datasets cleaned successfully!")
print(f"📁 4 new cleaned CSV files created")
print(f"🗑️  Removed: Duplicates, Missing values, Outliers")
print("=" * 50)