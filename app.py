import streamlit as st
import pandas as pd
import plotly.express as px
from analysis import clean_data, add_metrics, generate_insights

st.set_page_config(page_title="Student Performance Analytics", page_icon="🎓", layout="wide")
st.title("🎓 Student Performance Analysis Dashboard")
st.caption("Explore academic performance, attendance, study habits and assessment results.")

@st.cache_data
def load_sample():
    return pd.read_csv("data/student_performance.csv")

uploaded = st.sidebar.file_uploader("Upload a student CSV (optional)", type=["csv"])
raw = pd.read_csv(uploaded) if uploaded else load_sample()
st.sidebar.info("Expected columns: student_id, class, attendance_pct, study_hours_per_day, assignment_score, maths_score, science_score, english_score")
df, cleaning_report = clean_data(raw)
df = add_metrics(df)

st.sidebar.header("Filters")
classes = sorted(df["class"].dropna().astype(str).unique().tolist())
selected_classes = st.sidebar.multiselect("Class", classes, default=classes)
filtered = df[df["class"].astype(str).isin(selected_classes)].copy()

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

total = len(filtered)
avg_score = filtered["average_score"].mean()
avg_att = filtered["attendance_pct"].mean()
pass_rate = (filtered["result"] == "Pass").mean() * 100

c1, c2, c3, c4 = st.columns(4)
c1.metric("Students", f"{total:,}")
c2.metric("Average score", f"{avg_score:.1f}/100")
c3.metric("Average attendance", f"{avg_att:.1f}%")
c4.metric("Pass rate", f"{pass_rate:.1f}%")

st.subheader("Performance overview")
left, right = st.columns(2)
with left:
    subject_cols = ["maths_score", "science_score", "english_score"]
    subject_avg = filtered[subject_cols].mean().rename_axis("subject").reset_index(name="average")
    subject_avg["subject"] = subject_avg["subject"].str.replace("_score", "", regex=False).str.title()
    fig = px.bar(subject_avg, x="subject", y="average", title="Average marks by subject",
                 labels={"subject": "Subject", "average": "Average marks"}, text_auto=".1f")
    st.plotly_chart(fig, use_container_width=True)
with right:
    fig = px.histogram(filtered, x="average_score", nbins=15, title="Distribution of average scores",
                       labels={"average_score": "Average score"})
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Attendance and study habits")
left, right = st.columns(2)
with left:
    fig = px.scatter(filtered, x="attendance_pct", y="average_score", color="result",
                     hover_data=["student_id", "class"], title="Attendance vs average score",
                     labels={"attendance_pct": "Attendance (%)", "average_score": "Average score"})
    st.plotly_chart(fig, use_container_width=True)
with right:
    fig = px.scatter(filtered, x="study_hours_per_day", y="average_score", color="result",
                     hover_data=["student_id", "class"], title="Study time vs average score",
                     labels={"study_hours_per_day": "Study hours/day", "average_score": "Average score"})
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Class-wise summary")
summary = filtered.groupby("class", as_index=False).agg(
    students=("student_id", "count"),
    average_score=("average_score", "mean"),
    attendance=("attendance_pct", "mean"),
    pass_rate=("result", lambda x: (x == "Pass").mean() * 100)
).round(1)
st.dataframe(summary, use_container_width=True, hide_index=True)

st.subheader("Key observations")
for item in generate_insights(filtered):
    st.markdown(f"- {item}")

with st.expander("Data cleaning report"):
    st.write(f"Rows in uploaded/source data: **{cleaning_report['rows_before']}**")
    st.write(f"Duplicate rows removed: **{cleaning_report['duplicates_removed']}**")
    st.write(f"Missing numeric values filled: **{cleaning_report['missing_filled']}**")
    st.write("Missing values are filled using the median of each numeric column. This is a simple baseline approach; review the method for real institutional data.")

st.subheader("Student-level data")
st.dataframe(filtered.sort_values("average_score", ascending=False), use_container_width=True, hide_index=True)
st.download_button("Download cleaned analysis data", filtered.to_csv(index=False).encode("utf-8"),
                   file_name="cleaned_student_performance.csv", mime="text/csv")

st.caption("Dataset included with this project is synthetic sample data created for demonstration. It does not represent real students.")
