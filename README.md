# Student Performance Analysis

A beginner-friendly Data Analytics project that cleans student records, explores academic performance and presents interactive visual insights through Streamlit.

## Features
- Upload a CSV file or use the included synthetic sample dataset.
- Validate required columns, remove duplicate rows and fill missing numeric values using medians.
- Calculate each student's average score and a demonstration pass/support status.
- Explore subject-wise marks, score distributions, attendance, study time and class summaries.
- View automatically generated observations and download cleaned data.

## Technology stack
- Python
- Pandas and NumPy
- Plotly
- Streamlit

## Project structure
```text
Student-Performance-Analysis/
├── app.py
├── analysis.py
├── data/
│   └── student_performance.csv
├── requirements.txt
└── README.md
```

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment (recommended).
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the dashboard:
   ```bash
   streamlit run app.py
   ```

## CSV format
Required columns:
`student_id, class, attendance_pct, study_hours_per_day, assignment_score, maths_score, science_score, english_score`

All marks and attendance are expected on a 0–100 scale. Study hours are expected per day.

## Important notes
- The included dataset is synthetic demonstration data, not real student records.
- The pass rule in this project is defined for demonstration as 40 or more in every subject. Change it to match your institution's policy if needed.
- Correlation or visual patterns should not be interpreted as proof that one factor causes academic performance.
- For real student data, remove direct identifiers, obtain permission, restrict access and follow applicable privacy requirements.

## Possible future improvements
- Add SQL database integration.
- Add filters for semester and subject.
- Add exportable PDF reports.
- Add predictive modelling only after collecting an appropriate, consented dataset.
