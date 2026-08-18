import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from Chains import Email
from langchain_community.document_loaders import PyPDFLoader
import tempfile

def Create_Web(llm):
    st.title('Resume<>Email')
    Input = st.file_uploader('Choose a pdf file', type=['pdf'])
    Role = st.text_input('Enter a Position you want to apply')
    Company = st.text_input('Enter a company name')

    Button = st.button('Sumbit')

    if Button:
        try:

            if Input is None:
                st.warning('File not supported')
                return
            with st.spinner('Generatin Email...'):
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(Input.read())
                    temp_path = tmp_file.name

                Loader = PyPDFLoader(temp_path)
                Pages = Loader.load()
                Page_data = Pages
                Extract_Info = llm.Resume_Input(Page_data)
                Content = llm.Write_Email(Extract_Info, Role, Company)
                st.code(Content, language='markdown')

        except Exception as e:
            st.error(f"An error has occured {e}")

if __name__ == "__main__":
    Chain = Email()
    st.set_page_config(layout='wide', page_title='Email Generator')
    Create_Web(Chain)
