import numpy as np
import math
class ResultVector:
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.z = coords[2]

    def lerp(self, other, t):
        return ResultVector([self.x + t * (other.x - self.x),
                             self.y + t * (other.y - self.y),
                             self.z + t * (other.z - self.z)])

    def distance(self, other):
        return np.sqrt((other.x - self.x)**2 +
                       (other.y - self.y)**2 +
                       (other.z - self.z)**2)

    def subtract(self, other):
        return ResultVector([self.x - other.x,
                             self.y - other.y,
                             self.z - other.z])
    def cross(self, other):
        return ResultVector([self.y * other.z - self.z * other.y,
                             self.z * other.x - self.x * other.z,
                             self.x * other.y - self.y * other.x])
        
    # The length method calculates the length or magnitude of the vector using the Pythagorean theorem. 
    # It is a fundamental operation in vector algebra.
    def length(self):
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)

    def rollPitchYaw(self, p1, p2, p3):
        v1 = p2.subtract(p1)
        x = v1.y
        y = -v1.x
        z = 0
        v2 = p3.subtract(p1)
        v3 = v2.cross(v1)
        return {
            'x': math.atan2(v3.length(), v1.length()),
            'y': math.atan2(v2.length(), v1.length()),
            'z': -math.atan2(y, x)
        }

# replacing "Results" with list for Python
class CalculateHeadPose:
    PI = np.pi

    def createEulerPlane(self, head_coords):
        p1 = ResultVector(head_coords["21"])
        p2 = ResultVector(head_coords["251"])
        p3 = ResultVector(head_coords["397"])
        p4 = ResultVector(head_coords["172"])
        p3mid = p3.lerp(p4, 0.5)

        return {
            'vector': [p1, p2, p3mid],
            'points': [p1, p2, p3, p4]
        }

    def calcHead(self, head_coords):
        plane = self.createEulerPlane(head_coords)['vector']
        rotate = plane[0].rollPitchYaw(plane[0], plane[1], plane[2])
        midPoint = plane[0].lerp(plane[1], 0.5)
        width = plane[0].distance(plane[1])
        height = midPoint.distance(plane[2])

        rotate['x'] *= -1
        rotate['z'] *= -1

        return {
            'x': rotate['x'] * self.PI,
            'y': rotate['y'] * self.PI,
            'z': rotate['z'] * self.PI,
            'width': width,
            'height': height,
            'position': midPoint.lerp(plane[2], 0.5),
            'normalized': {
                'x': rotate['x'],
                'y': rotate['y'],
                'z': rotate['z']
            },
            'degrees': {
                'x': rotate['x'] * 180,
                'y': rotate['y'] * 180,
                'z': rotate['z'] * 180
            }
        }
