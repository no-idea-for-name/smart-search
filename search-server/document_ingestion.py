import requests


def load_initial_documents():

    response = requests.get(
                url="http://knowledge-manager:5000/v1/init")
