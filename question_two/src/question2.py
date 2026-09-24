import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from docx import Document
from docx.shared import Inches, Pt

#Ingest
df_raw = pd.read_csv( "question_two\\data_raw\\StudentsPerformance.csv")

#Preproccessing
print("Missing values per column:")
print(df_raw.isnull().sum())

plot_df = df_raw.melt(
    id_vars="gender",
    value_vars=["math score", "reading score"],
    var_name="subject",
    value_name="score",
)
#V1 — Gender boxplots (math vs reading) 
plt.figure(figsize=(8, 6), dpi=300)
sns.boxplot(data=plot_df, x="subject", y="score", hue="gender")

plt.title("Math vs Reading Scores by Gender")
plt.xlabel("Subject")
plt.ylabel("Score (points out of 100)")
plt.xticks([0, 1], ["Math", "Reading"])
plt.yticks(range(0, 101, 10))
plt.legend(title="Gender")
plt.tight_layout()
plt.savefig("question_two\\results\\v1_gender_boxplots.png", dpi=300)

#V2 — Test prep impact on math
plt.figure(figsize=(8, 6), dpi=300)
sns.boxplot(
    data=df_raw,
    x="test preparation course",
    y="math score",
    hue="test preparation course",
    order=["none", "completed"],
    legend=False,
)

plt.title("Math Score by Test Preparation Course")
plt.xlabel("Test Preparation Course")
plt.ylabel("Math Score (points out of 100)")
plt.xticks([0, 1], ["None", "Completed"])
plt.yticks(range(0, 101, 10))
plt.tight_layout()
plt.savefig("question_two\\results\\v2_testprep_math.png", dpi=300)


#V3 — Lunch type and average performance
df_raw["overall_avg"] = df_raw[["math score", "reading score", "writing score"]].mean(axis=1)

lunch_means = (
    df_raw.groupby("lunch")[["math score", "reading score", "writing score", "overall_avg"]]
    .mean()
    .reset_index()
)

plot_lunch = lunch_means.melt(
    id_vars="lunch",
    value_vars=["math score", "reading score", "writing score"],
    var_name="subject",
    value_name="mean_score",
)

plt.figure(figsize=(8, 6), dpi=300)
sns.barplot(
    data=plot_lunch,
    x="lunch",
    y="mean_score",
    hue="subject",
    order=["free/reduced", "standard"],
)

plt.title("Mean Exam Scores by Lunch Type")
plt.xlabel("Lunch Type")
plt.ylabel("Mean Score (points out of 100)")
plt.yticks(range(0, 101, 10))
plt.legend(title="Subject")
plt.tight_layout()
plt.savefig("question_two\\results\\v3_lunch_scores.png", dpi=300)

# V4 — Subject correlations
score_cols = ["math score", "reading score", "writing score"]
corr = df_raw[score_cols].corr()

plt.figure(figsize=(8, 6), dpi=300)
sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    vmin=0,
    vmax=1,
    cmap="Blues",
    square=True,
    cbar_kws={"label": "Pearson correlation (r)"},
)

plt.title("Correlation Heatmap of Math, Reading, and Writing Scores")
plt.tight_layout()
plt.savefig("question_two\\results\\v4_score_correlations.png", dpi=300)

# V5 — Math vs reading with trend lines by test prep
n_completed = (df_raw["test preparation course"] == "completed").sum()
n_none = (df_raw["test preparation course"] == "none").sum()

df_raw["prep_label"] = df_raw["test preparation course"].map({
    "completed": f"Completed (n={n_completed})",
    "none": f"None (n={n_none})",
})

g = sns.lmplot(
    data=df_raw,
    x="reading score",
    y="math score",
    hue="prep_label",
    height=6,
    aspect=8 / 6,
    scatter_kws={"alpha": 0.5, "s": 30},
    line_kws={"linewidth": 2},
)

g.set_axis_labels("Reading Score (points out of 100)", "Math Score (points out of 100)")
g.ax.set_title("Math vs Reading Scores by Test Preparation Course")
g.ax.set_xticks(range(0, 101, 10))
g.ax.set_yticks(range(0, 101, 10))
g.ax.set_xlim(0, 100)
g.ax.set_ylim(0, 100)
g._legend.set_title("Test Preparation Course")
plt.tight_layout()
g.savefig("question_two\\results\\v5_math_reading_by_prep.png", dpi=300)


#Create a Word doc
doc = Document()
doc.add_heading("V1 — Gender boxplots (math vs reading)", 1)
doc.add_paragraph(
    "These side-by-side boxplots show math and reading scores for girls and boys. "
    "In math, boys score a little higher than girls. Their middle score is higher, but the spread looks about the same. "
    "In reading, it is the opposite. Girls have a higher middle score and a higher top of the box than boys. "
    "Both subjects have a few very low scores that stick out, especially in math. Most scores sit between about 40 and 90. "
    "The boxes (the middle 50 percentof scores) are about the same size for everyone. So the gender difference is more about the middle moving up or down, not about one group being much more spread out. "
    "Overall, boys tend to do a bit better in math, and girls tend to do a bit better in reading. "
    "The boxes still overlap a lot, so gender does not cleanly split high and low scorers."
)
doc.add_picture("question_two\\results\\v1_gender_boxplots.png", width=Inches(6))
doc.add_heading("V2 — Test prep impact on math ", 1)
doc.add_paragraph(
    "This boxplot compares math scores for students who took a test-prep course and students who did not. "
    "The prep group has a higher middle score and a higher top of the box. Their bottom of the box is a little higher too, so the whole middle 50% sits a bit higher. "
    "The two groups still overlap a lot. Plenty of students with no prep scored as well as students who took prep. "
    "Both groups have a few very low scores that stick out. The lowest ones are mostly among students who did not take prep. "
    "Overall, test prep goes with higher math scores. That does not prove prep caused the difference. Students who choose prep may already be more motivated or better prepared. "
)
doc.add_picture("question_two\\results\\v2_testprep_math.png", width=Inches(6))
doc.add_heading("V3 — Lunch type and average performance ", 1)
doc.add_paragraph(
    "Lunch type is linked to exam scores in this dataset."
    "Students with standard lunch have a higher average overall score than students with free or reduced lunch. The same gap shows up in math, reading, and writing, so it is not just one subject."
    "The difference is medium, not huge. Both groups still score in a similar part of the 0–100 range."
    "A grouped bar chart makes this easy to see, because you can compare each subject inside each lunch type."
    "Lunch is probably standing in for money and resources at home, not causing the scores by itself. Students with free or reduced lunch may also differ in other ways. This chart shows a connection, not proof that lunch type alone changes scores."
)
doc.add_picture("question_two\\results\\v3_lunch_scores.png", width=Inches(6))
doc.add_heading("V4 — Subject correlations ", 1)
doc.add_paragraph(
    "The heatmap shows that math, reading, and writing scores all go up and down together."
    "Every correlation is positive and strong. Students who score higher in one subject usually score higher in the others too."
    "Reading and writing have the strongest link. That makes sense, because both are language skills."
    "Math is still closely tied to reading and writing, but those links are a little weaker."
    "None of the pairs is close to zero, so the three tests are not separate, independent scores."
    "This pattern points to something shared, like overall academic skill, study habits, or school quality."
    "Because the links are strong, an average of the three scores is a fair summary of overall performance."
)
doc.add_picture("question_two\\results\\v4_score_correlations.png", width=Inches(6))
doc.add_heading("V5 — Math vs reading with trend lines by test prep ", 1)
doc.add_paragraph(
    "Math and reading scores go up together. Students who read well also tend to score higher in math."
    "The points sit fairly close to the upward line. That matches the strong link we saw in the heatmap."
    "Both test-prep groups follow this same pattern."
    "The prep group sits a bit higher on the math side for the same reading score. Those students often have a math advantage."
    "The two best-fit lines have similar slopes. Prep does not clearly change how strongly math rises with reading."
    "Prep looks more like a lift in scores than a change in the math–reading link."
    "The two clouds of points still overlap a lot, so test prep does not split the groups completely."
)
doc.add_picture("question_two\\results\\v5_math_reading_by_prep.png", width=Inches(6))
doc.save("question_two\\results\\findings_report.docx")