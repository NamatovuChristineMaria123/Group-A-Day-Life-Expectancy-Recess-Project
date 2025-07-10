import pandas as pd


df = pd.read_csv("Life_Expectancy_Data.csv")

# Strip leading/trailing spaces in all column names
df.columns = df.columns.str.strip()

# Now safely create new features
df['Total_Mortality'] = df['Adult Mortality'] + df['infant deaths'] + df['under-five deaths']
df['Health_Wealth_Index'] = df['GDP'] * df['Total expenditure']
df['Combined_Thinness'] = df['thinness  1-19 years'] + df['thinness 5-9 years']

print(df[['Total_Mortality', 'Health_Wealth_Index', 'Combined_Thinness']].head())

# Save new dataset
df.to_csv("Life_Expectancy_Engineered.csv", index=False)

print("\n New features created and saved successfully!")
