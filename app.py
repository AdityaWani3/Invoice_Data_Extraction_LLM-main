import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import logging
from backend import create_docs  # Ensure this function is implemented correctly

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the page configuration
st.set_page_config(page_title="Invoice Extraction Bot", layout="wide")

# Hide default Streamlit menu and footer
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

def add_custom_css():
    """Add custom CSS for styling."""
    st.markdown(
        """
        <style>
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 10px 20px;
                border-radius: 8px;
                border: none;
                cursor: pointer;
                transition: 0.3s;
            }
            .stButton>button:hover {
                background-color: #45a049;
                color: black;
            }
            .stDownloadButton>button {
                background-color: #008CBA;
                color: white;
                font-size: 16px;
                padding: 10px 20px;
                border-radius: 8px;
                border: none;
                cursor: pointer;
                transition: 0.3s;
            }
            .stDownloadButton>button:hover {
                background-color: #007bb5;
                color: black;
            }
            .center-aligned-title {
                text-align: center;
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .center-aligned-subheader {
                text-align: center;
                font-size: 20px;
                font-weight: normal;
                margin-bottom: 20px;
            }
            .info-section {
                background-color: rgba(255, 255, 255, 0.9);
                padding: 15px;
                border-radius: 10px;
                margin-top: 20px;
                box-shadow: 0px 0px 10px #5DADEC;
            }
            .info-section h3 {
                color: #ffcc00;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():
    load_dotenv()

    # Apply custom CSS
    add_custom_css()

    # App Title and Subtitle
    st.markdown('<h1 class="center-aligned-title">Invoice Extraction Bot</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="center-aligned-subheader">Extract invoice data effortlessly.</h2>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader("Upload invoices (PDFs or images)", accept_multiple_files=True)

    if st.button("Extract Data"):
        if uploaded_files:
            with st.spinner("Processing..."):
                try:
                    extracted_data = create_docs(uploaded_files)  # Ensure correct implementation
                    if isinstance(extracted_data, pd.DataFrame) and not extracted_data.empty:
                        st.dataframe(extracted_data)

                        data_as_csv = extracted_data.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            "Download data as CSV",
                            data_as_csv,
                            "extracted_data.csv",
                            "text/csv",
                        )
                        st.success("Data extraction complete!")
                    else:
                        st.warning("No data extracted from the uploaded files.")
                except Exception as e:
                    logger.error(f"Error during data extraction: {str(e)}", exc_info=True)
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please upload at least one file.")

    # Informational section
    st.markdown(
        """
        <div class="info-section">
            <h3>What is Invoice Data Extraction using LLM?</h3>
            <p>Invoice data extraction using a Large Language Model (LLM) leverages AI techniques to automatically extract key invoice details such as invoice numbers, dates, vendor names, amounts, and line-item data.</p>
            <p>By using LLMs, this process becomes highly accurate and efficient, reducing manual efforts in handling invoices.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == '__main__':
    logger.info("Invoice Extraction Bot started.")
    main()
