class PromptRegistry:
    """
    Registry for all available prompt templates.
    """

    def __init__(self):
        self._prompts = {}

    def register_prompt(self, prompt):
        """
        Register a prompt template.
        """
        self._prompts[prompt.name] = prompt

    def get_prompt(self, name: str):
        """
        Retrieve a prompt template by name.
        """
        return self._prompts.get(name)

    def list_prompts(self):
        """
        Return all registered prompt templates.
        """
        return list(self._prompts.values())