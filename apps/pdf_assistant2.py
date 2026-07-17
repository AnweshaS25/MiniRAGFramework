import sys 

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


import os
import tempfile

import streamlit as st


from src.constants import (
    LoaderTypes,
    SplitterTypes,
    EmbeddingTypes,
    VectorStoreTypes,
    RetrieverTypes,
    LLMTypes,
    RerankerTypes,
    SecurityTypes,
    RoleTypes,
    ToolRouterTypes,
    ContextRouterTypes,
    QueryRewriterTypes,
    PromptRouterTypes
)


from src.auth.user import User
from src.factories.role_factory import RoleFactory

from src.config.framework_config import FrameworkConfig
from src.config.framework_builder import FrameworkBuilder


current_user = User(
    username="anwesha",
    roles=[
       RoleFactory.create(RoleTypes.ADMIN),
    ],
)


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



        config = FrameworkConfig(
            loader_type=LoaderTypes.PDF,
            splitter_type=SplitterTypes.RECURSIVE,
            embedding_type=EmbeddingTypes.HUGGINGFACE,
            vector_store_type=VectorStoreTypes.CHROMA,
            retriever_type=RetrieverTypes.SIMILARITY,

            llm_types=[
                LLMTypes.GROQ,
                LLMTypes.GEMINI,
                LLMTypes.OLLAMA,
            ],

            conversation_window_size=2,

            summarize_after=6,

            prompt_router_type=PromptRouterTypes.RULE_BASED,

            tool_router_type=ToolRouterTypes.LLM,

            context_router_type=ContextRouterTypes.RULE_BASED,

            query_rewriter_type=QueryRewriterTypes.LLM,

            security_type=SecurityTypes.LLM,

            reranker_type=RerankerTypes.NONE,
        )




        builder = FrameworkBuilder(config)

        framework = builder.build(pdf_path)

        document_store = framework.document_store

        indexing_pipeline = framework.indexing_pipeline

        tool_manager = framework.tool_manager

        prompt_manager = framework.prompt_manager

        memory = framework.memory

        context_manager = framework.context_manager

        query_rewriter = framework.query_rewriter

        memory_retriever = framework.memory_retriever

        reranker = framework.reranker

        security_guard = framework.security_guard

        output_guard = framework.output_guard

        token_budget_strategy = framework.token_budget_strategy

        rag_pipeline = framework.pipeline





        st.write(type(framework))

        st.write(type(framework.core))

        st.write(type(framework.llm_manager))



        # core = builder.build_core(pdf_path)
        core = framework.core


        loader = core["loader"]
        splitter = core["splitter"]
        embedding_model = core["embedding_model"]
        vector_store = core["vector_store"]
        retriever = core["retriever"]

        print("\n========== FRAMEWORK BUILDER TEST ==========")
        print(type(core["loader"]))
        print(type(core["splitter"]))
        print(type(core["embedding_model"]))
        print(type(core["vector_store"]))
        print(type(core["retriever"]))
        print("===========================================\n")  


        vector_store.clear()



        try: 
            with st.spinner("🧠 Indexing document..."):
                chunks = indexing_pipeline.run(
                    metadata={
                        "permission": "VIEW_HR_DOCUMENTS"
                    }
                )
        except Exception as e:
            st.error(f"Indexing failed: {e}")
            st.stop()
        finally:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        



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
                        user=current_user,
                    )

                    assistant_answer = llm_response.text

                except PermissionError as e:
                    assistant_answer = f"🔒 {e}"

                except Exception as e:

                    import traceback

                    st.code(traceback.format_exc())

                    assistant_answer = f"❌ Error: {e}"

                st.markdown(assistant_answer)

        # Save assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_answer,
            }
        )

