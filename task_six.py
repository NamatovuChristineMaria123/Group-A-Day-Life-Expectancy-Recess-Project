
# 📂 evaluate New Features


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


df = pd.read_csv("Life_Expectancy_Engineered.csv")

# Strip spaces from column names again (safe practice)
df.columns = df.columns.str.strip()

# Define target and features
target = 'Life expectancy'

# 🔹 Baseline features (before new features)
baseline_features = [
    'Schooling', 'Income composition of resources', 'BMI',
    'GDP', 'percentage expenditure', 'Alcohol',
    'Diphtheria', 'Polio', 'Hepatitis B', 'Total expenditure'
]

# 🔹 New features added
engineered_features = baseline_features + [
    'Total_Mortality', 'Health_Wealth_Index', 'Combined_Thinness'
]

# Split
X_base = df[baseline_features]
X_eng = df[engineered_features]
y = df[target]

Xb_train, Xb_test, yb_train, yb_test = train_test_split(X_base, y, test_size=0.2, random_state=42)
Xe_train, Xe_test, ye_train, ye_test = train_test_split(X_eng, y, test_size=0.2, random_state=42)

# Train base model
model_base = LinearRegression()
model_base.fit(Xb_train, yb_train)
yb_pred = model_base.predict(Xb_test)

# Train engineered model
model_eng = LinearRegression()
model_eng.fit(Xe_train, ye_train)
ye_pred = model_eng.predict(Xe_test)

# Evaluate
mae_base = mean_absolute_error(yb_test, yb_pred)
r2_base = r2_score(yb_test, yb_pred)

mae_eng = mean_absolute_error(ye_test, ye_pred)
r2_eng = r2_score(ye_test, ye_pred)

print(f"\n🔹 Baseline Model — MAE: {mae_base:.2f} | R²: {r2_base:.4f}")
print(f"🔹 Engineered Model — MAE: {mae_eng:.2f} | R²: {r2_eng:.4f}")

if r2_eng > r2_base:
    print("\ New features improved the model!")
else:
    print("\n New features did not significantly improve the model.")
