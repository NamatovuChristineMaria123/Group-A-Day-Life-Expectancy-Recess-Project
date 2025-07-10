import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Load the engineered dataset
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

# Split dataset (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training samples: {X_train.shape[0]}")
print(f"Testing samples: {X_test.shape[0]}")

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on test set
y_pred = model.predict(X_test)

# Evaluate performance on test set
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"\n✅ Model Trained!")
print(f"Test RMSE: {rmse:.2f}")
print(f"Test R²: {r2:.4f}")
