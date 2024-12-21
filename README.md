# llm-stream

## Overview

The API is boiler plate reference to handle streaming responses and using CustomLLM class that langchain provides

How to Run the Server
  To run the FastAPI server, follow these steps:

  Install dependencies: Ensure you have Python and pip installed. Then, install the required dependencies by running:

  pip install -r requirements.txt
  Run the server: Start the FastAPI server using the following command:

  uvicorn main:app --reload
  By default, the server will run on http://localhost:8000.
  
  API Endpoints
  Generate Poem
  Endpoint: /api/generate/{poem_topic}
  Method: GET
  Description: Generates a poem based on the specified theme.
  Example
  To generate a "happiness" themed poem with streaming enabled, you can use the following URL:

http://localhost:8000/api/generate/happiness?stream=true


To consume the streaming API, you can use the following code:

```python
import requests

def stream_response(url):
    """
    Stream data from the given URL and print chunks as they arrive.
    """
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            print("Streaming response started...\n")
            # Iterate over the streamed chunks
            for chunk in response.iter_lines():
                if chunk:  # Avoid empty chunks or keep-alive newlines
                    print(f"Received chunk: {chunk.decode('utf-8')}")
                else:
                    print("(empty chunk received)")
    except requests.exceptions.RequestException as err:
        print(f"Error while streaming: {err}")

# Stream from your FastAPI endpoint
if __name__ == "__main__":
    STREAM_URL = "http:localhost:8080/api/generate/happiness?stream=true"
    stream_response(STREAM_URL)