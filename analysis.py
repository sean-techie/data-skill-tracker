import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")

all_skills = []

for skills in df["skills"]:
    all_skills.extend(skills.split())

skill_counts = Counter(all_skills)

skill_df = pd.DataFrame(skill_counts.items(), columns=["Skill", "Count"])
skill_df = skill_df.sort_values(by="Count", ascending=False)

print(skill_df)

plt.figure(figsize=(10,5))
plt.bar(skill_df["Skill"], skill_df["Count"])
plt.title("Most In-Demand Skills")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("skills_chart.png")
print("\nChart saved as skills_chart.png")