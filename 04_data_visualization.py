import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv("smart_watch_health_data_final.csv")

# sns.countplot(x='health', data=df)
# plt.title("Health Class Distribution")
# plt.show()

# plt.figure(figsize=(8,6))
# sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
# plt.title("Correlation Matrix")
# plt.show()

# sns.pairplot(df, hue='health')
# plt.show()

# sns.histplot(data=df, x='stress_level', hue='health', multiple='stack')
# plt.show()

plt.figure(figsize=(8,5))
sns.boxplot(x='health', y='heart_rate_BPM', data=df)
plt.title("Heart Rate vs Health")
plt.show()