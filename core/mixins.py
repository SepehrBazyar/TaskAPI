class LowerNameMixin:
    """Mixin Class to Add Method for Retrieve Lower Class Name Property"""

    @classmethod
    def lower_name(cls) -> str:
        """Class Method to Returned Lower Case of Class Name for Use in Paths"""

        return cls.__name__.lower()
