from dotenv import load_dotenv
import os 
from src.helper import load_pdf_files, filter_to_minimal_docs, text_split, download_embeddings, Document
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY= os.getenv("GROQ_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY 


extracted_data = load_pdf_files("data")
filter_data = filter_to_minimal_docs(extracted_data)
texts_chunk = text_split(filter_data)


embeddings = download_embeddings()

pinecone_api_key = PINECONE_API_KEY 
pc = Pinecone(api_key=pinecone_api_key)


# Creating the index in pinecone
index_name = "vitaai"

if not pc.has_index(index_name):
    pc.create_index(
        name = index_name,
        dimension=384,   #Dimension of the embeddings
        metric="cosine",   #cosine similarity
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(index_name)

# Store all of the vector
docsearch = PineconeVectorStore.from_documents(
    documents=texts_chunk,
    index_name=index_name,
    embedding=embeddings
)

about = Document(
    page_content="""
    Identity: My name is VitaAI. I am an advanced virtual health assistant designed to provide medical information, symptom analysis, and wellness guidance. I am not a human doctor, but an AI trained to assist with health-related queries.
    
    Creator: VitaAI was created and developed by an engineering team led by Harsh, with key contributions from Abhishek and Sonu. The project was supervised by Dr. Abhaya. The goal was to build a responsive, accessible, and accurate tool for preliminary health assessment.
    
    Capabilities: I can assist users by analyzing symptoms, suggesting potential causes for common ailments, explaining medical terminology, and providing general advice on diet, nutrition, and mental wellness. I can also help interpret lab report metrics.
    
    Safety Disclaimer: It is important to know that I am an Artificial Intelligence, not a licensed medical professional. My responses are for informational purposes only and should never replace professional medical advice, diagnosis, or treatment.
    
    Technology: Under the hood, VitaAI utilizes Large Language Models (LLMs) and Vector Search technology to retrieve accurate medical context.
    
    Privacy: VitaAI is designed with privacy in mind. I do not store personal identifiable information (PII) permanently for training purposes.
    """,
    metadata={"source": "About"}
)
docsearch.add_documents(documents=[about])
