import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import tempfile
import os

st.set_page_config(page_title="RAG PDF QA", layout="wide")
st.title("📄💬 High Accuracy PDF QA App")
st.write("✅ App started! Upload your PDF and ask your question.")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    # Load PDF
    loader = PyPDFLoader(tmp_path)
    documents = loader.load()

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)

    # Embeddings
    embeddings = OpenAIEmbeddings()

    # Vectorstore
    vectorstore = Chroma.from_documents(docs, embedding=embeddings)

    # Retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # LLM
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

    # QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False
    )

    question = st.text_input("Ask a question about this PDF:")

    if question:
        with st.spinner("Generating answer..."):
            result = qa_chain({"query": question})
            answer = result["result"]

            if "I don't know" in answer or "not found" in answer.lower():
                answer = "Information not found in the document."

            st.success(answer)

    os.remove(tmp_path)
