import pandas as pd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("seaborn")

df = pd.read_csv("data.csv")
print(df.describe())

z_scores = stats.zscore(df)
abs_z_scores = np.abs(z_scores)
filtered_entries = (abs_z_scores < 3).all(axis=1)
df = df[filtered_entries]
plt.figure(figsize=(12, 8))
plt.scatter(df['anc'], df['psi'])
plt.savefig("result.png")
plt.show()

