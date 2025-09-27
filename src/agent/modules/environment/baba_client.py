import requests


class BABAClient:
    def __init__(self, base_url="http://localhost:5000", token=None):
        """
        base_url: e.g. 'http://localhost:6277'
        token: Optional Bearer token for Authorization header if required
        """
        self.base_url = base_url.rstrip("/")
        self.token = token

    def _headers(self):
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        headers["Content-Type"] = "application/json"
        return headers

    def game_rules(self, topic="basic"):
        url = f"{self.base_url}/game_rules"
        payload = {"topic": topic}
        response = requests.get(url, params=payload, headers=self._headers())
        return response.text

    def enter_level(self, level):
        url = f"{self.base_url}/enter_level"
        payload = {"level": level}
        response = requests.post(url, json=payload, headers=self._headers())
        return response.text

    def get_game_state(self):
        url = f"{self.base_url}/game_state"
        response = requests.get(url, headers=self._headers())
        return response.text[5:-6]

    def execute_commands(self, commands):
        url = f"{self.base_url}/execute_commands"
        payload = {"commands": commands}
        response = requests.post(url, json=payload, headers=self._headers())
        return response.text

    def undo_multiple(self, n):
        url = f"{self.base_url}/undo_multiple"
        payload = {"n": n}
        response = requests.post(url, json=payload, headers=self._headers())
        return response.text

    def restart_level(self):
        url = f"{self.base_url}/restart_level"
        response = requests.post(url, headers=self._headers())
        return response.text

    def leave_level(self):
        url = f"{self.base_url}/leave_level"
        response = requests.post(url, headers=self._headers())
        return response.text
