import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY", "")

# PDF path (preloaded)
PDF_PATH = "docs/quiz_and_qest_feature.pdf"  # Adjust this path if needed

# Page config
st.set_page_config(page_title="Chat with PDF", layout="wide")
st.title("📄 Quiz & Quest Documentation Chat")

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "qa" not in st.session_state:
    st.session_state.qa = None

# Load and process PDF once
if os.path.exists(PDF_PATH) and not st.session_state.qa:
    with st.spinner("Loading preloaded PDF..."):
        loader = PyPDFLoader(PDF_PATH)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = splitter.split_documents(documents)

        embeddings = HuggingFaceEmbeddings()
        db = FAISS.from_documents(docs, embeddings)

        llm = ChatGroq(api_key=groq_api_key, model="llama-3.3-70b-versatile")
        qa = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())

        st.session_state.qa = qa
        st.success("PDF loaded. Ask your questions!")

# Show chat interface
if st.session_state.qa:
    for user_msg, bot_msg in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(user_msg)
        with st.chat_message("assistant"):
            st.markdown(bot_msg)

    prompt = st.chat_input("Ask a question about the documentation:")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.spinner("Thinking..."):
            answer = st.session_state.qa.run(prompt)
        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.chat_history.append((prompt, answer))
