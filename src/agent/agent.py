from typing import List

from src.agent.modules.core import Strategist, Tactician, Runner, Critic
from src.agent.modules.environment.perception.perceptor import Perceptor
from src.agent.modules.environment.actuation.actuator import Actuator
from src.agent.modules.nl_processor import LocalLLMClient
from src.agent.state import Outcome, State
from src.agent.modules.memory.memory import Memory


# Using mock until integration with Strategist module is complete
def goal_condition_mock(state: State) -> bool:
    return state.outcome == Outcome.WIN


class Agent:
    def __init__(self, baba_host_url: str, llm_host_url: str):
        self.memory = Memory()
        self.perceptor = Perceptor(baba_host_url=baba_host_url)
        self.actuator = Actuator(baba_host_url=baba_host_url)

        self.runner = Runner(
            llm_client=LocalLLMClient(llm_host_url=llm_host_url), memory=self.memory
        )
        self.critic = Critic(
            llm_client=LocalLLMClient(llm_host_url=llm_host_url), memory=self.memory
        )
        self.tactician = Tactician(
            state_transition_function=self.runner.run,
            goal_condition_function=goal_condition_mock,
        )
        # self.strategist = Strategist()  # To be integrated later

    def run(
        self, load_stored_beliefs: bool = True, load_stored_step_function: bool = True
    ) -> List:
        print("Running Agent...")

        if load_stored_beliefs:
            self.memory.load_beliefs()
        if load_stored_step_function:
            self.memory.load_step_function()

        while True:
            initial_state = self.perceptor.get_state()
            self.critic.infer_player_and_win_condition(initial_state)
            self.runner.update_step_function_with_new_belief(
                str(self.memory.rule_beliefs)
            )

            action_list = self.tactician.plan(start_state=initial_state, max_depth=10)
            real_state = self._execute_action_sequence(initial_state, action_list)

            if real_state.outcome == Outcome.WIN:
                break

        print("Final action sequence:", action_list)
        return action_list

    def _execute_action_sequence(
        self, initial_state: State, action_list: List
    ) -> State:
        simulated_state = initial_state
        real_state = initial_state

        for action in action_list:
            previous_state = simulated_state
            simulated_state = self.runner.run(previous_state, action)
            self.actuator.send_action(action)
            real_state = self.perceptor.get_state()

            if simulated_state != real_state:
                simulated_state = self._update_beliefs_on_mismatch(
                    action, previous_state, simulated_state, real_state
                )
                self.actuator.undo_actions(1)
                self.actuator.send_action(action)

        return real_state

    def _update_beliefs_on_mismatch(
        self, action, previous_state: State, simulated_state: State, real_state: State
    ) -> State:
        new_belief = self.critic.analyze_single(
            action=action.name,
            previous=previous_state,
            simulated=simulated_state,
            real=real_state,
        )
        self.runner.update_step_function_with_new_belief(str(new_belief))
        simulated_state = self.runner.run(previous_state, action)

        while simulated_state != real_state:
            self.runner.update_step_function_with_incorrect_state_transition(
                previous_state, simulated_state, real_state
            )
            simulated_state = self.runner.run(previous_state, action)

        return simulated_state
