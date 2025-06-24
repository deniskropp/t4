# sample_code.py

class If:
    """A simple class to represent an If condition."""
    def __init__(self, condition):
        self.condition = condition
        self.default_value = 42

    def __repr__(self):
        return f"If({self.condition})"


def calculate(a, b, c=None):
    if (isinstance(c, If)):
        return a * b if c.condition else c.default_value

    return a + b

# TODO: Add more functions and documentation.
