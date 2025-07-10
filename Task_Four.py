import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


df = pd.read_csv("Life_Expectancy_Data.csv")

# Remove leading/trailing spaces from column names
df.columns = df.columns.str.strip()

# Drop non-numeric columns
numeric_df = df.select_dtypes(include=[np.number])

# Correlation matrix
corr_matrix = numeric_df.corr()

# Correlation with Life expectancy
life_corr = corr_matrix["Life expectancy"].sort_values(ascending=False)
print("\nCorrelation with Life Expectancy:\n", life_corr)

# Top correlated features (excluding self-correlation)
top_features = life_corr.index[1:11]

# Plot heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(numeric_df[top_features].corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap of Top Features")
plt.show()
