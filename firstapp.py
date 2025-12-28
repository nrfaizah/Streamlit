import streamlit as st
# title()---> it will display big title on web page
st.title("My First Streamlit App")
# Write()---> it will normal text on web page
st.write("Hello Word")
st.write("Learning Streamlit is FUN")

# must SAVE OKAY(SO CAN RUN) CTRL s
# IN Streamlit , using terminal to see the output 

st.title("🧤MY FUN GAME")
st.write("This is the **Bold Text** and this is the *Italic Text*")


# slider --> help to take number from user

st.header("Number Slider")
age = st.slider("Select Your Age",1,100,30)  # min,max,default value
st.write("Your Age 👧: ",age)

st.header("Taking an user input")
name = st.text_input("What is your name :")
if name:
    st.success(f"Nice to meet you {name} 👌") # while show u green box

st.header("Streamlit Button")
if st.button("Click Me!"):
    st.balloons() # pops ballon animation    

st.header("Markdown")# using for html program(that whose know, if not just use st.write)
st.markdown(" HI I AM MARKDOWN ")

st.write(" Learn more about streamlit using : http")

st.header("Streamlot code")
code1 = '''
def hello():
    print("I am faiza")
'''
st.code(code1,language="python")

# can use latex ---> can be used ML FORMULA'S
st.latex("(a+b) = a^2 +  b^2 + c^2")  
st.latex(r"\frac {1}{1+e^-score}")