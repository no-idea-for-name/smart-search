import requests


def load_initial_documents():

    response = requests.get(
                url="http://knowledge-manager:6000/v1/init")
