import streamlit as st
import tempfile
from prediction import load_model, predict
import wikipedia

def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix="." + uploaded_file.name.split('.')[-1]) as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        return tmp_file.name

def get_wikipedia_summary(search_term, sentences=3):
    try:
        summary = wikipedia.summary(search_term, sentences=sentences)
        return summary
    except wikipedia.exceptions.PageError:
        return "No page found for the search term."
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple pages found: {e.options}"

# Add CSS style to change the background color
st.markdown("""
<style>
body {
    background-color: #f5f5f5;
}
</style>
""", unsafe_allow_html=True)

st.title('SniffAI 🐶🐾')
st.subheader('Identify your furry friend's breed with ease!')
st.write("Upload a dog image and find out the breed. 🚀")

load = st.button("Load Model")
if 'model' not in st.session_state:
    st.session_state['model'] = load_model()
    st.write("Model loaded!")

if st.session_state['model']:
    with st.form(key='prexdict_form'):
        st.subheader('Upload your dog image')
        input_dog_file = st.file_uploader("", type=["jpg", "png", "jpeg"], accept_multiple_files=False)
        submit_button = st.form_submit_button("Predict Dog Breed")

        if input_dog_file is not None:
            with st.spinner('Predicting...'):
                file_path = save_uploaded_file(input_dog_file)
                result = predict(st.session_state['model'], file_path)
            answer = get_wikipedia_summary(result[0])
            st.success(f"The predicted breed is: {result[0]}")
            st.write(f"{answer}")
            st.image(file_path, caption=f"Predicted breed: {result[0]}", use_column_width=True)
        else:
            st.error("Please upload a file first.")
