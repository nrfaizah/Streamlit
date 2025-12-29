import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Data Cleaning App", layout="wide", page_icon="🧹")

st.title("🧹 Data Cleaning App (Streamlit)")
st.write("Upload a **CSV** or **Excel** file, clean it, and download the cleaned version.")

# -------------------------
# Helpers
# -------------------------
@st.cache_data
def load_file(file, file_name: str) -> pd.DataFrame:
    file_name = file_name.lower()
    if file_name.endswith(".csv"):
        return pd.read_csv(file)
    return pd.read_excel(file)  # supports .xlsx / .xls

def init_clean_df(df: pd.DataFrame):
    # store a working copy in session_state so buttons can modify it
    if "clean_df" not in st.session_state:
        st.session_state.clean_df = df.copy()

def missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    ms = df.isnull().sum()
    ms = ms[ms > 0].sort_values(ascending=False)
    return ms.reset_index().rename(columns={"index": "column", 0: "missing_count"})

def get_num_cols(df: pd.DataFrame):
    return df.select_dtypes(include=[np.number]).columns.tolist()

def get_cat_cols(df: pd.DataFrame):
    return df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

# -------------------------
# Upload
# -------------------------
uploaded = st.file_uploader("📂 Upload CSV / Excel", type=["csv", "xlsx", "xls"])

if uploaded is None:
    st.info("Upload a file to start cleaning.")
    st.stop()

try:
    df = load_file(uploaded, uploaded.name)
except Exception as e:
    st.error("❌ Could not read the file. Please upload a valid CSV/Excel file.")
    st.exception(e)
    st.stop()

# Init working df
init_clean_df(df)

st.subheader("1) Original Data Preview")
st.dataframe(df.head(), use_container_width=True)

# -------------------------
# Cleaning workspace
# -------------------------
st.subheader("2) Cleaning Workspace (Current Clean Data)")
clean_df = st.session_state.clean_df
st.dataframe(clean_df.head(), use_container_width=True)

# -------------------------
# Missing + Duplicate report
# -------------------------
st.subheader("3) Missing Values & Duplicate Records")

colA, colB, colC, colD = st.columns(4)
colA.metric("Rows", clean_df.shape[0])
colB.metric("Columns", clean_df.shape[1])
colC.metric("Total Missing Values", int(clean_df.isnull().sum().sum()))
colD.metric("Duplicate Rows", int(clean_df.duplicated().sum()))

ms_table = missing_summary(clean_df)
if ms_table.empty:
    st.success("✅ No missing values found.")
else:
    st.write("Missing values by column:")
    st.dataframe(ms_table, use_container_width=True)

dup_count = int(clean_df.duplicated().sum())
if dup_count == 0:
    st.success("✅ No duplicate rows found.")
else:
    st.warning(f"⚠️ Found {dup_count} duplicate rows.")

# -------------------------
# Cleaning Actions (Buttons)
# -------------------------
st.subheader("4) Cleaning Actions")

left, right = st.columns(2)

with left:
    st.markdown("### A) Remove Missing Values (Drop)")
    drop_how = st.selectbox(
        "Drop rule",
        ["Drop rows with ANY missing values", "Drop rows where ALL values are missing"],
        key="drop_how"
    )
    if st.button("🗑️ Remove Missing Values", key="btn_drop_missing"):
        before = len(st.session_state.clean_df)
        if drop_how == "Drop rows with ANY missing values":
            st.session_state.clean_df = st.session_state.clean_df.dropna()
        else:
            st.session_state.clean_df = st.session_state.clean_df.dropna(how="all")
        after = len(st.session_state.clean_df)
        st.success(f"✅ Done! Rows: {before} → {after}")

with right:
    st.markdown("### B) Handle Missing Values (Fill)")
    num_cols = get_num_cols(clean_df)
    cat_cols = get_cat_cols(clean_df)

    fill_mode = st.selectbox(
        "Fill method",
        ["Fill numeric with MEAN + categorical with MODE", "Fill numeric with MEDIAN + categorical with MODE"],
        key="fill_mode"
    )

    # Optional: user chooses specific columns to fill
    fill_cols = st.multiselect(
        "Select columns to fill (leave empty = fill all columns with missing values)",
        options=clean_df.columns.tolist(),
        key="fill_cols"
    )

    if st.button("🧩 Handle Missing Values (Fill)", key="btn_fill_missing"):
        work = st.session_state.clean_df.copy()

        target_cols = fill_cols if len(fill_cols) > 0 else work.columns.tolist()

        for c in target_cols:
            if work[c].isnull().sum() == 0:
                continue

            if pd.api.types.is_numeric_dtype(work[c]):
                if fill_mode.startswith("Fill numeric with MEAN"):
                    value = work[c].mean()
                else:
                    value = work[c].median()
                work[c] = work[c].fillna(value)

            else:
                # MODE for categorical/others
                mode_series = work[c].mode(dropna=True)
                value = mode_series.iloc[0] if len(mode_series) > 0 else "Unknown"
                work[c] = work[c].fillna(value)

        st.session_state.clean_df = work
        st.success("✅ Missing values handled successfully!")

st.markdown("---")

st.markdown("### C) Remove Duplicate Rows")
if st.button("🧽 Remove Duplicate Values", key="btn_remove_dups"):
    before = len(st.session_state.clean_df)
    st.session_state.clean_df = st.session_state.clean_df.drop_duplicates()
    after = len(st.session_state.clean_df)
    st.success(f"✅ Done! Rows: {before} → {after}")

st.markdown("---")

# Optional: Reset
with st.expander("Reset options"):
    if st.button("↩️ Reset to Original Data"):
        st.session_state.clean_df = df.copy()
        st.success("Reset complete. Now using original data again.")

# -------------------------
# Download cleaned file
# -------------------------
st.subheader("5) Download Cleaned File")

download_format = st.radio("Download format", ["CSV", "Excel"], horizontal=True)

clean_df_final = st.session_state.clean_df

if download_format == "CSV":
    csv_bytes = clean_df_final.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Cleaned CSV",
        data=csv_bytes,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )
else:
    # Excel download (in-memory)
    import io
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        clean_df_final.to_excel(writer, index=False, sheet_name="cleaned_data")
    st.download_button(
        label="⬇️ Download Cleaned Excel",
        data=buffer.getvalue(),
        file_name="cleaned_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.caption("Tip: Clean using the buttons above, then download the updated file.")
