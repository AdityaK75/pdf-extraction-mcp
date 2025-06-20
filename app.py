import streamlit as st
from pdf_extractor import PDFExtractor

st.title("📄 PDF Extractor (with OCR fallback)")

pdf_file = st.file_uploader("Upload a PDF", type="pdf")
pages_input = st.text_input("Pages to extract (e.g. 1,2,-1)", "")

if pdf_file:
    with open("temp.pdf", "wb") as f:
        f.write(pdf_file.read())

    extractor = PDFExtractor()
    try:
        result = extractor.extract_content("temp.pdf", pages_input)
        st.text_area("Extracted Content", result, height=400)
    except Exception as e:
        st.error(f"Error: {e}")
