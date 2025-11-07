import os
import threading
from pathlib import Path
from time import sleep

from dotenv import load_dotenv

from src.agent.modules.environment.actuation.actuator import Actuator
from src.agent.state import Action
from src.api.app import app
from src.agent.agent import Agent

load_dotenv()

BABA_COMMANDS_DIR = Path(os.getenv("BABA_COMMANDS_DIR"))
BABA_LOCALHOST_PORT = int(os.getenv("BABA_LOCALHOST_PORT"))
LLM_HOST_ADDRESS = os.getenv("LLM_HOST_ADDRESS")

LEVELS_TO_TEST = {
    "BABA IS YOU": 0,
    "WHERE DO I GO?": 1,
    "NOW WHAT IS THIS": 189,
    "OUT OF REACH": 3,
    "STILL OUT OF REACH": 2,
    "VOLCANO": 90,
    "OFF LIMITS": 5,
    "GRASS YARD": 6
}

def run_baba_api():
    app.run(host="localhost", port=BABA_LOCALHOST_PORT, debug=False)

if __name__ == "__main__":

    baba_api_thread = threading.Thread(target=run_baba_api, daemon=True)
    baba_api_thread.start()

    print("Waiting for baba api to start...")
    sleep(3)

    agent = Agent(f"http://localhost:{BABA_LOCALHOST_PORT}", llm_host_url=LLM_HOST_ADDRESS)
    agent.run(baba_map_id=0, load_stored_beliefs=False, load_stored_step_function=False)

    for map_id in list(LEVELS_TO_TEST.values())[:1]:
        agent.run(baba_map_id=map_id, load_stored_beliefs=True, load_stored_step_function=True)
