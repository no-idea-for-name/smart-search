from flask import Flask, render_template, request
from document_ingestion import elasticsearch_client, load_pdf_documents
import time


time.sleep(25)
#Retriever Setup
retriever = elasticsearch_client.as_retriever(search_kwargs={"score_threshold": 0.7})

# Load PDF documents into Elasticsearch
uuids = load_pdf_documents(elasticsearch_client)


app = Flask(__name__)
    
@app.route("/search/<query>", methods=['GET']) 
def search(query):
    if request.method == 'GET':
        retrieved_documents = retriever.invoke(query)

        return str(retrieved_documents)



if __name__ == '__main__':
    app.run(debug=True,port=5000,use_reloader=False)
    elasticsearch_client.delete(uuids)