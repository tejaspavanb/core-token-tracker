import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load historical token data
data = pd.read_csv('historical_token_data.csv')

# Prepare features and target
X = data[['liquidity', 'holder_count', 'total_supply', 'launch_time']]
y = data['successful']  # 1 if token was successful, 0 otherwise

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Evaluate model
accuracy = model.score(X_test, y_test)
print(f'Model accuracy: {accuracy}')

# Save the model
import joblib
joblib.dump(model, 'models/token_predictor.pkl')