from typing import Callable, Optional, List
from collections import deque

from src.agent.state import State, Action


class Tactician:

    def __init__(
        self,
        state_transition_function: Callable[[State, Action], State],
        goal_condition_function: Callable[[State], bool],
    ):
        self.state_transition_function = state_transition_function
        self.goal_condition_function = goal_condition_function

    def plan(
        self, start_state: State, max_depth: Optional[int] = None
    ) -> Optional[List[Action]]:
        """
        Performs a BFS search starting from `start_state` using the provided `actions`.
        Returns the sequence of actions to reach the goal, or None if not found.

        :param start_state: The initial State object.
        :param max_depth: Optional depth limit to prevent infinite loops.
        """
        queue = deque()
        visited: Set[State] = set()

        # Each element in queue is (current_state, path_taken)
        queue.append((start_state, []))
        visited.add(start_state)

        print(f"[Tactician] Computing plan...")

        while queue:
            current_state, path = queue.popleft()

            # print(repr(current_state))
            # print(current_state.kind_to_properties)
            # print("ACTIONS: " + str(path))
            # print("STATE: " + str(start_state))
            # print("STATE: " + str(current_state))

            # Check if goal reached
            if self.goal_condition_function(current_state):
                print(
                    f"[Tactician] Concluded plan: {list(map(lambda a: a.name, path))}"
                )
                return path

            # Depth check
            if max_depth is not None and len(path) >= max_depth:
                continue

            # Explore neighbors
            for action in Action:
                next_state = self.state_transition_function(current_state, action)
                # print(next_state)
                # print(next_state.kind_to_properties)

                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, path + [action]))

        return None
