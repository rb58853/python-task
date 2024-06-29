import functools

class chain_rules:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.rules = []

    def __call__(self, *args, **kwargs):
        # Aplicamos las reglas al primer argumento, que esperamos sea una cadena
        chain = args[0]  # Por ejemplo, convertimos la cadena a mayúsculas

        # Llamamos a la función original con el argumento modificado
        return self.func(chain)

    