import copy
from typing import Callable, Optional, List
from collections import deque

from src.agent.modules.core.planner.base import Planner
from src.agent.state import State, Action


class BFSPlanner(Planner):

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
        visited: set[State] = set()

        # Each element in queue is (current_state, path_taken)
        queue.append((start_state, []))
        visited.add(start_state)

        print(f"[Tactician] Computing plan...")

        while queue:
            current_state, trajectory = queue.popleft()
            action_list = [action for state, action in trajectory]

            # print(repr(current_state))
            # print(current_state.kind_to_properties)
            # print("ACTIONS: " + str(action_list))
            #print("STATE: " + str(start_state))
            #print("STATE: " + str(current_state))

            # Check if goal reached
            if self.goal_condition_function(trajectory, current_state):
                print(
                    f"[Tactician] Concluded plan: {action_list}"
                )
                return [action for state, action in trajectory]

            # Depth check
            if max_depth is not None and len(trajectory) >= max_depth:
                continue

            # Explore neighbors
            for action in Action:
                next_state = copy.deepcopy(current_state)
                next_state = self.state_transition_function(next_state, action)
                # print(next_state)
                # print(next_state.kind_to_properties)

                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, trajectory + [(current_state, action)]))

        return None
