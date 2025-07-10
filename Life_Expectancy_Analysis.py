==
# TASK 1:Data Exploration


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("Life_Expectancy_Data.csv")

hape
print("Shape of dataset:", df.shape)


print("\nFirst 5 rows:\n", df.head())


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
