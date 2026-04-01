import pandas as pd
import numpy as np

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Preprocessing
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

# Models
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

# Evaluation
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

df = pd.read_csv("Data/health_data_1.csv")
df.head()

print(df.info())
print(df.describe())
print(df['health'].value_counts())

df = df.dropna()  # or use fillna()

df = df.drop("user_id", axis=1)

df = df.drop("health_score", axis=1)

df['activity_level'] = LabelEncoder().fit_transform(df['activity_level'])

le = LabelEncoder()
df['health'] = le.fit_transform(df['health'])

X = df.drop("health", axis=1)
y = df["health"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

rf = RandomForestClassifier()
rf.fit(X_train, y_train)

y_pred_rf = rf.predict(X_test)

svm = SVC()
svm.fit(X_train, y_train)

y_pred_svm = svm.predict(X_test)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

y_pred_knn = knn.predict(X_test)

print("RF Accuracy:", accuracy_score(y_test, y_pred_rf))
print("SVM Accuracy:", accuracy_score(y_test, y_pred_svm))
print("KNN Accuracy:", accuracy_score(y_test, y_pred_knn))

print(classification_report(y_test, y_pred_rf))

sns.heatmap(confusion_matrix(y_test, y_pred_rf), annot=True)
plt.show()

importances = rf.feature_importances_
feature_names = X.columns

plt.barh(feature_names, importances)
plt.show()

# Train model
rf = RandomForestClassifier()
rf.fit(X_train, y_train)

# Predictions
y_train_pred_rf = rf.predict(X_train)
y_test_pred_rf = rf.predict(X_test)

# Accuracy
train_acc_rf = accuracy_score(y_train, y_train_pred_rf)
test_acc_rf = accuracy_score(y_test, y_test_pred_rf)

print("Random Forest Training Accuracy:", train_acc_rf)
print("Random Forest Testing Accuracy:", test_acc_rf)

svm = SVC()
svm.fit(X_train, y_train)

y_train_pred_svm = svm.predict(X_train)
y_test_pred_svm = svm.predict(X_test)

print("SVM Training Accuracy:", accuracy_score(y_train, y_train_pred_svm))
print("SVM Testing Accuracy:", accuracy_score(y_test, y_test_pred_svm))

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

y_train_pred_knn = knn.predict(X_train)
y_test_pred_knn = knn.predict(X_test)

print("KNN Training Accuracy:", accuracy_score(y_train, y_train_pred_knn))
print("KNN Testing Accuracy:", accuracy_score(y_test, y_test_pred_knn))

results = pd.DataFrame({
    "Model": ["Random Forest", "SVM", "KNN"],
    "Train Accuracy": [
        accuracy_score(y_train, y_train_pred_rf),
        accuracy_score(y_train, y_train_pred_svm),
        accuracy_score(y_train, y_train_pred_knn)
    ],
    "Test Accuracy": [
        accuracy_score(y_test, y_test_pred_rf),
        accuracy_score(y_test, y_test_pred_svm),
        accuracy_score(y_test, y_test_pred_knn)
    ]
})

print(results)

