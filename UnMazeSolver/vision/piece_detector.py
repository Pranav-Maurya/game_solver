import cv2
import numpy as np
from dataclasses import dataclass
from typing import Tuple, List
from vision.arrow_detector import ArrowDetector

@dataclass
class Piece:
    id: int
    direction: str  # 'UP', 'DOWN', 'LEFT', 'RIGHT', 'UNKNOWN'
    center: Tuple[int, int]
    bbox: Tuple[int, int, int, int] # x, y, w, h
    contour: np.ndarray
    mask: np.ndarray # The binary mask of the piece

class PieceDetector:
    def __init__(self):
        pass

    def detect_pieces(self, preprocessed_image, original_image=None) -> List[Piece]:
        """
        Finds all pieces on the board using connected components.
        Because each puzzle piece is a continuous black path,
        a single connected component represents a single piece.
        """
        if preprocessed_image is None:
            return []

        # Find connected components (contours)
        contours, _ = cv2.findContours(preprocessed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        pieces = []
        piece_id = 0

        # We will filter out very small contours that might be noise or grid dots.
        min_area = 50

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > min_area:
                x, y, w, h = cv2.boundingRect(contour)

                # Calculate the centroid (center of mass) of the contour
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                else:
                    cx, cy = x + w//2, y + h//2

                # Create an isolated mask for just this piece
                mask = np.zeros_like(preprocessed_image)
                cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

                direction = self.detect_direction(contour, mask, (cx, cy))

                piece = Piece(
                    id=piece_id,
                    direction=direction,
                    center=(cx, cy),
                    bbox=(x, y, w, h),
                    contour=contour,
                    mask=mask
                )
                pieces.append(piece)
                piece_id += 1

        return pieces

    def detect_direction(self, contour, mask, center) -> str:
        """
        Analyzes the geometry of the piece to find the arrowhead and its direction.
        """
        return ArrowDetector.detect(contour)
