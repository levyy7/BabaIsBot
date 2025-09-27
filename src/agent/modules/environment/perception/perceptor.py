from src.agent.modules.environment.baba_client import BABAClient
from src.agent.state.state import State


class Perceptor:
    def __init__(self, baba_host_url: str):
        self.client = BABAClient(base_url=baba_host_url)

    def get_state(self) -> State:
        state_str = self.client.get_game_state()
        print(state_str)
        state = State.from_grid_string(state_str)
        return state
