from src.prompt_routing.base_prompt_router import BasePromptRouter
from src.factories.prompt_template_factory import PromptTemplateFactory
from src.prompts.prompt_registry import PromptRegistry


class PromptManager:
    """
    Coordinates prompt routing and prompt template creation.
    """

    def __init__(self, router: BasePromptRouter, registry: PromptRegistry,):

        if router is None:
            raise ValueError("router cannot be None.")
        
        if registry is None:
            raise ValueError("registry cannot be None.")

        self.router = router
        self.registry = registry

    def get_prompt_template(self, query: str):

        prompt_request = self.router.route(query)

        if prompt_request is None:
            raise ValueError(
                "Prompt router failed to select a prompt."
            )

        prompt = self.registry.get_prompt(
            prompt_request.prompt_type
        )

        if prompt is None:
            raise ValueError(
                f"Prompt '{prompt_request.prompt_type}' is not registered."
            )

        return prompt