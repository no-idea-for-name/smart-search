# smart-search

## Setup:
- go into search-server and run ```docker build -t search-server:0.1.2 .```
- run ```docker-compose up```

## Customization:


ELASTIC_PASSWORD: password for the elasticsearch instance (change in Elasticsearch configuration and Search-Server configuration)


EMBEDDING_MODEL: name of the embedding model to use

LANGCHAIN_API_KEY,LANGCHAIN_TRACING_V2,LANGCHAIN_PROJECT: configure as needed for langsmith tracing



## Roadmap:


Version 1.0.0:
- [ ] finished frontend implementation
- [ ] management for documents/knowledge base to be searched (as separate service or inside of flask app)

