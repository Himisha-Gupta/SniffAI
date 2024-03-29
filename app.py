# import streamlit as st
# import tempfile
# from prediction import load_model, predict
# import wikipedia


# def save_uploaded_file(uploaded_file):
#     # Create a temporary file
#     with tempfile.NamedTemporaryFile(delete=False, suffix="." + uploaded_file.name.split('.')[-1]) as tmp_file:
#         # Write the uploaded file's contents to the temporary file
#         tmp_file.write(uploaded_file.getbuffer())
#         return tmp_file.name  # Return the path of the saved file


# def get_wikipedia_summary(search_term, sentences=3):
#     try:
#         summary = wikipedia.summary(search_term, sentences=sentences)
#         return summary
#     except wikipedia.exceptions.PageError:
#         return "No page found for the search term."
#     except wikipedia.exceptions.DisambiguationError as e:
#         return f"Multiple pages found: {e.options}"



# st.title('SniffAI')
# st.write(":robot_face: Upload a dog image and find out the breed :sparkles:")

# load = st.button("Load model")
# if 'model' not in st.session_state:
#     st.session_state['model'] = load_model()
#     st.write("Model loaded!")

# if st.session_state['model']:
#     with st.form(key='prexdict_form'):
#         input_dog_file = st.file_uploader("Upload a picture of your dog here.", type=["jpg", "png", "jpeg"])
#         submit_button = st.form_submit_button("Predict Dog")

#         if submit_button:
#             if input_dog_file is not None:
#                 with st.spinner('Predicting...'):
#                     print(input_dog_file)
#                     file_path = save_uploaded_file(input_dog_file)
            #         # st.write(f"The file is temporarily saved at: {file_path}")
            #         result = predict(st.session_state['model'], file_path)
            #     answer = get_wikipedia_summary(result[0])
            #     st.success(f"{result[0]} : {answer}")
            #     st.image(file_path)
            # else:
            #     st.error("Please upload a file first.")


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

# Set page title and description
st.title('🐾 SniffAI 🤖')
st.markdown("*Upload a picture of your dog and find out its breed!*")

# Load model button
load = st.button("Load model")
if 'model' not in st.session_state:
    st.session_state['model'] = load_model()
    st.success("Model loaded!")

# Display prediction form
if st.session_state.get('model'):
    with st.form(key='predict_form'):
        st.header("Predict Dog Breed")
        input_dog_file = st.file_uploader("Upload a picture of your dog", type=["jpg", "png", "jpeg"])
        submit_button = st.form_submit_button("Predict")

        if submit_button:
            if input_dog_file is not None:
                with st.spinner('Predicting...'):
                    file_path = save_uploaded_file(input_dog_file)
                    result = predict(st.session_state['model'], file_path)
                    answer = get_wikipedia_summary(result[0])
                    st.success(f"Predicted Breed: {result[0]}")
                    st.image(file_path, caption='Uploaded Image', use_column_width=True)
                    st.markdown("---")
                    st.markdown(f"**Wikipedia Summary for {result[0]}**: {answer}")
            else:
                st.error("Please upload a file first.")


