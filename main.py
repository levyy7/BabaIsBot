import os
import threading
from pathlib import Path
from dotenv import load_dotenv

from src.api.app import app
from src.agent.agent import Agent

load_dotenv()

BABA_COMMANDS_DIR = Path(os.getenv("BABA_COMMANDS_DIR"))
BABA_LOCALHOST_PORT = int(os.getenv("BABA_LOCALHOST_PORT"))
LLM_HOST_ADDRESS = os.getenv("LLM_HOST_ADDRESS")


def delete_commands_from_command_dir():
    for item in BABA_COMMANDS_DIR.iterdir():
        if item.is_file() or item.is_symlink():
            item.unlink()  # delete file or symlink

def run_baba_api():
    app.run(host="localhost", port=BABA_LOCALHOST_PORT, debug=False)


if __name__ == "__main__":
    delete_commands_from_command_dir()

    baba_api_thread = threading.Thread(target=run_baba_api, daemon=True)
    baba_api_thread.start()

    agent = Agent(baba_host_url=f"http://localhost:{BABA_LOCALHOST_PORT}", llm_host_url=LLM_HOST_ADDRESS)
    agent.run(load_stored_beliefs=False, load_stored_step_function=False)

    delete_commands_from_command_dir()
