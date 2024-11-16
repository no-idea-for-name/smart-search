#!/bin/bash

# Pull the model
curl http://ollama:11434/api/pull -d "{\"name\":\"$EMBEDDING_MODEL\"}"


# Run Streamlit
flask run