class Evaluator:
    """
    Compares benchmark results
    between multiple frameworks.
    """

    def __init__(self):

        self.results = {}

    def add_result(
        self,
        framework_name: str,
        summary: dict,
    ):

        self.results[framework_name] = summary

    def compare(self):

        return self.results