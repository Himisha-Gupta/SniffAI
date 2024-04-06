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
    with st.form(key='predict_form'):
        st.write("Upload a picture of your dog:")
        input_dog_file = st.file_uploader("", type=["jpg", "png", "jpeg"], help="Accepted formats: JPG, PNG, JPEG")

        if input_dog_file is not None:
            submit_button = st.form_submit_button("Predict")

            if submit_button:
                with st.spinner('Predicting...'):
                    file_path = save_uploaded_file(input_dog_file)
                    result = predict(st.session_state['model'], file_path)
                    answer = get_wikipedia_summary(result[0])
                st.success(f"Predicted Breed: {result[0]}")
                st.write(f"*{answer}*")
                st.image(file_path, caption='Uploaded Image', use_column_width=True)
        else:
            st.error("Please upload an image.")



