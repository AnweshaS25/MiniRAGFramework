import os
from dotenv import load_dotenv
import shutil

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_groq import ChatGroq

load_dotenv()

class LangChainPipeline:

    def __init__(self, pdf_path: str):

        self.pdf_path = pdf_path
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0,
        )

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        persist_directory = "./test_chroma_db_langchain"

        if os.path.exists(persist_directory):
            shutil.rmtree(persist_directory)

        self.vector_store = Chroma(
            collection_name="langchain_benchmark",
            persist_directory=persist_directory,
            embedding_function=self.embedding_model,
        )


    def load_documents(self):
        loader = PyMuPDFLoader(self.pdf_path)
        return loader.load()
    
    def split_documents(self, documents):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        return splitter.split_documents(documents)
    
    def index_documents(self, chunks):
        self.vector_store.add_documents(chunks)

    def get_retriever(
        self,
        k: int = 5,
    ):
        return self.vector_store.as_retriever(
            search_kwargs={
                "k": k,
            }
        )
    
    def retrieve(
        self,
        query: str,
        k: int = 5,
    ):
        retriever = self.get_retriever(k=k)
        return retriever.invoke(query)
    

    def generate(
        self, 
        query: str
    ) -> str:
        """
        Retrieve relevant documents and generate an answer.
        """

        retrieved_docs = self.retrieve(query)

        context = "\n\n".join(
            doc.page_content
            for doc in retrieved_docs
        )

        prompt = f"""
    You are a helpful assistant.

    Answer the user's question ONLY using the context below.

    If the answer is not present in the context, say:
    "I could not find the answer in the provided documents."

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

        response = self.llm.invoke(prompt)

        return response.content