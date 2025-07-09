import streamlit as st
import PyPDF2
import tempfile

st.set_page_config(page_title="PDF QA Demo", layout="wide")
st.title("📄💬 Simple PDF Q&A Demo (No API)")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    # Read PDF text
    pdf_reader = PyPDF2.PdfReader(tmp_path)
    all_text = ""
    for page in pdf_reader.pages:
        all_text += page.extract_text() or ""

    st.subheader("PDF uploaded successfully! You can now ask a question.")

    question = st.text_input("Ask a question:")

    if question:
        # 🟢 Improved: Split on single newlines for resumes
        paragraphs = all_text.split("\n")
        best_chunk = ""
        max_matches = 0

        # Simple keyword-based search
        question_words = question.lower().split()

        for para in paragraphs:
            matches = sum(1 for word in question_words if word in para.lower())
            if matches > max_matches:
                max_matches = matches
                best_chunk = para

        if best_chunk.strip() and max_matches > 0:
            st.success("Answer (best matched line):")
            st.write(best_chunk.strip())
        else:
            st.error("Sorry, could not find relevant information in the PDF.")

    st.download_button("Download Full PDF Text", all_text, file_name="extracted_text.txt")
