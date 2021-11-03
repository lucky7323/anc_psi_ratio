import pandas as pd
import matplotlib.pyplot as plt
plt.style.use("seaborn")

df = pd.read_csv("data.csv")
print(df.describe())
#plt.figure(figsize=(12, 8))
#plt.scatter(df['anc'], df['psi'])
#plt.show()

