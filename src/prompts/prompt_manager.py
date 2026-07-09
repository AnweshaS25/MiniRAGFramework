from src.prompt_routing.base_prompt_router import BasePromptRouter
from src.factories.prompt_template_factory import PromptTemplateFactory


class PromptManager:
    """
    Coordinates prompt routing and prompt template creation.
    """

    def __init__(self, router: BasePromptRouter,):

        if router is None:
            raise ValueError("router cannot be None.")

        self.router = router

    def get_prompt_template(self, query: str):

        prompt_request = self.router.route(query)

        if prompt_request is None:
            raise ValueError(
                "Prompt router failed to select a prompt."
            )

        return PromptTemplateFactory.create(
            prompt_request.prompt_type
        )