import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

st.set_page_config(page_title="EDA App", layout="wide", page_icon="📊")

st.title("📊 Data Science EDA App (Streamlit)")
st.write("Upload a **CSV** or **Excel** file to explore your dataset.")

# ---------------------------
# Helpers
# ---------------------------
@st.cache_data
def load_data(file, file_type: str):
    if file_type == "csv":
        return pd.read_csv(file)
    else:
        # Excel
        return pd.read_excel(file)

def dataframe_info(df: pd.DataFrame) -> str:
    buffer = io.StringIO()
    df.info(buf=buffer)
    return buffer.getvalue()

def safe_numeric_cols(df: pd.DataFrame):
    return df.select_dtypes(include=[np.number]).columns.tolist()

def safe_categorical_cols(df: pd.DataFrame):
    return df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

# ---------------------------
# Upload
# ---------------------------
uploaded_file = st.file_uploader("📂 Upload CSV or Excel", type=["csv", "xlsx", "xls"])

if uploaded_file is None:
    st.info("Please upload a dataset to begin.")
    st.stop()

file_name = uploaded_file.name.lower()
file_type = "csv" if file_name.endswith(".csv") else "excel"

try:
    df = load_data(uploaded_file, file_type)
except Exception as e:
    st.error("❌ Unable to read file. Please upload a valid CSV/Excel file.")
    st.exception(e)
    st.stop()

st.success("✅ File loaded successfully!")

# ---------------------------
# Basic EDA
# ---------------------------
st.subheader("1) Preview")
st.dataframe(df.head(), use_container_width=True)

st.subheader("2) Basic EDA Summary")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", df.shape[0])
c2.metric("Columns", df.shape[1])
c3.metric("Missing Values", int(df.isnull().sum().sum()))
c4.metric("Duplicate Records", int(df.duplicated().sum()))

st.subheader("3) Info (df.info())")
st.text(dataframe_info(df))

st.subheader("4) Describe (Numerical)")
num_cols = safe_numeric_cols(df)
if len(num_cols) > 0:
    st.dataframe(df[num_cols].describe().T, use_container_width=True)
else:
    st.warning("No numerical columns found.")

st.subheader("5) Describe (Categorical)")
cat_cols = safe_categorical_cols(df)
if len(cat_cols) > 0:
    st.dataframe(df[cat_cols].describe().T, use_container_width=True)
else:
    st.warning("No categorical columns found.")

# ---------------------------
# Column Selection (Multiselect)
# ---------------------------
st.subheader("6) Select Columns (Multiselect)")
selected_cols = st.multiselect("Choose columns to view", df.columns.tolist())

view_df = df[selected_cols] if selected_cols else df
st.write("Selected Data Preview")
st.dataframe(view_df.head(), use_container_width=True)

# ---------------------------
# Visualization
# ---------------------------
st.subheader("7) Visualizations (Seaborn + Matplotlib)")

tabs = st.tabs(["Histogram", "Boxplot", "Countplot", "Scatterplot", "Correlation Heatmap"])

# Histogram
with tabs[0]:
    st.markdown("### Histogram (Numeric)")
    if len(num_cols) == 0:
        st.info("No numeric columns available.")
    else:
        col = st.selectbox("Select numeric column", num_cols, key="hist_col")
        bins = st.slider("Bins", 5, 100, 30, key="hist_bins")

        fig, ax = plt.subplots()
        sns.histplot(df[col].dropna(), bins=bins, kde=True, ax=ax)
        ax.set_title(f"Histogram: {col}")
        st.pyplot(fig, use_container_width=True)

# Boxplot
with tabs[1]:
    st.markdown("### Boxplot (Numeric)")
    if len(num_cols) == 0:
        st.info("No numeric columns available.")
    else:
        col = st.selectbox("Select numeric column", num_cols, key="box_col")

        fig, ax = plt.subplots()
        sns.boxplot(x=df[col], ax=ax)
        ax.set_title(f"Boxplot: {col}")
        st.pyplot(fig, use_container_width=True)

# Countplot
with tabs[2]:
    st.markdown("### Countplot (Categorical)")
    if len(cat_cols) == 0:
        st.info("No categorical columns available.")
    else:
        col = st.selectbox("Select categorical column", cat_cols, key="count_col")
        top_n = st.slider("Show top N categories", 5, 50, 10, key="count_topn")

        vc = df[col].astype(str).value_counts().head(top_n).index
        plot_df = df[df[col].astype(str).isin(vc)]

        fig, ax = plt.subplots()
        sns.countplot(data=plot_df, y=col, order=plot_df[col].astype(str).value_counts().index, ax=ax)
        ax.set_title(f"Countplot (Top {top_n}): {col}")
        st.pyplot(fig, use_container_width=True)

# Scatterplot
with tabs[3]:
    st.markdown("### Scatterplot (Numeric vs Numeric)")
    if len(num_cols) < 2:
        st.info("Need at least 2 numeric columns for scatterplot.")
    else:
        x = st.selectbox("X-axis", num_cols, key="scat_x")
        y = st.selectbox("Y-axis", num_cols, key="scat_y")

        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x=x, y=y, ax=ax)
        ax.set_title(f"Scatterplot: {y} vs {x}")
        st.pyplot(fig, use_container_width=True)

# Correlation Heatmap
with tabs[4]:
    st.markdown("### Correlation Heatmap (Numeric)")
    if len(num_cols) < 2:
        st.info("Need at least 2 numeric columns for correlation heatmap.")
    else:
        corr = df[num_cols].corr(numeric_only=True)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr, annot=True, fmt=".2f", ax=ax)
        ax.set_title("Correlation Heatmap")
        st.pyplot(fig, use_container_width=True)

# ---------------------------
# Query Section (Assignment Part F)
# ---------------------------
st.subheader("8) Query Section (Return DataFrame Results)")

st.markdown("Choose a query type OR type a query in simple English (limited rules).")

query_mode = st.radio("Query input mode", ["Guided (Recommended)", "Free text"], horizontal=True)

# ---- Guided queries ----
if query_mode == "Guided (Recommended)":
    q_type = st.selectbox(
        "Select query",
        [
            "Show me top 5 categories",
            "Show records where customer initiated more than 5 customer service calls"
        ]
    )

    if q_type == "Show me top 5 categories":
        if len(cat_cols) == 0:
            st.warning("No categorical columns found to compute top categories.")
        else:
            cat_col = st.selectbox("Select categorical column", cat_cols, key="top5_cat_col")
            top_n = 5

            result = (
                df[cat_col]
                .astype(str)
                .value_counts()
                .head(top_n)
                .reset_index()
            )
            result.columns = [cat_col, "count"]

            st.write("✅ Result (Top 5 Categories)")
            st.dataframe(result, use_container_width=True)

    else:
        # "customer initiated more than 5 customer service calls"
        # Let user map which column represents customer service calls
        numeric_candidates = num_cols
        if len(numeric_candidates) == 0:
            st.warning("No numeric columns found to filter by service calls.")
        else:
            calls_col = st.selectbox("Select column for 'customer service calls'", numeric_candidates, key="calls_col")
            threshold = st.number_input("Threshold (more than)", min_value=0, value=5, step=1)

            result = df[df[calls_col] > threshold]
            st.write(f"✅ Result (Rows where {calls_col} > {threshold})")
            st.dataframe(result, use_container_width=True)
            st.caption(f"Returned {len(result)} rows.")

# ---- Free text queries (simple parser) ----
else:
    user_query = st.text_input("Type your query (examples below):")
    st.caption("Examples: 'show me top 5 categories' | 'show records where customer initiated more than 5 customer service calls'")

    if st.button("Run Query"):
        q = (user_query or "").strip().lower()

        if "top 5" in q and ("category" in q or "categories" in q):
            if len(cat_cols) == 0:
                st.warning("No categorical columns available.")
            else:
                st.info("Detected query: Top 5 categories. Please select a categorical column below.")
                cat_col = st.selectbox("Select categorical column", cat_cols, key="free_top5_cat_col")

                result = (
                    df[cat_col]
                    .astype(str)
                    .value_counts()
                    .head(5)
                    .reset_index()
                )
                result.columns = [cat_col, "count"]
                st.dataframe(result, use_container_width=True)

        elif ("customer service calls" in q or "service calls" in q) and ("more than" in q or "greater than" in q):
            if len(num_cols) == 0:
                st.warning("No numeric columns available.")
            else:
                st.info("Detected query: Filter records by service calls > threshold. Please map the column below.")
                calls_col = st.selectbox("Select service calls column", num_cols, key="free_calls_col")
                threshold = st.number_input("Threshold (more than)", min_value=0, value=5, step=1, key="free_threshold")

                result = df[df[calls_col] > threshold]
                st.dataframe(result, use_container_width=True)
                st.caption(f"Returned {len(result)} rows.")

        else:
            st.warning("Query not recognized. Use Guided mode or follow the example queries exactly.")
