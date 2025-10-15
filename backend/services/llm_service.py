"""LLM service for text extraction."""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

from backend.config import settings


class LLMService:
    """Service for LLM-based text extraction."""

    def __init__(self):
        """Initialize LLM service."""
        self.llm = ChatOpenAI(
            model_name=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            api_key=settings.OPENAI_API_KEY,
        )
        self.embedding_model = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)

    def extract_direct(self, text: str) -> str:
        """
        Extract information directly from text using LLM.

        Args:
            text: Text to extract information from

        Returns:
            Extracted information
        """
        prompt = f"Extract applicant info from this text:\n\n{text}"
        response = self.llm.predict(prompt)
        return response

    def extract_with_rag(self, text: str) -> str:
        """
        Extract information using RAG (Retrieval Augmented Generation).

        Args:
            text: Text to extract information from

        Returns:
            Extracted information
        """
        # Split text into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP
        )
        chunks = splitter.split_text(text)

        # Create vector store
        vectordb = FAISS.from_texts(chunks, self.embedding_model)
        retriever = vectordb.as_retriever()

        # Create QA chain
        qa = RetrievalQA.from_chain_type(llm=self.llm, retriever=retriever)

        # Extract information
        response = qa.run("Extract applicant GPA, intended major, and test scores.")
        return response


llm_service = LLMService()
