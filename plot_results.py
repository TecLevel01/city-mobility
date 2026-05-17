import pandas as pd
import matplotlib.pyplot as plt

# Load results
pg = pd.read_csv("postgres_results.csv")
mongo = pd.read_csv("mongo_results.csv")

# Merge on run settings
df = pg.merge(
    mongo,
    on=["Run", "Users", "Trips", "Events_per_trip"],
    suffixes=("_pg", "_mongo")
)

queries = ["Q1_time", "Q2_time", "Q3_time", "Q4_time"]

for query in queries:

    plt.figure(figsize=(12, 6))

    x = range(len(df))

    plt.plot(x, df[f"{query}_pg"], marker="o", label="PostgreSQL")
    plt.plot(x, df[f"{query}_mongo"], marker="o", label="MongoDB")

    labels = [
        f'U{u}-T{t}-E{e}'
        for u, t, e in zip(df["Users"], df["Trips"], df["Events_per_trip"])
    ]

    plt.xticks(x, labels, rotation=90)

    plt.title(f"{query} Performance Comparison")
    plt.xlabel("The 36 insertions")
    plt.ylabel("Execution Time (seconds)")
    plt.legend()

    plt.tight_layout()

    plt.savefig(f"{query}_comparison.png")
    plt.close()

print("Graphs generated successfully.")
