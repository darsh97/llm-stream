from config import Config
from prompts.prompt_templates import create_poem_prompt_template
from chains.chain_runners import create_chain
from models.gemini_wrapper import GeminiWrapper
from langchain_core.runnables import Runnable
from fastapi import APIRouter, Query, Path
from typing import Mapping, Any
from fastapi.responses import StreamingResponse, JSONResponse
from logger import Logger


logger = Logger()
router = APIRouter()


def chain_runner(invocation_type: str, input: Mapping[str, Any], chain: Runnable):
    assert invocation_type in ("stream", "non-stream")
    if "non-stream" in invocation_type:
        return chain.invoke(input)  # `chain.invoke()` calls GeminiWrapper's `_call()`
    else:
        yield from chain.stream(input)  # `chain.stream()` calls GeminiWrapper's `_stream()`


# Root Endpoint to describe the service
@router.get("/", tags=["root"])
def root():
    """
    Welcome message to the root of the API.
    """
    return {"message": "Welcome"}


# FastAPI route for `/message`
@router.get("/generate/{poem_topic}")
def message_endpoint(
        poem_topic: str = Path(..., description="The topic of the poem to generate."),
        stream: bool = Query(False, description="Enable or disable streaming output.")
):
    """
    Endpoint to fetch model-generated output.
    - If `stream=True`, streams the output chunks.
    - If `stream=False`, returns the output as a single JSON response.
    """
    # Set up the chain and chain input based on the `main()` logic
    model = GeminiWrapper(model_name=Config.MODEL, api_key=Config.GEMINI_API_KEY)
    chain = create_chain(prompt=create_poem_prompt_template(), model=model)
    chain_input = dict(poem_topic=poem_topic)

    # Determine invocation type based on `stream` query parameter
    invocation_type = ("non-stream", "stream")[stream]
    logger.info(f"Invocation type: {invocation_type}")

    if invocation_type == "stream":
        # Return a StreamingResponse for streaming output
        stream_output = chain_runner(invocation_type="stream", input=chain_input, chain=chain)
        return StreamingResponse(stream_output,
                                 media_type="text/event-stream")

    else:
        # Return JSON response for non-streaming output
        output = chain_runner(invocation_type="non-stream", input=chain_input, chain=chain)
        return JSONResponse(content={"response": output})
