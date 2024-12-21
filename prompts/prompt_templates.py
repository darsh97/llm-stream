from langchain_core.prompts import PromptTemplate
from .prompts import POEM_GENERATION_PROMPT


def create_poem_prompt_template() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["poem_topic"],
        template=POEM_GENERATION_PROMPT
    )
