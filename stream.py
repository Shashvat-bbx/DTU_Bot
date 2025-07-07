import streamlit as st
from Rag_vector_store import ask_rag    

# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

# Add headings
st.title("DTU Notice Bot")
st.subheader("Enter your text below to get relevant information.")

text_input = st.text_input(
    "Enter some text 👇",
    label_visibility=st.session_state.visibility,
    disabled=st.session_state.disabled,
    placeholder="Enter your query",
)

final = ask_rag(text_input)

if text_input:
    st.write("You entered: ", text_input)
    st.markdown("### Answer:")
    st.markdown(final)
