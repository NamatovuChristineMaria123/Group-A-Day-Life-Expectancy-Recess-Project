import pandas as pd
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import LinearRegression


df = pd.read_csv("Life_Expectancy_Engineered.csv")
df.columns = df.columns.str.strip()

# Select final features
features = [
    'Schooling', 'Income composition of resources', 'BMI',
    'GDP', 'percentage expenditure', 'Alcohol',
    'Diphtheria', 'Polio', 'Hepatitis B', 'Total expenditure',
    'Total_Mortality', 'Health_Wealth_Index', 'Combined_Thinness'
]

X = df[features]
y = df['Life expectancy']

# Create the model
model = LinearRegression()

# 5-fold Cross-Validation
cv = KFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(model, X, y, cv=cv, scoring='r2')

print(f"\nCross-validated R² scores for each fold: {cv_scores}")
print(f"Mean R²: {cv_scores.mean():.4f}")
print(f"Std Dev of R²: {cv_scores.std():.4f}")

if cv_scores.mean() > 0.6:
    print("\n The model generalizes well across folds.")
else:
    print("\n The model might need tuning for better generalization.")
