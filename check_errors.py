def check_steps_error(value):
    if type(value) != int:
        raise TypeError(f'Steps must be an intiger: {value}')
    elif value <= 0:
        raise ValueError(f'Steps must be positive: {value}')


def check_time_error(value):
    if type(value) != float and type(value) != int:
        raise TypeError(f'Time must be float or intiger: {value}')
    elif value <= 0:
        raise ValueError(f'Time must be positive: {value}')