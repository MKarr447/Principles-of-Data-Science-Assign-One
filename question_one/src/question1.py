
import pandas as pd

#Ingest
df_raw = pd.read_csv( "question_one\\\\data_raw\\frailty_data.csv")

#process
#Unit standardizationn
IN_TO_M = 0.0254
LB_TO_KG = 0.45359237

df_raw["Height_m"] = df_raw["Height"] * IN_TO_M
df_raw["Weight_kg"] = df_raw["Weight"] * LB_TO_KG
print(df_raw.head())

#Feature engineering
df_raw["BMI"] = (df_raw["Weight_kg"] / (df_raw["Height_m"] ** 2)).round(2)
print(df_raw.head())

df_raw["AgeGroup"] = pd.cut(
    df_raw["Age"],
    bins=[0, 29, 45, 60, 200],
    labels=["<30", "30–45", "46–60", ">60"],
).astype("category")

print(df_raw.head())

#Categorical → numeric encoding
df_raw["Frailty_binary"] = (df_raw["Frailty"] == "Y").astype("int8")
print(df_raw.head())

df_raw["AgeGroup_<30"] = (df_raw["AgeGroup"] == "<30").astype("int8")
df_raw["AgeGroup_30–45"] = (df_raw["AgeGroup"] == "30–45").astype("int8")
df_raw["AgeGroup_46–60"] = (df_raw["AgeGroup"] == "46–60").astype("int8")
df_raw["AgeGroup_>60"] = (df_raw["AgeGroup"] == ">60").astype("int8")

print(df_raw.head())

df_raw.to_csv("question_one\\data_clean\\processed.csv", index=False)

#EDA & Reporting
summary = df_raw.select_dtypes("number").agg(["mean", "median", "std"]).T.round(4)
print(summary)

lines = ["# Findings", "", "| Column | Mean | Median | Std |", "| --- | ---: | ---: | ---: |"]
for name, row in summary.iterrows():
    lines.append(f"| {name} | {row['mean']:.4f} | {row['median']:.4f} | {row['std']:.4f} |")

with open("question_one\\results\\findings.md", "w") as f:
    f.write("\n".join(lines))
print("wrote findings.md")

#Quantify relation of strength and frailty
corr = df_raw["Grip strength"].corr(df_raw["Frailty_binary"])
print(corr)

with open("question_one\\results\\findings.md", "a") as f:
    f.write("\n\n# Grip strength and frailty\n")
    f.write(f"Correlation between Grip strength and Frailty_binary: {corr:.4f}\n")
print("wrote correlation to findings.md")