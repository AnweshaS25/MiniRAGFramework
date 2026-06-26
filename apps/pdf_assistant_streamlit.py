import sys 

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


import os
import tempfile

import streamlit as st

from src.factories.loader_factory import LoaderFactory
from src.factories.splitter_factory import SplitterFactory
from src.factories.embedding_factory import EmbeddingFactory
from src.factories.vector_store_factory import VectorStoreFactory
from src.factories.retriever_factory import RetrieverFactory
from src.prompts.default_prompt_template import DefaultPromptTemplate
from src.factories.llm_factory import LLMFactory
from src.factories.reranker_factory import RerankerFactory

from src.constants import (
    LoaderTypes,
    SplitterTypes,
    EmbeddingTypes,
    VectorStoreTypes,
    RetrieverTypes,
    LLMTypes,
    RerankerTypes,
)

from src.pipelines.indexing_pipeline import IndexingPipeline
from src.pipelines.rag_pipeline import RAGPipeline


st.set_page_config(
    page_title="MiniRAG PDF Assistant",
    page_icon="📄",
    layout="wide",
)

st.title("📄 MiniRAG PDF Assistant")

st.caption(
    "Upload a PDF and ask questions using Retrieval-Augmented Generation."
)

if "indexed" not in st.session_state:
    st.session_state.indexed = False

if "rag_pipeline" not in st.session_state:
    st.session_state.rag_pipeline = None

if "current_file" not in st.session_state:
    st.session_state.current_file = None

if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:

    st.header("📂 Document")

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"],
    )

    st.divider()

    if st.session_state.indexed:

        st.success("✅ Document Indexed")

        st.write(f"**Current PDF:**")
        st.caption(st.session_state.current_file)

        if "num_chunks" in st.session_state:
            st.write(f"**Chunks:** {st.session_state.num_chunks}")

        st.write("**Embedding:**")
        st.caption("Sentence Transformers")

        st.write("**Vector Store:**")
        st.caption("ChromaDB")

        st.write("**LLM:**")
        st.caption("Groq Llama 3.3 70B")


if uploaded_file is not None: 

    file_changed = (
        uploaded_file.name != st.session_state.current_file
    )

    if file_changed:

        st.session_state.messages = []

        st.session_state.indexed = False
        st.session_state.rag_pipeline = None
        st.session_state.current_file = None

        with st.spinner("📄 Saving uploaded PDF..."):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf",
            ) as temp_file:

                temp_file.write(uploaded_file.getbuffer())
                pdf_path = temp_file.name

        st.success("PDF uploaded successfully!")

        loader = LoaderFactory.create(LoaderTypes.PDF, file_path=pdf_path,)

        splitter = SplitterFactory.create(SplitterTypes.RECURSIVE,)

        embedding_model = EmbeddingFactory.create(EmbeddingTypes.HUGGINGFACE,)

        vector_store = VectorStoreFactory.create(
            VectorStoreTypes.CHROMA,
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

        retriever = RetrieverFactory.create(
            RetrieverTypes.SIMILARITY,
            embedding_model=embedding_model,
            vector_store=vector_store,
        )

        reranker = RerankerFactory.create(RerankerTypes.NONE,)

        prompt_template = DefaultPromptTemplate()

        llm = LLMFactory.create(LLMTypes.GROQ,)

        rag_pipeline = RAGPipeline(
            retriever=retriever,
            prompt_template=prompt_template,
            llm=llm,
            reranker=reranker,
        )

        st.session_state.rag_pipeline = rag_pipeline
        st.session_state.indexed = True
        st.session_state.current_file = uploaded_file.name
        st.session_state.num_chunks = len(chunks)

        st.rerun()

        st.success(f"✅ Successfully indexed {len(chunks)} chunks!")



# ---------------- Chat ---------------- #

if st.session_state.indexed:

    # Display previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    user_question = st.chat_input(
        "Ask a question about the PDF..."
    )

    if user_question:

        # Display user message immediately
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_question,
            }
        )

        with st.chat_message("user"):
            st.markdown(user_question)

        # Generate assistant response
        with st.chat_message("assistant"):

            with st.spinner("🤖 Thinking..."):

                try:

                    llm_response = st.session_state.rag_pipeline.run(
                        query=user_question,
                    )

                    assistant_answer = llm_response.text

                except Exception as e:

                    assistant_answer = f"❌ Error: {e}"

                st.markdown(assistant_answer)

        # Save assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_answer,
            }
        )




# if st.session_state.indexed:

#     st.success(
#         f"Current document: {st.session_state.current_file}"
#     )

#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     user_question = st.chat_input(
#         "Ask a question about the PDF..."
#     )

#     if user_question:
#         st.session_state.messages.append(
#             {
#                 "role": "user",
#                 "content": user_question,
#             }
#         )

#         with st.chat_message("user"):
#             st.markdown(user_question)

#         with st.chat_message("assistant"):

#             with st.spinner("Thinking..."):

#                 response = st.session_state.rag_pipeline.run(
#                     query=user_question,
#                 )

#                 assistant_answer = response.text

#                 st.markdown(assistant_answer)

#         st.session_state.messages.append(
#             {
#                 "role": "assistant",
#                 "content": assistant_answer,
#                 }
#         )