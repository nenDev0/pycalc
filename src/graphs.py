
from src.calculations import read_term
from src.log import log
from math import ceil,sqrt

class Graph():

    def __init__(self):
        self.constants = 0.0
        self.points = []
        self.function = None


    def get_function(self):
        return self.function

    def set_function(self, function: str):
        self.points.clear()
        function = function.replace(" ", "", -1)
        function = function.replace("--", '', -1)
        function = function.replace("-", "+-", -1)
        function = function.replace("(+-", "(-", -1)
        function = function.replace("=+-", "=-", -1)

        function = function.lower()
        self.function = function
        return

    def get_points(self):
        return self.points


    def calculate_point(self, x: float, begin) -> tuple:
        function = self.function
        
        #if x<0:
        #    function = function.replace("-x",str(-x))
        function = function.replace("x",str(x))

        left, right = function.split("=")
        log.debug(f'{left} left, right {right}')

        y = read_term(right)
        if y == None:
            return None
        return (x, float(y))


    def calculate_interval(self, x_1: int, x_2: int, zoom: int, begin: bool):
        delta_x = x_2 - x_1
        new_points = []
        log.debug(f'delta_x, zoom: {delta_x*zoom}')
        log.debug(f'x_1 x_2 {x_1}, {x_2}')

        for x in range(int(delta_x*zoom)):
            data = self.calculate_point(x_1+x/zoom, begin)
            log.debug(f'data: {data}')
            if data == None:
                continue
            new_points.append(data)
        if begin:
            log.debug(f'begin: {(new_points[0], new_points[-1])}')
            new_points.extend(self.points)
            self.points = new_points
        else:
            log.debug(f'end: {(new_points[0], new_points[-1])}')
            self.points.extend(new_points)
        return
