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
            llm_client=LocalLLMClient(base_url=llm_host_url), memory=self.memory
        )
        self.critic = Critic(
            llm_client=LocalLLMClient(base_url=llm_host_url), memory=self.memory
        )
        self.tactician = Tactician(
            state_transition_function=self.runner.run,
            goal_condition_function=goal_condition_mock,
        )
        # self.strategist = Strategist()  # To be integrated later

    def run(
        self, baba_map_id: int, load_stored_beliefs: bool = True, load_stored_step_function: bool = True
    ) -> List:
        print(f"Running Agent for map ID {baba_map_id}...")
        self.actuator.load_level(baba_map_id)

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
        self, initial_state: State, action_list: list
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
        """
        This function is called when a contradiction (belief mismatch) is detected.
        """

        # 1. Get New Knowledge
        new_belief = self.critic.analyze_single(
            action=action.name,
            previous=previous_state,
            simulated=simulated_state,
            real=real_state,
        )

        # 2. Generate new Code
        self.runner.update_step_function_with_new_belief(str(new_belief))

        # 3. Test the New Code
        current_simulated_state = self.runner.run(previous_state, action)

        # 4. Code Debug Loop
        max_debug_attempts = 5
        debug_attempts = 0

        while current_simulated_state != real_state:
            # Check if the Coder LLM is stuck.
            if debug_attempts >= max_debug_attempts:
                print(f"CRITICAL: Failed to debug step function for belief: {new_belief}")
                print("This rule is likely flawed, contradictory, or impossible.")
                raise Exception("Code debug loop failed. Knowledge is likely flawed.")

            print(f"Debug attempt {debug_attempts + 1}: Code is buggy. Retrying...")

            self.runner.update_step_function_with_new_belief(
                belief_to_implement=str(new_belief),
                previous_state=previous_state,
                action=action,
                failed_state=current_simulated_state,
                correct_state=real_state
            )

            debug_attempts += 1

            # 5. Re-test the newly fixed code
            current_simulated_state = self.runner.run(previous_state, action)

        # If we exit the loop, it means:
        # current_simulated_state == real_state
        return current_simulated_state
