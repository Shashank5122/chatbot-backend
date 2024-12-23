from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from dotenv import load_dotenv
from app.services.chatbot_logic import get_llm_chain
import os

# Load environment variables
load_dotenv()
token = os.getenv("HF_API_TOKEN")

# Directory to persist vectorstore
PERSIST_DIRECTORY = "vectorstores"

# URLs for World Bank indicators
urls = [
    'https://data.worldbank.org/indicator/SI.POV.DDAY?locations=1W-BR',
    'https://data.worldbank.org/indicator/IT.NET.USER.ZS?locations=1W-BR',
    'https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS?locations=1W-BR'
]

# Check if the vectorstore already exists
if not os.path.exists(PERSIST_DIRECTORY):
    print("Vectorstore not found. Creating a new one...")

    # Load and process data from URLs
    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
    docs = text_splitter.split_documents(data)

    # Load and process data from PDFs
    DATA_PATH = 'data/'
    loader_1 = DirectoryLoader(DATA_PATH, glob="./*.pdf", loader_cls=PyPDFLoader)
    docs_1 = loader_1.load()
    text_splitter_1 = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts_1 = text_splitter_1.split_documents(docs_1)

    # Combine all documents
    combined_docs = docs + texts_1

    # Initialize embeddings and create vectorstore
    embeddings = HuggingFaceEmbeddings()
    vectorstore = Chroma.from_documents(
        documents=combined_docs,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    # Persist the vectorstore for future use
    print("Vectorstore created and persisted.")
else:
    print("Loading existing vectorstore...")
    # Load precomputed vectorstore
    embeddings = HuggingFaceEmbeddings()
    vectorstore = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings
    )

# Define retriever
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Define the HuggingFace LLM endpoint
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    max_length=128,
    temperature=0.2,
    token=token
)

# Prompt Template
prompt_template = """
<|system|>
Answer the question based on your knowledge. Use the following context to help:

{context}

</s>
<|user|>
{question}
</s>
<|assistant|>
"""

# Build LLM Chain
prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)
llm_chain = prompt | llm | StrOutputParser()

# RAG Pipeline
rag_chain = {"context": retriever, "question": RunnablePassthrough()} | llm_chain
