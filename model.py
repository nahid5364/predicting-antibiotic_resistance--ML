from imblearn.over_sampling import SMOTE
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix, classification_report
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import shap

# Step 1: Load and preprocess data
def load_and_preprocess_data(filepath):
    data = pd.read_csv(filepath)  # Load the dataset

    # Create interaction feature between Hospitalization Duration and Last Antibiotic Exposure
    data['Duration_Exposure_Interaction'] = (
        data['Hospitalization_Duration'] + '_' + data['Last_Antibiotic_Exposure']
    )

    # Encode categorical variables, including the interaction feature
    data = pd.get_dummies(data, columns=[
        "Gender", "Admission_Department", "Hospitalization_Duration",
        "Last_Antibiotic_Exposure", "Region", "Duration_Exposure_Interaction"
    ], drop_first=True)

    # Define features and target
    X = data.drop(columns=["Resistance"])  # Features
    y = data["Resistance"]  # Target

    # Feature correlation check- to see weightings of variables on model with dummy dataset
    correlations = data.corr()
    # Plotting heatmap to show feature weighting
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlations, annot=True, cmap="coolwarm")
    plt.title("Feature Correlations")
    plt.show()

    # Resample to address imbalance
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    return X_resampled, y_resampled, X.columns.tolist()

# Plotting Feature distributions to normalize data
def plot_feature_distributions(data):
    features = data.columns
    for feature in features:
        if data[feature].dtype in ["int64", "float64"]:  # Plot only the numerical features
            plt.figure(figsize=(6, 4))
            plt.hist(data[feature], bins=30, color='blue', alpha=0.7)
            plt.title(f"Distribution of {feature}")
            plt.xlabel(feature)
            plt.ylabel("Frequency")
            plt.grid(axis='y', alpha=0.75)
            plt.show()

# Step 2: Train logistic regression model
def train_model(X, y):
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train logistic regression model
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])

    print("Model Performance:")
    print(f"Accuracy: {accuracy}")
    print(f"ROC-AUC: {roc_auc}")
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    # Save the model
    joblib.dump(model, "logistic_regression_model.pkl")
    print("Model saved to logistic_regression_model.pkl")

    return model, X_train, X_test, y_test, y_pred

# Step 3: Visualize model performance
def plot_confusion_matrix(y_test, y_pred):
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Not Resistant", "Resistant"], yticklabels=["Not Resistant", "Resistant"])
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.show()

# Step 3.1: Using SHAP to analyse feature contributions of model
def evaluate_shap(model, X_train, X_test, feature_names):
    # Convert X_test to a DataFrame with the correct feature names
    X_test = pd.DataFrame(X_test, columns=feature_names)

    # Use a KernelExplainer for SHAP compatibility with logistic regression
    explainer = shap.KernelExplainer(model.predict_proba, shap.kmeans(X_train, 10))
    shap_values = explainer.shap_values(X_test)

    # Check for shape consistency
    if shap_values[1].shape != X_test.shape:
        raise ValueError("SHAP values matrix shape does not match input data. Check feature preprocessing.")

    # Summary plot for global feature importance
    shap.summary_plot(shap_values[1], X_test, feature_names=feature_names)

    # Bar plot for average feature importance
    shap.summary_plot(shap_values[1], X_test, feature_names=feature_names, plot_type="bar")

    # Force plot for a single prediction (first instance in X_test)
    shap.force_plot(explainer.expected_value[1], shap_values[1][0], X_test.iloc[0, :], matplotlib=True)

# Step 4: Save predictions
def save_predictions(X_test, y_test, y_pred):
    results = X_test.copy()
    results["Actual"] = y_test.values
    results["Predicted"] = y_pred
    results.to_csv("predictions.csv", index=False)
    print("Predictions saved to predictions.csv")

# Main function
if __name__ == "__main__":
    filepath = "antibiotic_resistance_dummy_dataset.csv"  # Dataset path
    X, y, feature_names = load_and_preprocess_data(filepath)  # Preprocess and resample

    # Debug: Verify feature count and names
    print("Training Feature Names:", feature_names)
    print("Number of Features in Training:", len(feature_names))

    # Train the model
    model, X_train, X_test, y_test, y_pred = train_model(X, y)  # Train model

    # Save feature names
    joblib.dump(feature_names, "logistic_regression_features.pkl")
    print("Feature names saved to logistic_regression_features.pkl")

    plot_confusion_matrix(y_test, y_pred)  # Visualize

    # 3.1 SHAP analysis
    evaluate_shap(model, X_train, X_test, feature_names)
    save_predictions(X_test, y_test, y_pred)  # Save predictions

    # Loading dataset
    data = pd.read_csv(filepath)
    plot_feature_distributions(data)  # Check feature distributions
