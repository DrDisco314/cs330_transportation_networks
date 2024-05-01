import pandana as pdna
import pandas as pd
from pandas import DataFrame
import csv
from pandana import Network
import time


def load_csv(filename: str) -> DataFrame:
    df = pd.read_csv(filename)
    return df


node_map = {}
matrix = [[]]
df = load_csv("Data/Surat_Edgelist.csv")
for row in df.iterrows():
    if row[1].iloc[2] not in node_map:
        node_map[row[1].iloc[2]] = 1
    if row[1].iloc[3] not in node_map:
        node_map[row[1].iloc[3]] = 1

n = int(max(node_map.keys()))
table = [
    [0 if i == j else float("infinity") for i in range(n + 1)] for j in range(n + 1)
]
print(len(table), len(table[0]))

for row in df.iterrows():
    print(int(row[1].iloc[2]), int(row[1].iloc[3]))
    table[int(row[1].iloc[2])][int(row[1].iloc[2])] = row[1].iloc[5]

print(table)
