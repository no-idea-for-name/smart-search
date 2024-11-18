from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
from langchain_core.documents import Document
import os
from langchain_elasticsearch import ElasticsearchStore
from langchain_ollama import OllamaEmbeddings



es_host = os.environ["ES_HOST"]
es_password = os.environ["ELASTIC_PASSWORD"]
ollama_host = os.environ["OLLAMA_HOST"]
embedding_model = os.environ["EMBEDDING_MODEL"]


def get_pdf_documents(pdf_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len
    )
    documents = []
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        page_number = 1
        for page in pdf_reader.pages:
            text = ""
            text += page.extract_text()
            chunks = text_splitter.split_text(text)
            for chunk in chunks:
                documents.append(Document(page_content=chunk,metadata={"source": f"{pdf}"+f" Page: {page_number}"}))
            page_number += 1

    return documents

def load_pdf_documents(elasticsearch_client):

    if check_elasticsearch_state() == False:
        # Replace this with the actual directory path containing your PDFs
        pdf_directory = "./test_documents"

        # Get a list of all PDF files in the directory
        pdf_files = [os.path.join(pdf_directory, f) for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

        # Pass the list of PDF file paths to the function
        documents = get_pdf_documents(pdf_files)
        document_length = 0
        for doc in documents:
            document_length += len(doc.page_content)

        print(document_length)
        print("embedding documents")


        uuids = elasticsearch_client.add_documents(documents)
        return uuids

    else:
        return None



#TODO: This function sucks, remove as soon as possible
def check_elasticsearch_state():
    if not os.path.exists("./state.txt"):
        # File does not exist, create it with 'false'
        with open("./state.txt", 'w') as file:
            file.write('true')
        return False    
    
    # File exists, read its content
    with open("./state.txt", 'r') as file:
        content = file.read().strip().lower()  # Normalize case and strip whitespace
    
    # Check if the content is 'true'
    return content == 'true'



# Initialize the Elasticsearch vector store for embedding and retrieval
elasticsearch_client = ElasticsearchStore(
    es_url="http://" + es_host + ":9200",
    index_name="smart-search",
    embedding=OllamaEmbeddings(model=embedding_model, base_url="http://" + ollama_host + ":11434"),
    es_user="elastic",
    es_password=es_password
    )


