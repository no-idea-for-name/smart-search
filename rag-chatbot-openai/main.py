from flask import Flask, request, jsonify
from langchain_openai import OpenAI,ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_elasticsearch import ElasticsearchStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import PromptTemplate
from langsmith import Client,traceable
import os


embedding_model = os.environ["LANGCHAIN_TRACING_V2"]
api_key = os.environ["LANGCHAIN_API_KEY"]
embedding_model = os.environ["LANGCHAIN_PROJECT"]

client = Client(api_key=api_key)


import os
import time

time.sleep(10)

openai_key = os.environ["OPENAI_API_KEY"]
ollama_host = os.environ["OLLAMA_HOST"]
es_host = os.environ["ES_HOST"]
es_password = os.environ["ELASTIC_PASSWORD"]
embedding_model = os.environ["EMBEDDING_MODEL"]


llm = ChatOpenAI(model="gpt-4o-mini")

# Initialize the Elasticsearch vector store for embedding and retrieval
elasticsearch_client = ElasticsearchStore(
    es_url="http://" + es_host + ":9200",
    index_name="smart-search",
    embedding=OllamaEmbeddings(model=embedding_model, base_url="http://" + ollama_host + ":11434"),
    es_user="elastic",
    es_password=es_password
    )


prompt_template = PromptTemplate.from_template(
'''You are a helpful, smart, kind, and efficient AI assistant. You always fulfill the user's requests to the best of your ability, even when the context provided does not help you with the users request, in that case you apply your general knowledge, even when it risks giving an inaccurate answer.

Context:
{context}

Question:
{question}
''')

retriever = elasticsearch_client.as_retriever(
        search_kwargs={'k': 3},
    )


def format_docs(docs):

    return "\n\n".join(doc.page_content for doc in docs)

@traceable
def model_predict(question: str):


    rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt_template
            | llm
            | StrOutputParser()
    )
    response = rag_chain.invoke(question)

    return response



app = Flask(__name__)
    
@app.route("/v1/chat", methods=['POST']) 
def chat_openai():
    if request.method == 'POST':
        # Parse the JSON request body
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "Missing 'query' in request body"}), 400

        question = data['query']
        response = model_predict(question)



        # Return the documents as a JSON response
        return jsonify(response)
    



if __name__ == '__main__':
    app.run(debug=True,port=7000,use_reloader=False)