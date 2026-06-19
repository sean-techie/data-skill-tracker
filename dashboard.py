import streamlit as st
import pandas as pd
from collections import Counter
import plotly.express as px

st.set_page_config(
    page_title="Workforce Skills Analytics Dashboard",
    layout="wide"
)

st.title("Workforce Skills Analytics Dashboard")
st.caption("Cross-industry skills intelligence and workforce demand analysis")

df = pd.read_csv("data.csv")

industries = ["All Industries"] + sorted(
    df["industry"].unique().tolist()
)

selected_industry = st.selectbox(
    "Industry",
    industries
)

filtered_df = df

if selected_industry != "All Industries":
    filtered_df = df[
        df["industry"] == selected_industry
    ]

all_skills = []

for skills in filtered_df["skills"]:
    all_skills.extend(skills.split())

skill_counts = Counter(all_skills)

skill_df = pd.DataFrame(
    skill_counts.items(),
    columns=["Skill", "Count"]
).sort_values(
    by="Count",
    ascending=False
)

top_skill = skill_df.iloc[0]["Skill"]
top_count = skill_df.iloc[0]["Count"]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Job Listings",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Unique Skills",
        len(skill_df)
    )

with col3:
    st.metric(
        "Top Skill",
        top_skill
    )

with col4:
    st.metric(
        "Demand Score",
        top_count
    )

st.divider()

left, right = st.columns([2, 1])

with left:

    st.subheader("Top 10 Most In-Demand Skills")

    chart_df = skill_df.head(10)

    fig = px.bar(
        chart_df,
        x="Count",
        y="Skill",
        orientation="h",
        text="Count",
        color="Count",
        color_continuous_scale=[
            "#0F172A",
            "#334155",
            "#64748B",
            "#94A3B8"
        ]
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=550,
        showlegend=False,
        title=None,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        font=dict(
            family="Arial",
            size=14
        ),
        coloraxis_showscale=False,
        yaxis=dict(
            title="",
            categoryorder="total ascending"
        ),
        xaxis=dict(
            title="Demand Score",
            showgrid=True,
            gridcolor="#E5E7EB"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("Top Skills")

    st.dataframe(
        chart_df,
        use_container_width=True,
        hide_index=True
    )

st.divider()

st.subheader("Insights")

st.info(
    f"{top_skill} is currently the most requested skill with {top_count} mentions across the selected dataset."
)

st.markdown("### Key Findings")

st.markdown(
    f"""
    - **{top_skill}** ranks as the highest-demand skill.
    - The dataset contains **{len(skill_df)} unique skills**.
    - A total of **{len(filtered_df)} job listings** were analyzed.
    - Skills demand varies significantly across industries.
    """
)

st.divider()

st.subheader("Dataset Preview")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)