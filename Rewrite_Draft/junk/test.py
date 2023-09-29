from abc import ABC, abstractmethod
 
 
class Polygon(ABC):
 
    # @abstractmethod
    def noofsides(self):
        pass
 
 
class Triangle(Polygon):
 
    # overriding abstract method
    def noofsides(self):
        print("I have 3 sides")


class Pentagon(Polygon):
    pass


poly = Triangle()
poly2 = Pentagon()
poly.noofsides()
poly2.noofsides()