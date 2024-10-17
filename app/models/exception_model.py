class UncoveredAreaException(Exception):
    def __init__(self, status_code, uncovered_area):
        self.status_code = status_code
        self.uncovered_area = uncovered_area
        super().__init__()

class UnexpectedGeometryException(Exception):
    def __init__(self, status_code, intersection):
        self.status_code = status_code
        self.intersection = intersection
        super().__init__()