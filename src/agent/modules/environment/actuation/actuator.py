from src.agent.modules.environment.baba_client import BABAClient
from src.agent.state.actions import Action


class Actuator:
    def __init__(self, baba_host_url: str):
        self.client = BABAClient(base_url=baba_host_url)

    def send_action(self, action: Action) -> None:
        self.send_actions([action])

    def send_actions(self, actions: list[Action]) -> None:
        actions_str = ",".join(map(lambda a: a.name.lower(), actions))
        print(f"Sending actions: {actions_str}")
        self.client.execute_commands(actions_str)

    def undo_actions(self, num_actions: int) -> None:
        self.client.undo_multiple(num_actions)

    def restart_level(self) -> None:
        self.client.execute_commands("restart_instant")
