import pandas as pd

REQUIRED_COLUMNS = [
    "student_id", "class", "attendance_pct", "study_hours_per_day",
    "assignment_score", "maths_score", "science_score", "english_score"
]
NUMERIC_COLUMNS = [
    "attendance_pct", "study_hours_per_day", "assignment_score",
    "maths_score", "science_score", "english_score"
]
SUBJECT_COLUMNS = ["maths_score", "science_score", "english_score"]

def clean_data(data: pd.DataFrame):
    """Validate, remove duplicate rows and impute numeric missing values."""
    df = data.copy()
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError("Missing required columns: " + ", ".join(missing_columns))

    rows_before = len(df)
    duplicates_removed = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()

    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    missing_filled = int(df[NUMERIC_COLUMNS].isna().sum().sum())
    for col in NUMERIC_COLUMNS:
        median = df[col].median()
        df[col] = df[col].fillna(0 if pd.isna(median) else median)

    # Keep percentage/mark fields within their valid ranges.
    for col in ["attendance_pct", "assignment_score"] + SUBJECT_COLUMNS:
        df[col] = df[col].clip(0, 100)
    df["study_hours_per_day"] = df["study_hours_per_day"].clip(lower=0, upper=24)
    df["student_id"] = df["student_id"].astype(str)
    df["class"] = df["class"].fillna("Unknown").astype(str)

    report = {
        "rows_before": rows_before,
        "duplicates_removed": duplicates_removed,
        "missing_filled": missing_filled
    }
    return df, report

def add_metrics(df: pd.DataFrame):
    result = df.copy()
    result["average_score"] = result[SUBJECT_COLUMNS].mean(axis=1).round(2)
    # Pass is defined as 40 or more in every subject for this demonstration.
    result["result"] = result[SUBJECT_COLUMNS].ge(40).all(axis=1).map({True: "Pass", False: "Needs Support"})
    return result

def generate_insights(df: pd.DataFrame):
    insights = []
    if df.empty:
        return ["No data available for the selected filters."]
    subject_means = df[SUBJECT_COLUMNS].mean()
    best_subject = subject_means.idxmax().replace("_score", "").title()
    weakest_subject = subject_means.idxmin().replace("_score", "").title()
    insights.append(f"{best_subject} has the highest average score ({subject_means.max():.1f}).")
    insights.append(f"{weakest_subject} has the lowest average score ({subject_means.min():.1f}); it may need additional learning support.")
    insights.append(f"{(df['result'] == 'Pass').mean() * 100:.1f}% of students meet the demonstration pass rule (at least 40 in every subject).")
    insights.append(f"Average attendance is {df['attendance_pct'].mean():.1f}%.")
    return insights
