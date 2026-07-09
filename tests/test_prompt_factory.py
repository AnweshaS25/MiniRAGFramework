from src.factories.prompt_template_factory import PromptTemplateFactory
from src.constants import PromptTemplateTypes

templates = [
    PromptTemplateTypes.DEFAULT,
    PromptTemplateTypes.CONCISE,
    PromptTemplateTypes.SUMMARY,
    PromptTemplateTypes.CITATION,
]

for template in templates:

    prompt = PromptTemplateFactory.create(template)

    print("-" * 40)
    print(template)
    print(type(prompt).__name__)