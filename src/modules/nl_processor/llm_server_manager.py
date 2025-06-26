import os
import subprocess
import sys
import time
import requests


class LLMServerManager:
    """
    Responsible for starting, checking, and stopping the LLM server.
    """

    def __init__(
            self,
            models_path="models/",
            model_name="Mistral-Nemo-Instruct-2407-Q5_K_M",
            loader="llama.cpp",
            server_path="llm_backend/text-generation-webui/",
            host="http://localhost:5000"
    ):
        self.models_path = models_path
        self.model_name = model_name
        self.loader = loader
        self.server_path = server_path
        self.api_url = f"{host}/v1/completions"
        self.process = None

    def is_server_running(self):
        try:
            r = requests.post(self.api_url, json={"prompt": "1", "max_tokens": 1}, timeout=2)
            return r.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def start_server(self):
        print("🔄 Starting LLM server...")

        bat_file = os.path.join(self.server_path, "start_windows.bat")
        self.process = subprocess.Popen(
            f'{bat_file} --model-dir "{self.models_path}" --model "{self.model_name}" --loader "{self.loader}" --api',
            shell=True,
            cwd=self.server_path,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        return self.wait_until_ready()

    def wait_until_ready(self, timeout=30):
        print("⏳ Waiting for server to become ready...")
        for _ in range(timeout):
            if self.is_server_running():
                print("✅ Server is ready!")
                return True
            time.sleep(1)
        print("❌ Server did not start in time.")
        return False

    def ensure_running(self):
        if self.is_server_running():
            print("✅ Server is already running.")
            return True
        return self.start_server()
