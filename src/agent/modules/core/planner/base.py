from abc import ABC, abstractmethod
from typing import Callable, Optional, List

from src.agent.state import State, Action


class Planner(ABC):

    def __init__(
        self,
        state_transition_function: Callable[[State, Action], State],
        goal_condition_function: Callable[[list[tuple[State, Action]], State], bool],
    ):
        self.state_transition_function = state_transition_function
        self.goal_condition_function = goal_condition_function

    @abstractmethod
    def plan(
        self, start_state: State, max_depth: Optional[int] = None
    ) -> Optional[List[Action]]:
        pass
