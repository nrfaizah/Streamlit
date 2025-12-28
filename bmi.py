import streamlit as st
import altair as alt
import pandas as pd

# Page config
st.set_page_config(page_title="BMI Calculator", layout="centered")

st.title("💪 BMI CALCULATOR")
st.write("Let's calculate your **Body Mass Index (BMI)**")

# --------------------------
# INPUT SECTION
# --------------------------
st.header("Enter your details")

height = st.number_input(
    "Enter Your Height (in cm)",
    min_value=50,
    max_value=250,
    value=170
)

weight = st.number_input(
    "Enter Your Weight (in kg)",
    min_value=10,
    max_value=200,
    value=50
)

st.write("Your Height :", height, "cm")
st.write("Your Weight :", weight, "kg")

bmi = None
category = None
color = "#000000"

# --------------------------
# CALCULATE BMI
# --------------------------
if st.button("Calculate BMI"):
    h_m = height / 100  # convert cm to meter
    bmi = weight / (h_m ** 2)
    st.success(f"Your BMI is : {bmi:.2f}")

    # Determine category + color
    if bmi < 18.5:
        category = "Underweight"
        color = "#0EE3D5"
    elif 18.5 <= bmi < 25:
        category = "Normal"
        color = "#F0F0A5"
    elif 25 <= bmi < 30:
        category = "Overweight"
        color = "#968CE7"
    else:
        category = "Obese"
        color = "#E70E65"

    st.markdown(
        f"<h3 style='color:{color};'>Category: {category}</h3>",
        unsafe_allow_html=True
    )

# ==========================
# ALT A I R  C H A R T
# ==========================

st.subheader("BMI Categories Overview")

# Data for BMI categories (example upper range values)
bmi_data = pd.DataFrame({
    "Category": ["Underweight", "Normal", "Overweight", "Obese"],
    "Range": [18.5, 24.9, 29.9, 35.0]
})

# Custom colors for each category
color_scale = alt.Scale(
    domain=["Underweight", "Normal", "Overweight", "Obese"],
    range=["#0EE3D5", "#F0F0A5", "#968CE7", "#E70E65"]
)

# Create bar chart
chart = (
    alt.Chart(bmi_data)
    .mark_bar()
    .encode(
        x=alt.X("Category:N", title="BMI Category"),
        y=alt.Y("Range:Q", title="Approx. Upper BMI Range"),
        color=alt.Color("Category:N", scale=color_scale, legend=None),
    )
    .properties(width=600, height=400)
)

# IMPORTANT: use_container_width works with your Streamlit version
st.altair_chart(chart, use_container_width=True)
