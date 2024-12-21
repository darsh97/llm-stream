import time
from typing import Optional, Any, Iterator
import google.generativeai as genai
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain_core.outputs import GenerationChunk
from typing import Mapping

from logger import Logger
from utils import timer_decorator

logger = Logger()


class GeminiWrapper(LLM):
    api_key: str
    model_name: str

    @property
    def _llm_type(self) -> str:
        return self.model_name

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"api_key": self.api_key, "model_name": self.model_name}

    @timer_decorator
    def _call(
            self,
            prompt: str,
            stop: Optional[list[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> str:
        logger.info(f"Inside GeminiWrapper _call()")
        logger.info(f"Using Model: {self.model_name}")
        try:
            response = genai.GenerativeModel(self.model_name).generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Caught exception: {e}")
            raise e

    def _stream(
            self,
            prompt: str,
            stop: Optional[list[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> Iterator[GenerationChunk]:


        logger.info(f"Inside GeminiWrapper _stream()")
        logger.info(f"Using Model: {self.model_name}")
        stream_response = genai.GenerativeModel(self.model_name).generate_content(prompt, stream=True)
        logger.info(f"Stream Response Created")

        start = time.time()

        for chunk in stream_response:
            logger.info(f"Yielding Chunk from _stream()")

            # wrapping the model output (chunk) explicitly in a GenerationChunk object
            # the function guarantees that only valid and structured data (with attributes like text) is yielded.
            yield GenerationChunk(
                text=chunk.text
            )

        logger.info(f"All Stream Response Yielded")
        logger.info(f"Time Taken to stream: {time.time() - start}")
