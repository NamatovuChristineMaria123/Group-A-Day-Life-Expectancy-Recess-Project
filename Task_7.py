
#  TASK 7 & 8: Visualizations


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("Life_Expectancy_Engineered.csv")
df.columns = df.columns.str.strip()

# 1️⃣ Scatter plot: Life Expectancy vs GDP
plt.figure(figsize=(8, 6))
sns.scatterplot(x='GDP', y='Life expectancy', data=df)
plt.title("Life Expectancy vs GDP")
plt.savefig("scatter_lifeexp_gdp.png")
plt.show()

# 2️⃣ Scatter plot: Life Expectancy vs Schooling
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Schooling', y='Life expectancy', data=df)
plt.title("Life Expectancy vs Schooling")
plt.savefig("scatter_lifeexp_schooling.png")
plt.show()

# 3️⃣ Scatter plot: Life Expectancy vs Total Mortality
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Total_Mortality', y='Life expectancy', data=df)
plt.title("Life Expectancy vs Total Mortality")
plt.savefig("scatter_lifeexp_totalmortality.png")
plt.show()

# 4️⃣ Correlation heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(df.corr(), annot=False, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.savefig("heatmap_corr.png")
plt.show()

print("\n✅ Plots created and saved!")
