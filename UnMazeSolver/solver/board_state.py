import cv2
import numpy as np
from typing import List
from vision.piece_detector import Piece

class BoardState:
    def __init__(self, width: int, height: int, pieces: List[Piece]):
        self.width = width
        self.height = height
        self.pieces = {p.id: p for p in pieces}
        # Create a global occupancy mask to speed up collision detection
        # 0 = empty, 255 = occupied
        self.global_mask = np.zeros((height, width), dtype=np.uint8)
        for piece in pieces:
            # Add piece mask to global mask
            self.global_mask = cv2.bitwise_or(self.global_mask, piece.mask)

    def is_piece_blocked(self, piece: Piece) -> bool:
        """
        Determines if a piece is blocked from leaving the board.
        A piece is blocked if its required movement path collides with another piece.
        """
        if piece.direction == "UNKNOWN":
            return True # Can't move if we don't know the direction

        # We simulate moving the piece's mask step by step towards the edge.
        # Since pieces are made of orthogonal segments, we can just sweep the bounding box
        # or sweep the mask itself. Sweeping the mask is more accurate.

        step_size = 10 # Pixels to jump per check

        # Determine the maximum distance it could travel to exit the board
        max_dist = max(self.width, self.height)

        # Create a copy of the global mask WITHOUT the current piece
        # This prevents the piece from colliding with itself
        other_pieces_mask = cv2.bitwise_xor(self.global_mask, piece.mask)

        current_mask = piece.mask.copy()

        # Define movement vector
        dx, dy = 0, 0
        if piece.direction == "RIGHT": dx = step_size
        elif piece.direction == "LEFT": dx = -step_size
        elif piece.direction == "DOWN": dy = step_size
        elif piece.direction == "UP": dy = -step_size

        # Translation matrix
        M = np.float32([[1, 0, dx], [0, 1, dy]])

        for _ in range(0, max_dist, step_size):
            # Move the mask
            current_mask = cv2.warpAffine(current_mask, M, (self.width, self.height))

            # If the mask has moved completely off the board, it's free
            if cv2.countNonZero(current_mask) == 0:
                return False

            # Check for collision with other pieces
            collision = cv2.bitwise_and(current_mask, other_pieces_mask)

            # Allow a tiny margin of error (e.g. 5 pixels overlap)
            # to account for anti-aliasing or pieces touching tightly.
            # If we strictly check > 0, almost all pieces might falsely be "blocked"
            # just by touching a neighboring pixel.
            if cv2.countNonZero(collision) > 15:
                return True # Blocked

        return False

    def get_removable_pieces(self) -> List[int]:
        """Returns a list of piece IDs that are currently unblocked."""
        removable = []
        for piece_id, piece in self.pieces.items():
            if not self.is_piece_blocked(piece):
                removable.append(piece_id)
        return removable

    def remove_piece(self, piece_id: int):
        """Removes a piece from the board state (e.g. after it's clicked)."""
        if piece_id in self.pieces:
            piece = self.pieces.pop(piece_id)
            # Remove from global mask
            self.global_mask = cv2.bitwise_xor(self.global_mask, piece.mask)
