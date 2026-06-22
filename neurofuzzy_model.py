import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd


class NeuroFuzzyModel:
    def __init__(self):
        self.rules = []
        self.membership_functions = {}
        self.scaler = StandardScaler()

    def create_membership_functions(self):
        """Create triangular membership functions for each feature"""
        features = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']

        for feature in features:
            self.membership_functions[feature] = {
                'low': lambda x, f=feature: self.triangular_mf(x, 0, 25, 50),
                'medium': lambda x, f=feature: self.triangular_mf(x, 40, 60, 80),
                'high': lambda x, f=feature: self.triangular_mf(x, 70, 100, 120)
            }

    def triangular_mf(self, x, a, b, c):
        """Triangular membership function"""
        if x <= a:
            return 0
        elif a < x <= b:
            return (x - a) / (b - a)
        elif b < x <= c:
            return (c - x) / (c - b)
        else:
            return 0

    def define_rules(self):
        """Define fuzzy rules for heart disease detection"""
        self.rules = [
            {'conditions': {'age': 'high', 'trestbps': 'high', 'chol': 'high'},
             'weight': 0.9, 'risk': 'high'},
            {'conditions': {'age': 'medium', 'trestbps': 'high', 'thalach': 'low'},
             'weight': 0.8, 'risk': 'high'},
            {'conditions': {'age': 'low', 'trestbps': 'low', 'chol': 'low'},
             'weight': 0.1, 'risk': 'low'},
            {'conditions': {'oldpeak': 'high', 'exang': 1},
             'weight': 0.85, 'risk': 'high'},
            {'conditions': {'thalach': 'high', 'oldpeak': 'low'},
             'weight': 0.2, 'risk': 'low'},
        ]

    def predict(self, features):
        """Predict heart disease risk using fuzzy inference"""
        self.create_membership_functions()
        self.define_rules()

        risk_score = 0
        total_weight = 0

        for rule in self.rules:
            rule_firing = 1.0
            for condition, value in rule['conditions'].items():
                if condition in features:
                    feature_value = features[condition]
                    if condition in self.membership_functions:
                        if value in self.membership_functions[condition]:
                            mf_value = self.membership_functions[condition][value](feature_value)
                            rule_firing *= mf_value

            risk_score += rule_firing * rule['weight']
            total_weight += rule_firing

        if total_weight > 0:
            risk_percentage = (risk_score / total_weight) * 100
        else:
            risk_percentage = 50  # Default risk

        # Additional factors from clinical parameters
        risk_factors = 0

        # Age factor
        if features.get('age', 0) > 60:
            risk_factors += 15
        elif features.get('age', 0) > 45:
            risk_factors += 8

        # Blood pressure factor
        if features.get('trestbps', 0) > 140:
            risk_factors += 15
        elif features.get('trestbps', 0) > 120:
            risk_factors += 8

        # Cholesterol factor
        if features.get('chol', 0) > 240:
            risk_factors += 15
        elif features.get('chol', 0) > 200:
            risk_factors += 8

        # Heart rate factor
        if features.get('thalach', 0) < 100:
            risk_factors += 10

        # Oldpeak factor
        if features.get('oldpeak', 0) > 2:
            risk_factors += 15
        elif features.get('oldpeak', 0) > 1:
            risk_factors += 8

        # Combine fuzzy logic and clinical factors
        final_risk = (risk_percentage * 0.6) + (risk_factors * 0.4)
        final_risk = min(100, max(0, final_risk))

        result = "High Risk" if final_risk > 50 else "Low Risk"

        return round(final_risk, 2), result

    def load_dataset(self, filepath='heart.csv'):
        """Load and preprocess the heart disease dataset"""
        df = pd.read_csv(filepath)
        # Select features used in prediction (same as input form)
        feature_columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
                           'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        X = df[feature_columns]
        y = df['target']
        return X, y

    def evaluate_accuracy(self, test_size=0.2, random_state=42):
        """Evaluate model accuracy on the dataset"""
        X, y = self.load_dataset()

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )

        # Make predictions on test set
        predictions = []
        for _, row in X_test.iterrows():
            features = row.to_dict()
            risk_percentage, _ = self.predict(features)
            # Convert risk percentage to binary prediction ( >50% = high risk = disease)
            pred_class = 1 if risk_percentage > 50 else 0
            predictions.append(pred_class)

        # Calculate accuracy
        accuracy = (predictions == y_test.values).mean() * 100

        # Also compute other metrics
        from sklearn.metrics import precision_score, recall_score, f1_score
        precision = precision_score(y_test, predictions) * 100
        recall = recall_score(y_test, predictions) * 100
        f1 = f1_score(y_test, predictions) * 100

        return {
            'accuracy': round(accuracy, 2),
            'precision': round(precision, 2),
            'recall': round(recall, 2),
            'f1_score': round(f1, 2),
            'total_samples': len(X_test)
        }
