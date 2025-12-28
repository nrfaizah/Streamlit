import streamlit as st
# page setup
st.set_page_config(page_title="My Streamlit Apps - Faiza")

st.title("Layout And Sidebar")
col1 ,col2 = st.columns(2)

with col1:
    st.header("Left Side")
    name = st.text_input("enter your name :")
    if name:
        st.success(f"welcome user {name}")

with col2:
    st.header("odd Even Checker") 
    num = st.slider("Select Number ",1,100,3)
    if num %2==0:
        st.write("Even Number")
    else:
        st.write("Odd number")    

with st.sidebar:
    st.header("Control Panel")
    usercolour = st.color_picker("Picker your fovourite Colour " ,"#000000")
    st.write("You have selected : ", usercolour)        


# in side bar provide 2 options to user
# select dark / light theme    
# if user selects dark change the theme of streamlit apps

#control c (for stop terminal run)