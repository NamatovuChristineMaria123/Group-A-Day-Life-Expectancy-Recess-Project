# ==============================
# 📂 TASK 1: Data Exploration
# ==============================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset
df = pd.read_csv("Life_Expectancy_Data.csv")

# Basic shape
print("Shape of dataset:", df.shape)

# Display first 5 rows
print("\nFirst 5 rows:\n", df.head())

# General info
print("\nInfo:\n")
df.info()

# Missing values count per column
missing_counts = df.isnull().sum()
print("\nMissing Values:\n", missing_counts)

# Percentage missing
missing_percent = df.isnull().mean() * 100
print("\nMissing Percentage:\n", missing_percent)

# Visualize missing data with a heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
plt.title("Heatmap of Missing Values")
plt.show()
# A thorough exploration of the Life Expectancy dataset revealed no missing values across all 22 features. Therefore, no imputation or removal of missing data is required for this dataset
# Task 2:

# “Upon exploration, it was found that there are no missing values in the dataset. As a result, there is no need to apply imputation or removal. This ensures the integrity and completeness of the dataset for further analysis.”

# Task 3:

# “Since no missing data was present, no imputation method was applied. Therefore, the dataset remains unchanged, maintaining its original size and quality.”

# ✅ Deliverables for Task 2 & 3:

# Screenshot of your terminal output (like what you pasted)

# Screenshot of the heatmap of missing data (it should appear fully filled — i.e., no missing gaps)