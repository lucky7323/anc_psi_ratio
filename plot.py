import pandas as pd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("seaborn")

df = pd.read_csv("data.csv")
print(df.describe())
scales = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]
xs, ys = [], []

for s in scales:
    x = np.arange(0, 150000)
    y = x * s
    xs.append(x)
    ys.append(y)

z_scores = stats.zscore(df)
abs_z_scores = np.abs(z_scores)
filtered_entries = (abs_z_scores < 3).all(axis=1)
df = df[filtered_entries]

lim_scales = [(90000, 11000), (50000, 7000), (20000, 6000), (10000, 5000), (5000, 4000), (2000, 1500)]
for xl, yl in lim_scales:
    plt.figure(figsize=(12, 8))
    plt.title("anc-psi weekly airdrop ratio")
    plt.scatter(df['anc'], df['psi'], s=8)
    for x, y, label in zip(xs, ys, scales):
        plt.plot(x, y, label=f"{float(label):0.2f}x")
    plt.xlabel("$ANC")
    plt.ylabel("$PSI")
    plt.xlim([100, xl])
    plt.ylim([0, yl])
    plt.vlines(15000, 0, yl, linestyle='--', color='gray', linewidth=1)
    plt.vlines(4000, 0, yl, linestyle='--', color='gray', linewidth=1)
    plt.vlines(1250, 0, yl, linestyle='--', color='gray', linewidth=1)
    plt.legend()
    plt.savefig(f"result_{xl}_{yl}.png")
    plt.show()

