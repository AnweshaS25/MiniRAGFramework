import sys 

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


import os
import tempfile

import streamlit as st

from src.loaders.pdf_loader import PDFLoader
from src.splitters.recursive_text_splitter import RecursiveTextSplitter
from src.embeddings.huggingface_embeddings import HuggingFaceEmbeddings
from src.vectorstores.chroma_vector_store import ChromaVectorStore
from src.retrievers.similarity_retriever import SimilarityRetriever
from src.prompts.default_prompt_template import DefaultPromptTemplate
from src.llms.groq_llm import GroqLLM

from src.pipelines.indexing_pipeline import IndexingPipeline
from src.pipelines.rag_pipeline import RAGPipeline


st.set_page_config(
    page_title="MiniRAG PDF Assistant",
    page_icon="📄",
    layout="wide",
)

st.title("📄 MiniRAG PDF Assistant")

st.write(
    "Upload a PDF and ask questions about it."
)

if "indexed" not in st.session_state:
    st.session_state.indexed = False

if "rag_pipeline" not in st.session_state:
    st.session_state.rag_pipeline = None

if "current_file" not in st.session_state:
    st.session_state.current_file = None

if "messages" not in st.session_state:
    st.session_state.messages = []

uploaded_file = st.file_uploader(
    "Choose a PDF",
    type=["pdf"],
)

if uploaded_file is not None: 

    file_changed = (
        uploaded_file.name != st.session_state.current_file
    )

    if file_changed:

        with st.spinner("📄 Saving uploaded PDF..."):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf",
            ) as temp_file:

                temp_file.write(uploaded_file.getbuffer())
                pdf_path = temp_file.name

        st.success("PDF uploaded successfully!")

        loader = PDFLoader(pdf_path)

        splitter = RecursiveTextSplitter()

        embedding_model = HuggingFaceEmbeddings()

        vector_store = ChromaVectorStore(
            collection_name="streamlit_pdf_assistant",
            persist_directory="./streamlit_chroma_db",
        )

        vector_store.clear()

        indexing_pipeline = IndexingPipeline(
            loader=loader,
            splitter=splitter,
            embedding_model=embedding_model,
            vector_store=vector_store,
        )
        try: 
            with st.spinner("🧠 Indexing document..."):
                chunks = indexing_pipeline.run()
        except Exception as e:
            st.error(f"Indexing failed: {e}")
            st.stop()
        finally:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

        retriever = SimilarityRetriever(
            embedding_model=embedding_model,
            vector_store=vector_store,
        )

        prompt_template = DefaultPromptTemplate()

        llm = GroqLLM()

        rag_pipeline = RAGPipeline(
            retriever=retriever,
            prompt_template=prompt_template,
            llm=llm,
        )

        st.session_state.rag_pipeline = rag_pipeline
        st.session_state.indexed = True
        st.session_state.current_file = uploaded_file.name

        st.success(f"✅ Successfully indexed {len(chunks)} chunks!")

if st.session_state.indexed:

    st.success(
        f"Current document: {st.session_state.current_file}"
    )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_question = st.chat_input(
        "Ask a question about the PDF..."
    )

    if user_question:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_question,
            }
        )

        with st.chat_message("user"):
            st.markdown(user_question)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                response = st.session_state.rag_pipeline.run(
                    query=user_question,
                )

                assistant_answer = response.text

                st.markdown(assistant_answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_answer,
                }
        )