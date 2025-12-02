import copy
import itertools
from typing import Optional, List, Set, Tuple, Callable
from collections import deque

# Assuming these are available from your project structure
from src.agent.modules.core.planner.base import Planner
from src.agent.state import State, Action


class IWPlanner(Planner):
    """
    Standard Iterated Width (IW) Planner.

    This planner attempts to solve the problem using IW(1).
    If that fails, it escalates to IW(2).

    Algorithm:
    1. Breadth-First Search.
    2. Pruning: A state is kept ONLY if it generates a new tuple of atoms (features)
       of size 'width' that has never been seen in the entire search history.
    """

    def plan(
            self, start_state: State, max_depth: Optional[int] = None
    ) -> Optional[List[Action]]:
        """
        Attempts to solve with increasing widths.
        """
        # 1. Try IW(1) - Fast exploration (Single atoms)
        solution = self._solve_iw(start_state, width=1, max_depth=max_depth)
        if solution:
            return solution

        # 2. Try IW(2) - Interaction discovery (Pairs of atoms)
        # Only runs if IW(1) fails.
        solution = self._solve_iw(start_state, width=3, max_depth=max_depth)
        return solution

    def _solve_iw(
            self, start_state: State, width: int, max_depth: Optional[int]
    ) -> Optional[List[Action]]:
        """
        Runs the search for a specific width 'k'.
        """
        # Queue stores: (Current State, Path taken)
        queue = deque([(start_state, [])])

        # The Global Memory for Standard IW.
        # Stores tuples of atoms found so far.
        # For IW(1), it stores { ("baba", 1, 1), ... }
        # For IW(2), it stores { (("baba",1,1), ("rock",2,2)), ... }
        seen_features: Set[Tuple] = set()

        # Initialize memory with the start state features
        start_atoms = self._get_atoms(start_state)
        self._register_features(seen_features, start_atoms, width)

        while queue:
            current_state, path = queue.popleft()

            # 1. Check Max Depth
            if max_depth is not None and len(path) > max_depth:
                continue

            # 2. Check Goal Condition
            # Passing empty list for history as usually only current state matters for is_win
            if self.goal_condition_function([], current_state):
                return path

            # 3. Expand Actions
            # Iterating over the Enum Action (assuming Action is an Enum)
            for action in Action:
                # Apply the transition
                next_state = copy.deepcopy(current_state)
                next_state = self.state_transition_function(next_state, action)

                # 4. Standard IW Pruning Logic
                next_atoms = self._get_atoms(next_state)

                # Check if this state provides ANY new feature tuple of size 'width'
                is_novel = self._check_novelty_and_register(seen_features, next_atoms, width)

                if is_novel:
                    queue.append((next_state, path + [action]))

        return None

    def _get_atoms(self, state: State) -> Set[Tuple]:
        """
        Extracts atoms from the state.
        Atom structure: (Block_Kind, X, Y)
        """
        atoms = set()
        # Iterate through the grid 3D array: list[list[list[Block]]]
        for x, row in enumerate(state.grid):
            for y, cell in enumerate(row):
                if cell:
                    for block in cell:
                        # An atom represents a physical fact in the world
                        atoms.add((block.kind, block.x, block.y))
        return atoms

    def _register_features(self, seen_set: Set[Tuple], atoms: Set[Tuple], width: int):
        """
        Helper to add all combinations of size 'width' to the seen set.
        Used for initialization.
        """
        for combination in itertools.combinations(atoms, width):
            # Sort the combination to ensure set-like behavior
            # (Atom A, Atom B) is the same as (Atom B, Atom A)
            feature_key = tuple(sorted(combination))
            seen_set.add(feature_key)

    def _check_novelty_and_register(
            self, seen_set: Set[Tuple], atoms: Set[Tuple], width: int
    ) -> bool:
        """
        Checks if the set of atoms contains at least one combination of size 'width'
        that is NOT in 'seen_set'.

        If found, it adds the new combinations to 'seen_set' and returns True.
        """
        is_novel = False

        # Iterate over all possible combinations of size 'width'
        for combination in itertools.combinations(atoms, width):
            feature_key = tuple(sorted(combination))

            if feature_key not in seen_set:
                # We found a new feature! This state is novel.
                is_novel = True
                seen_set.add(feature_key)

        # In Standard IW, we update the seen set with the new features found
        # and accept the state. If no new features were found, the state is pruned.
        return is_novel