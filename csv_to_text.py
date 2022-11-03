import pandas as pd

df = pd.read_csv("./lyrics.csv", usecols=["lyrics"], encoding="utf-8")

with open("constitution.txt", mode="a", encoding="utf-8") as f:
    for i in df["lyrics"]:
        f.write(i)
