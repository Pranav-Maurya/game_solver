import cv2
import numpy as np
import math

class ArrowDetector:
    """
    Detects the direction of an arrow piece by analyzing its contour.
    A puzzle piece has a distinct arrowhead which is typically at one extreme end
    of the continuous shape. The arrowhead is wider than the standard line thickness.
    """
    @staticmethod
    def detect(contour) -> str:
        # Approximate the contour to a polygon to reduce vertices
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Get bounding box to know the general flow
        x, y, w, h = cv2.boundingRect(contour)

        # Create a small mask of just the contour to use morphological operations or corner detection
        # To find the arrowhead, we can look for the "pointiest" part of the shape, or the widest part at the end.

        # A simpler heuristic for this specific game:
        # The game pieces are made of straight lines (horizontal/vertical) and 90-degree bends.
        # The arrowhead itself is a triangle at the end of a segment.
        # Let's find the convex hull. The tip of the arrow will always be a vertex on the convex hull.
        hull = cv2.convexHull(approx, returnPoints=True)

        # Find the sharpest angle on the hull, which typically corresponds to the arrow tip.
        min_angle = 180
        tip = None

        if len(hull) >= 3:
            for i in range(len(hull)):
                p1 = hull[i-1][0]
                p2 = hull[i][0]
                p3 = hull[(i+1)%len(hull)][0]

                # Vector p2 -> p1
                v1 = (p1[0] - p2[0], p1[1] - p2[1])
                # Vector p2 -> p3
                v2 = (p3[0] - p2[0], p3[1] - p2[1])

                # Calculate angle between vectors using dot product
                dot = v1[0]*v2[0] + v1[1]*v2[1]
                mag1 = math.hypot(v1[0], v1[1])
                mag2 = math.hypot(v2[0], v2[1])

                if mag1 > 0 and mag2 > 0:
                    cos_theta = max(min(dot / (mag1 * mag2), 1.0), -1.0)
                    angle = math.degrees(math.acos(cos_theta))

                    if angle < min_angle:
                        min_angle = angle
                        tip = p2

        # If we found a sharp tip (usually < 60 degrees for an arrowhead)
        # we can determine direction based on where the mass of the piece is relative to the tip.
        if tip is not None and min_angle < 85:
            # Calculate centroid
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                dx = tip[0] - cx
                dy = tip[1] - cy

                if abs(dx) > abs(dy):
                    if dx > 0:
                        return "RIGHT"
                    else:
                        return "LEFT"
                else:
                    if dy > 0:
                        return "DOWN"
                    else:
                        return "UP"

        # Fallback heuristic: check which side touches the bounding box max/min
        return "UNKNOWN"
