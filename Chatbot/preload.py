from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os
import traceback
from django.conf import settings

class FAISSLoader:
    db = None

    @staticmethod
    def preload_faiss():
        try:
            print("Starting FAISS database preload...")
            pdf_path = os.path.join(settings.BASE_DIR, "Knowledge_Base.pdf")
            # Check if the PDF file exists
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
            print("File Found in the required path")
            # Load the PDF
            loader = UnstructuredPDFLoader(pdf_path)
            documents = loader.load()
            print(f"Loaded {len(documents)} documents from the PDF.")

            # Split the text
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            docs = text_splitter.split_documents(documents)
            print(f"Split into {len(docs)} chunks.")

            # Initialize embeddings
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

            # Create the FAISS database
            FAISSLoader.db = FAISS.from_documents(docs, embeddings)
            print("FAISS database successfully preloaded!")
        except Exception as e:
            print("Error during FAISS database preload:")
            print(traceback.format_exc())

    @staticmethod
    def get_faiss_db():
        if FAISSLoader.db is None:
            raise ValueError("FAISS database has not been preloaded!")
        return FAISSLoader.db