from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings


# Extract text from PDF files
def load_pdf_files(data):
    loader = DirectoryLoader(
        data,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )
     
    documents = loader.load()
    return documents 


def filter_to_minimal_docs(docs):
    filter_data = []
    for doc in docs:
        src = doc.metadata.get("source", "Unknown PDF")
        page_no = doc.metadata.get("page", "NA")
        
        # Metadata ko text ka hissa bana diya
        new_content = f"{doc.page_content}\n\n[INFO - Source: {src}, Page: {page_no}]"
        
        filter_data.append(
            Document(page_content=new_content)
        )
    return filter_data


# Split  the documents into smaller chunks
def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=20,
    length_function=len
)
    texts_chunk = text_splitter.split_documents(minimal_docs)
    return texts_chunk



# Download the Embeddings from HuggingFace
def download_embeddings():
    model_name = "sentence-transformers/all-MiniLM-L6-v2"  #this model return 384 dimension
    embeddings = HuggingFaceEmbeddings(
        model_name = model_name
    )
    return embeddings

