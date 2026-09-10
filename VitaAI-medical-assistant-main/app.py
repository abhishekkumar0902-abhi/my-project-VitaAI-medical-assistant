from flask import Flask , render_template, jsonify, request
from src.helper import download_embeddings, filter_to_minimal_docs
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os




app = Flask(__name__)


load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY= os.getenv("GROQ_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY 


embeddings = download_embeddings()


index_name = "vitaai"
#embedd each chunk and upsert the embeddings into your pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})
chatModel = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),

    ]
)


# QA chain 
question_answer_chain = create_stuff_documents_chain(chatModel, prompt)


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    print(f"User Input: {msg}")
    # Pinecone se docs fetch 
    retrieved_docs = retriever.invoke(msg)
    # Docs ko filter (Source/Page)
    filtered_docs = filter_to_minimal_docs(retrieved_docs)
    # QA chain call 
    response = question_answer_chain.invoke({
        "input": msg,
        "context": filtered_docs
    })
    # Response print and return
    print("Response : ", response)
    return str(response)
    



if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)