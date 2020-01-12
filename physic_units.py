class PositiveFloat(float):

    def __init__(self, value, unit_type):
        if type(value) != int and type(value) != float:
            raise TypeError(f'{unit_type} must be intiger or float: {value}')
        elif value <= 0:
            raise ValueError(f'{unit_type} must be positive: {value}')
        super().__init__()


class Mass(PositiveFloat):

    def __init__(self, value):
        super().__init__(value, 'Mass')


class Radius(PositiveFloat):

    def __init__(self, value):
        super().__init__(value, 'Radius')


class Time(PositiveFloat):

    def __init__(self, value):
        super().__init__(value, 'Time')


class PositiveInt(int):

    def __init__(self, value, unit_type):
        if type(value) != int:
            raise TypeError(f'{unit_type} must be an intiger: {value}')
        elif value <= 0:
            raise ValueError(f'{unit_type} must be positive: {value}')
        super().__init__()


class Steps(PositiveInt):

    def __init__(self, value):
        super().__init__(value, 'Steps')
