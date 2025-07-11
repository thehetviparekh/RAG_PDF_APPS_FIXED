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
        # Split on single newlines for resumes
        paragraphs = all_text.split("\n")
        best_index = -1
        max_matches = 0

        # Simple keyword-based search
        question_words = question.lower().split()

        for i, para in enumerate(paragraphs):
            matches = sum(1 for word in question_words if word in para.lower())
            if matches > max_matches:
                max_matches = matches
                best_index = i

        if best_index != -1 and max_matches > 0:
            # Build a mini paragraph around the best line (2 before and 2 after)
            start = max(best_index - 2, 0)
            end = min(best_index + 3, len(paragraphs))
            context_snippet = "\n".join(paragraphs[start:end]).strip()

            st.success("Answer (context snippet):")
            st.write(context_snippet)
        else:
            st.error("Sorry, could not find relevant information in the PDF.")

    st.download_button("Download Full PDF Text", all_text, file_name="extracted_text.txt")
