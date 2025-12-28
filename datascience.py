import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title='Analyze Your Data', layout="wide", page_icon="🪭")

st.title("📊 Analyze Your Data")
st.write("Upload a **CSV** file and explore your data interactively")

# ─── Uploading CSV file ────────────────────────────────────────────────
uploaded_file = st.file_uploader("📂 Upload Your CSV File", type=["csv"])

if uploaded_file is not None:
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)

        # -------------------------------
        # Convert boolean columns to string
        # -------------------------------
        bool_cols = df.select_dtypes(include=["bool"]).columns
        if len(bool_cols) > 0:
            df[bool_cols] = df[bool_cols].astype(str)

    except Exception as e:
        st.error("❌ Could not read the file. Please upload a valid CSV file.")
        st.exception(e)
        st.stop()

    # If no error → show success + data preview
    st.success("✅ File Uploaded Successfully!")
    st.write("**📄 Preview of Data**")
    st.dataframe(df.head())

    # 📌 Data Overview
    st.write("**🔎 Data Overview**")
    st.write("Number Of Rows : ", df.shape[0])
    st.write("Number Of Columns : ", df.shape[1])
    st.write("Number Of Missing Values : ", df.isnull().sum().sum())
    st.write("Number Of Duplicate Records : ", df.duplicated().sum())

    # 📌 Complete Summary of Dataset (df.info)
    st.write("**ℹ️ Complete Summary of Dataset**")
    buffer = io.StringIO()
    df.info(buf=buffer)
    info = buffer.getvalue()
    st.text(info)

    # explanation
    # df.info() normally prints output to the console, it does not return text.
    # Streamlit can’t display console prints directly using st.write(df.info()).
    # So we use io.StringIO() as a temporary text holder (a “buffer”) to capture what df.info() prints.
    # Then we show that captured text on the Streamlit page using st.text(info).

    # 📊 Statistical Summary (Numerical)
    st.write("**📈 Statistical Summary Of Dataset**")
    st.dataframe(df.describe())

    # 📊 Statistical Summary (Non-Numerical / Categorical)
    st.write("**📋 Statistical Summary For Non-Numerical Features**")
    st.dataframe(df.describe(include="object"))

    # 🧑‍💻 Column Selection & Preview
    st.write("**🧑‍💻 Select Your Desired Columns**")
    columns = st.multiselect("Choose Columns", df.columns.tolist())

    st.write("**📄 Preview**")
    if columns:
        st.dataframe(df[columns].head())
    else:
        st.info("No columns selected. Showing full dataset.")
        st.dataframe(df.head())

    st.write("**📊 Data Visualization**")

    columns = df.columns.tolist()
    x_axis = st.selectbox("Select Column For The X-Axis", options=columns)
    y_axis = st.selectbox("Select Column For The Y-Axis", options=columns)

    # Create buttons for chart types
    col1, col2 = st.columns(2)

    with col1:
        lin_btn = st.button("Click Here To Generate A Line Graph")

    with col2:
        bar_btn = st.button("Click Here To Generate A Bar Graph")

    # ----------------------------
    # Plot Line Chart
    # ----------------------------
    if lin_btn:
        st.write("Line Graph")
        fig, ax = plt.subplots()
        ax.plot(df[x_axis], df[y_axis], marker="o")
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f"Line Graph of {y_axis} vs {x_axis}")
        st.pyplot(fig)

    # ----------------------------
    # Plot Bar Chart
    # ----------------------------
    if bar_btn:
        st.write("Bar Graph")
        fig, ax = plt.subplots()
        ax.bar(df[x_axis], df[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f"Bar Chart of {y_axis} vs {x_axis}")
        st.pyplot(fig)
