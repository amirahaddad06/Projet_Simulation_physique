from vector3D import Vector3D
from abc import ABC, abstractmethod

class Force(ABC):
    @abstractmethod
    def appliquer(self, objet):
        pass

class Gravite(Force):
    def __init__(self, direction=Vector3D(0, -1, 0), g=9.81):
        self.direction = direction.norm()
        self.g = g

    def appliquer(self, objet):
        return self.direction * (objet.mass * self.g)
