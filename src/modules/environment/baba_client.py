import requests

class BABAClient:
    BASE_URL = "http://localhost:8000"

    @staticmethod
    def get(endpoint, **kwargs):
        url = f"{BABAClient.BASE_URL}{endpoint}"
        response = requests.get(url, **kwargs)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def post(endpoint, data=None, **kwargs):
        url = f"{BABAClient.BASE_URL}{endpoint}"
        response = requests.post(url, json=data, **kwargs)
        response.raise_for_status()
        return response.json()
