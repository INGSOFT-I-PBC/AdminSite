
class ParamNotFoundError(Exception):
    pass


class ParamTypeMatchError(TypeError):
    pass


class Validator:
    """
    Builds a new Validator for an HTTP requests.
    """

    def add_field(self, field_name:str, field_type = str):

        pass
