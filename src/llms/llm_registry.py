class LLMRegistry:
    """
    Registry for all available LLM plugins.
    """

    def __init__(self):
        self._llms = {}

    def register_llm(self, name: str, llm):

        self._llms[name] = llm

    def get_llm(self, name: str):

        return self._llms.get(name)

    def list_llms(self):

        return self._llms
    

    def list_metadata(self):
        """
        Returns metadata for all registered LLM plugins.
        """

        return [
            llm.metadata
            for llm in self._llms.values()
        ]