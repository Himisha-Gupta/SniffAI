import streamlit as st
import tempfile
from prediction import load_model, predict
import wikipedia

# Function to save uploaded file
def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix="." + uploaded_file.name.split('.')[-1]) as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        return tmp_file.name

# Function to get Wikipedia summary
def get_wikipedia_summary(search_term, sentences=3):
    try:
        summary = wikipedia.summary(search_term, sentences=sentences)
        return summary
    except wikipedia.exceptions.PageError:
        return "No page found for the search term."
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple pages found: {e.options}"

# Page Title and Description
st.title('🐾 SniffAI 🤖')
st.markdown("*Upload a picture of your dog and discover its breed!*")

# Load model button
load = st.button("Load Model")
if 'model' not in st.session_state:
    st.session_state['model'] = load_model()
    if st.session_state['model']:
        st.success("Model loaded successfully!")

# Prediction Form
if st.session_state.get('model'):
    st.subheader("Prediction Form")
    with st.form(key='predict_form')




