from flask import Flask, render_template, request, jsonify
import time

#TODO: find a way to wait for the elasticsearch container to be ready
time.sleep(30)
from document_ingestion import elasticsearch_client, load_pdf_documents
#Retriever Setup
retriever = elasticsearch_client.as_retriever(search_kwargs={"score_threshold": 0.7})

# Load PDF documents into Elasticsearch
uuids = load_pdf_documents(elasticsearch_client)


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

        # Use the query, filters, and options to retrieve documents
        retrieved_documents = retriever.invoke(query)

        # Prepare the JSON response
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