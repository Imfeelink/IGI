from abc import ABC, abstractmethod
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class FigureColor:
    """
    Class representing the color of a geometric figure.
    Uses properties to validate and store the color string.
    """
    def __init__(self, color_name: str):
        self.color = color_name

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val: str):
        """
        setter checks if color value is correct
        """
        #isalpha returns true if string contains only letters without other symbols and spaces
        if not isinstance(val, str) or not val.isalpha():
            raise ValueError("Color should contain only letters!")
        self._color = val


class GeometricFigure(ABC):
    """
    Abstract base class for all geometric figures.
    Declares static attributes, class methods and abstract methods.
    """
    figure_name = "Undefined figure"

    def __init__(self):
        pass

    @classmethod
    def get_figure_name(cls) -> str:
        return cls.figure_name

    @abstractmethod
    def calculate_area(self) -> float:
        pass


class Square(GeometricFigure):
    """
    Class representing a square circumscribed around a circle of radius R.
    Inherits from GeometricFigure and demonstrates polymorphism.
    """
    #class attribute
    figure_name = "Square"

    def __init__(self, r: float, color_name: str):
        self.r = r
        self.color_obj = FigureColor(color_name)

    @property
    def r(self):
        return self._r
    
    @r.setter
    def r(self, val):
        try:
            radius_float = float(val)
        except ValueError:
            raise ValueError("Radius should be a number!")
        if radius_float < 0:
            raise ValueError("Radius must be greater than 0")
        self._r = radius_float


    def calculate_area(self) -> float:
        """
        Returns area of square circumscribed around a circle
        """
        return 4 * math.pow(self.r, 2)

    #format
    def get_info(self) -> str:
        """
        Returns string with info about square
        """
        info_string = "Figure: {0}. Radius: {1}. Color: {2}. Area: {3:.2f}."
        return info_string.format(
            self.get_figure_name(),
            self.r,
            self.color_obj.color,
            self.calculate_area()
        )

def repeat_run(func):
    '''decorator:
    gets function, launches it and asking user if he needs to launch program again
    uses decorator'''
    def wrapper(*args, **kwargs):
        while True:
            func(*args, **kwargs)

            answer = input("Wanna launch program again(y - yes, n - no): ").strip().lower()
            if(answer == 'yes' or answer == 'y'):
                continue
            elif(answer == 'no' or answer == 'n'):
                break
            else:
                break
    return wrapper