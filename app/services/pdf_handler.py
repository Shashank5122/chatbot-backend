
import requests
from langchain.document_loaders import PyPDFLoader

def fetch_gem_report():
    GEM_URL = "https://gemconsortium.org/file/open?fileId=51377"
    LOCAL_FILE = "data/gem_report.pdf"

    response = requests.get(GEM_URL)
    with open(LOCAL_FILE, 'wb') as f:
        f.write(response.content)

    pdf_loader = PyPDFLoader(LOCAL_FILE)
    return pdf_loader.load()
