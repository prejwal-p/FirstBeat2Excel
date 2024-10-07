import streamlit as st  
import pandas as pd
import pymupdf
from functions import *
import base64

# Adding header to the app
st.title("Data Extraction from FirstBeat Reports")


# Uploading the file
uploaded_file = st.file_uploader("Choose a file", type=['pdf'])

if uploaded_file is not None:
    pdf_file = uploaded_file.read()
    doc = pymupdf.open(stream=pdf_file, filetype="pdf")

    # Extracting the text from the first page
    page = doc[0]
    text = page.get_text("text")
    text = text.split("\n")
    try:
        first_page_data = extract_first_page_data(text)
    except Exception as e:
        st.warning(f"The data could not be extracted from the first page. Error Message: {e}")
        st.stop()

    # Extracting the data from the third page
    page = doc[2]
    text = page.get_text("text")
    text = text.split("\n")
    try:
        third_page_data = extract_third_page_data(text)
    except Exception as e:
        st.warning(f"The data could not be extracted from the third page. Error Message: {e}")
        st.stop()

    # Combining the data
    data = pd.concat([first_page_data, third_page_data], axis=1)
    # Closing the document
    doc.close()

    st.dataframe(data)


