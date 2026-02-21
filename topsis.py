import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_excel("decision_matrix.xlsx")

models = data.iloc[:, 0]
matrix = data.iloc[:, 1:].values.astype(float)

weights = np.array([0.30, 0.25, 0.15, 0.15, 0.15])
impacts = np.array([1, 1, -1, -1, -1])

norm = matrix / np.sqrt((matrix**2).sum(axis=0))
weighted = norm * weights

ideal_best = np.where(impacts == 1, weighted.max(axis=0), weighted.min(axis=0))
ideal_worst = np.where(impacts == 1, weighted.min(axis=0), weighted.max(axis=0))

dist_best = np.sqrt(((weighted - ideal_best)**2).sum(axis=1))
dist_worst = np.sqrt(((weighted - ideal_worst)**2).sum(axis=1))

score = dist_worst / (dist_best + dist_worst)

result = pd.DataFrame({
    "Model": models,
    "TOPSIS Score": score
})

result = result.sort_values(by="TOPSIS Score", ascending=False)
result["Rank"] = range(1, len(result) + 1)

result.to_csv("results.csv", index=False)

plt.figure()
plt.bar(result["Model"], result["TOPSIS Score"])
plt.title("TOPSIS Ranking of Text Classification Models")
plt.ylabel("Score")
plt.savefig("graphs.png")

print(result)