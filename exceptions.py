class EnvironmentUnsetError(Exception):
    def __init__(self, *variables):
        self.variables = variables

    def __str__(self):
        return f"Environment variable(s) not set: {repr(self.variables)}"
