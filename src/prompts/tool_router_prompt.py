from src.tools.tool_registry import ToolRegistry


class ToolRouterPrompt:
    """
    Builds the prompt used by the LLM Tool Router.
    """

    @staticmethod
    def build(query: str, registry: ToolRegistry) -> str:

        tool_descriptions = []

        for tool in registry.list_tools():

            tool_descriptions.append(
                f"- {tool.name}: {tool.description}"
            )

        tools = "\n".join(tool_descriptions)

        return f"""
You are a tool routing assistant.

Available tools:

{tools}

Your job is to decide whether a tool should be used.

Rules:

1. Respond ONLY with valid JSON.
2. Do NOT explain your answer.
3. Do NOT write markdown.
4. Do NOT use ```json.
5. Do NOT write any extra text.

If a tool is needed, respond exactly like:

{{
    "tool": "calculator",
    "arguments": {{
        "expression": "3*5"
    }}
}}

If the datetime tool is needed:

{{
    "tool": "datetime",
    "arguments": {{}}
}}

If no tool is required, respond exactly:

null

User Query:

{query}
"""