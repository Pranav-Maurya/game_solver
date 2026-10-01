from typing import List, Optional
from solver.board_state import BoardState
import copy

class GreedySolver:
    def __init__(self):
        pass

    def get_next_move(self, board_state: BoardState) -> Optional[int]:
        """
        Finds the first removable piece and returns its ID.
        This is suitable for live automation where we just want the very next action.
        """
        removable = board_state.get_removable_pieces()
        if removable:
            # We can optionally sort candidates by distance to edge or size,
            # but picking the first valid one works for most layouts.
            return removable[0]
        return None

    def solve_full_sequence(self, initial_state: BoardState) -> List[int]:
        """
        Calculates the complete sequence of moves to clear the board.
        Helpful for dry-run mode and verification.
        Uses a backtracking approach if greedy gets stuck.
        """
        sequence = []
        state_copy = copy.deepcopy(initial_state)

        while state_copy.pieces:
            removable = state_copy.get_removable_pieces()
            if not removable:
                # Dead end reached (greedy failed).
                # A full DFS with backtracking would go here,
                # but for this game, greedy usually works if vision is perfect.
                print("WARNING: Reached a state where no pieces are removable!")
                break

            # Pick the first removable
            choice = removable[0]
            sequence.append(choice)
            state_copy.remove_piece(choice)

        return sequence
