from flask import Flask, render_template, request, jsonify
import time
from langchain_elasticsearch import ElasticsearchStore
from langchain_ollama import OllamaEmbeddings
import os
from document_ingestion import  load_pdf_documents

es_host = os.environ["ES_HOST"]
es_password = os.environ["ELASTIC_PASSWORD"]
ollama_host = os.environ["OLLAMA_HOST"]
embedding_model = os.environ["EMBEDDING_MODEL"]


#TODO: find a way to wait for the elasticsearch container to be ready
time.sleep(30)

# Initialize the Elasticsearch vector store for embedding and retrieval
elasticsearch_client = ElasticsearchStore(
    es_url="http://" + es_host + ":9200",
    index_name="smart-search",
    embedding=OllamaEmbeddings(model=embedding_model, base_url="http://" + ollama_host + ":11434"),
    es_user="elastic",
    es_password=es_password
    )

#Retriever Setup
retriever = elasticsearch_client.as_retriever(search_kwargs={"score_threshold": 0.7})

# Load PDF documents into Elasticsearch
uuids = load_pdf_documents(elasticsearch_client)
print(uuids)



app = Flask(__name__)
    
@app.route("/v1/search", methods=['POST']) 
def search():
    if request.method == 'POST':
        # Parse the JSON request body
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "Missing 'query' in request body"}), 400

        query = data['query']
        #TODO: Maybe in the future add filters or additional metadata for the search
        #filters = data.get('filters', {})
        #options = data.get('options', {})

        # Use the query to retrieve documents
        retrieved_documents = retriever.invoke(query)

        documents = []
        for document in retrieved_documents:
            documents.append({
                "page_content": document.page_content,
                "metadata": document.metadata
            })

        # Return the documents as a JSON response
        return jsonify(documents)



if __name__ == '__main__':
    app.run(debug=True,port=5000,use_reloader=False)