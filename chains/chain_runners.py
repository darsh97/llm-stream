from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from logger import Logger

logger = Logger()

def create_chain(model, prompt) -> RunnableSequence:
    logger.info(f"Inside create_chain()")
    chain = prompt | model | StrOutputParser()
    logger.info(f"Chain Created")
    return chain
