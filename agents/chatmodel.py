import ollama
import os
from abc import ABC, abstractmethod
from huggingface_hub import InferenceClient, HfApi
# Gemini API imports
from google.genai import Client as GenerativeLanguageServiceClient, types

class StreamingChatModel(ABC):
    """Abstract base class for streaming chat models."""
    def chat(self, model, messages, stream=True):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def list_models(self):
        """List available models for the chat model."""
        raise NotImplementedError("This method should be implemented by subclasses.")


class OllamaStreamingChatModel(StreamingChatModel):
    """HuggingFace implementation of the StreamingChatModel."""
    def __init__(self, model=None):
        self.model = model

    """Ollama implementation of the StreamingChatModel."""
    def chat(self, model=None, messages=None, stream=True):
        if model is None:
            model = self.model or "gemma3:4b"

        if not messages or not isinstance(messages, list):
            raise ValueError("Messages must be a non-empty list.")

        # Ensure messages are in the correct format for Ollama
        for msg in messages:
            if not isinstance(msg, dict) or 'role' not in msg or 'content' not in msg:
                raise ValueError("Each message must be a dict with 'role' and 'content' keys.")

        # Call the Ollama chat API with streaming enabled
        return ollama.chat(model=model, messages=messages, stream=stream)

    def list_models(self):
        # List available models from the Ollama API
        models = ollama.list_models()
        if not models:
            raise ValueError("No models found. Ensure Ollama is running and models are available.")
        return [m.name for m in models]


class HFStreamingChatModel(StreamingChatModel):
    """HuggingFace implementation of the StreamingChatModel."""
    def __init__(self, model=None, api_key=None, provider="auto"):
        self.model = model
        self.api_key = api_key or os.environ.get("HF_TOKEN")
        self.provider = provider
        self.client = InferenceClient(provider=self.provider, api_key=self.api_key)
        #print(self.list_models())

    def chat(self, model=None, messages=None, stream=True):
        if model is None:
            model = self.model or "Qwen/Qwen3-8B"

        if not messages or not isinstance(messages, list):
            raise ValueError("Messages must be a non-empty list.")

        # Ensure messages are in the correct format for Ollama
        for msg in messages:
            if not isinstance(msg, dict) or 'role' not in msg or 'content' not in msg:
                raise ValueError("Each message must be a dict with 'role' and 'content' keys.")

        # Convert messages to the expected format if needed
        # Simulate streaming by yielding fake Ollama-like chunks with 'message': {'content': ...}
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,  # Enable streaming
        )
        # HuggingFace streaming returns an iterator of chunks
        for chunk in response:
            # Each chunk should have a 'delta' or 'content' field depending on the API
            content = ""
            if hasattr(chunk.choices[0].delta, "content"):
                content = chunk.choices[0].delta.content
            elif "content" in chunk.choices[0].delta:
                content = chunk.choices[0].delta["content"]
            if content:
                yield {"message": {"content": content}}

    def list_models(self):
        # List available models from the HuggingFace Hub using HfApi (recommended)
        api = HfApi(token=self.api_key)
        models = api.list_models(inference="warm", pipeline_tag="text-generation")
        return [m.id for m in models]


class GeminiStreamingChatModel(StreamingChatModel):
    """Gemini API implementation of the StreamingChatModel."""
    def __init__(self, model=None, api_key=None):
        self.model = model or "gemini-pro"
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:streamGenerateContent"
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable must be set or api_key provided.")

    def chat(self, model=None, messages=None, stream=True):
        if model is None:
            model = self.model

        if not messages or not isinstance(messages, list):
            raise ValueError("Messages must be a non-empty list.")

        # Ensure messages are in the correct format for Gemini
        for msg in messages:
            if not isinstance(msg, dict) or 'role' not in msg or 'content' not in msg:
                raise ValueError("Each message must be a dict with 'role' and 'content' keys.")

        # Prepare the request payload
        x2 = [msg["content"] for msg in messages]

        # Create a client and stream the response
        client = GenerativeLanguageServiceClient()
        response = client.models.generate_content_stream(model=model, contents=x2)

        # Yield each chunk of the response
        for chunk in response:
            if (chunk.candidates and chunk.candidates[0].content and
                    chunk.candidates[0].content.parts):
                #print(chunk.candidates[0].content.parts[0].text)
                yield {"message": {"content": chunk.candidates[0].content.parts[0].text}}

    def list_models(self):
        # Gemini API does not provide a public model listing endpoint; return common models
        return ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash"]


class ChatModelFactory:
    """Factory class to initialize the appropriate chat model."""
    def __init__(self, chat_model=None, model=None):
        self.chat_model = chat_model
        self.model = model

    def get(self, model=None):
        """Returns the initialized chat model based on the provided model name."""
        if self.chat_model is None:
            if model is None:
                model = self.model or "ollama:gemma3:1b"

            """Initializes the appropriate streaming chat model."""
            if model.startswith("ollama"):
                self.model = model.split(':', 1)[1]
                self.chat_model = OllamaStreamingChatModel(self.model)
            elif model.startswith("hf") or model.startswith("huggingface"):
                self.model = model.split(':', 1)[1]
                self.chat_model = HFStreamingChatModel(self.model)
            elif model.startswith("gemini"):
                self.model = model.split(':', 1)[1] if ':' in model else "gemini-pro"
                self.chat_model = GeminiStreamingChatModel(self.model)
            else:
                raise ValueError(f"Unknown model provider for model: '{model}'")

        return self.chat_model
