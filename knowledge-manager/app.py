from flask import Flask, request, jsonify
import os
from langchain_elasticsearch import ElasticsearchStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
from langchain_core.documents import Document
from langchain_elasticsearch import ElasticsearchStore
from langchain_ollama import OllamaEmbeddings
import json
import requests

es_host = os.environ["ES_HOST"]
es_password = os.environ["ELASTIC_PASSWORD"]
ollama_host = os.environ["OLLAMA_HOST"]
embedding_model = os.environ["EMBEDDING_MODEL"]

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'pdf'}

import time
time.sleep(15)

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

elasticsearch_client = ElasticsearchStore(
    es_url="http://" + es_host + ":9200",
    index_name="smart-search",
    embedding=OllamaEmbeddings(model=embedding_model, base_url="http://" + ollama_host + ":11434"),
    es_user="elastic",
    es_password=es_password
    )

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
                documents.append(Document(page_content=chunk,metadata={"source_document": f"{pdf.filename}","page_number": page_number}))
            page_number += 1

    return documents

@app.route('/v1/init', methods=['GET'])
def load_initial_pdf_documents():
    # Directory containing test PDF documents
    pdf_directory = "./test_documents"

    # Get a list of PDF files in the directory
    pdf_files = [os.path.join(pdf_directory, f) for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

    uuids = []

    # Iterate over the PDF files and send each one to the /v1/add endpoint
    for pdf_file in pdf_files:
        with open(pdf_file, 'rb') as file:
            # Make a POST request to the /v1/add endpoint
            response = requests.post(
                url="http://localhost:6000/v1/add",
                files={'file': file}
            )
        
        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            if "uuids" in response_data:
                uuids.extend(response_data["uuids"])
        else:
            print(f"Failed to upload {pdf_file}: {response.text}")
    return jsonify({"message": "Knowledge store initialized."}), 200


def add_pdf_documents(documents)-> list[str]:
    document_length = 0
    for doc in documents:
        document_length += len(doc.page_content)

    print(document_length)
    print("embedding documents")


    uuids = elasticsearch_client.add_documents(documents)
    return uuids


@app.route('/v1/add', methods=['POST'])
def upload_file():
    # Check if the request has a file
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    # If no file is selected
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Check if the file is a PDF
    if file and allowed_file(file.filename):
        filename = file.filename
        output_file_path = "data/data.json"

        # Ensure the data directory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        # Load existing data or initialize a new list
        if os.path.exists(output_file_path):
            with open(output_file_path, "r") as json_file:
                try:
                    data = json.load(json_file)
                except json.JSONDecodeError:
                    data = []  # If the file is empty or invalid
        else:
            data = []

        # Check if the file already exists in the JSON
        if any(entry["file"] == filename for entry in data):
            return jsonify({"message": f"File {filename} already exists."}), 200

        # Process and embed the new file
        documents = get_pdf_documents([file])
        uuids = add_pdf_documents(documents)

        # Construct the current entry
        current_entry = {
            "file": filename,
            "uuids": uuids
        }

        # Append the new entry
        data.append(current_entry)

        # Write back to the JSON file
        with open(output_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        return jsonify({"message": f"File {filename} uploaded successfully", "uuids": uuids}), 200
    else:
        return jsonify({"error": "Invalid file type. Only PDFs are allowed."}), 400
    

@app.route('/v1/delete', methods=['DELETE'])
def delete_file():
    file_name = request.args.get('file')
    if not file_name:
        return jsonify({"error": "File name is required"}), 400

    # Specify the data file path
    data_file_path = "data/data.json"

    # Check if data.json exists
    if not os.path.exists(data_file_path):
        return jsonify({"error": "No data.json file found"}), 404

    # Load existing data
    with open(data_file_path, "r") as json_file:
        try:
            data = json.load(json_file)
        except json.JSONDecodeError:
            return jsonify({"error": "data.json is corrupted"}), 500

    # Find the entry for the given file name
    entry_to_delete = None
    for entry in data:
        if entry["file"] == file_name:
            entry_to_delete = entry
            break

    if not entry_to_delete:
        return jsonify({"error": f"No entry found for file: {file_name}"}), 404

    # Retrieve the UUIDs to delete
    uuids_to_delete = entry_to_delete["uuids"]

    # Delete the documents from the vector store
    try:
        elasticsearch_client.delete(uuids_to_delete)
    except Exception as e:
        return jsonify({"error": f"Failed to delete UUIDs from vector store: {str(e)}"}), 500

    # Remove the entry from data.json
    data = [entry for entry in data if entry["file"] != file_name]

    # Write updated data back to data.json
    with open(data_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

    return jsonify({"message": f"File {file_name} and associated UUIDs deleted successfully"}), 200

@app.route('/v1/documents', methods=['GET'])
def list_documents():
    # Specify the data file path
    data_file_path = "data/data.json"

    # Check if data.json exists
    if not os.path.exists(data_file_path):
        return jsonify({"error": "No data.json file found"}), 404

    # Load existing data
    with open(data_file_path, "r") as json_file:
        try:
            data = json.load(json_file)
        except json.JSONDecodeError:
            return jsonify({"error": "data.json is corrupted"}), 500
        
    # Return all of the things in the json file
    return jsonify({"documents": data}), 200


if __name__ == '__main__':
    app.run(debug=True,port=6000)
