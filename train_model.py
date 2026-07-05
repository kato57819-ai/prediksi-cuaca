import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# Load dataset
data = pd.read_csv("weather.csv")

# Feature
X = data[['suhu', 'kelembapan', 'angin']]

# Target
y = data['cuaca']

# Model
model = DecisionTreeClassifier()

# Training
model.fit(X, y)

# Simpan model
joblib.dump(model, 'model.pkl')

print("Model berhasil dibuat!")