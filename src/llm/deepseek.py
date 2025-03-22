"""
DeepSeek LLM integration using Ollama.
"""
import os
import yaml
import requests
import json
from typing import Optional, Dict, Any, Generator, Callable, Union


class DeepSeekLLM:
    def __init__(self, config_path: str = "config/llm_config.yaml"):
        """
        Initialize the DeepSeek LLM integration.
        
        Args:
            config_path (str): Path to the configuration file
        """
        self.config = self._load_config(config_path)
        self.model = self.config["model"]["name"]
        self.api_url = self.config["model"]["api_url"]
        self.system_prompt = self.config.get("system_prompt")
        self._ensure_model_available()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")
            return {
                "model": {
                    "name": "deepseek-r1:8b",
                    "api_url": "http://localhost:11434"
                },
                "generation": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 500,
                    "repeat_penalty": 1.1,
                    "stop": ["\n\n", "Human:", "Assistant:"],
                    "num_predict": 100
                },
                "formatting": {
                    "remove_artifacts": True,
                    "ensure_sentence_endings": True,
                    "clean_whitespace": True,
                    "max_line_length": 80,
                    "add_punctuation": True
                }
            }

    def _ensure_model_available(self) -> None:
        """Ensure the model is available locally."""
        try:
            # Check if model exists
            response = requests.get(f"{self.api_url}/api/tags")
            response.raise_for_status()
            models = [model["name"] for model in response.json()["models"]]
            
            if self.model not in models:
                print(f"Pulling model {self.model}...")
                response = requests.post(
                    f"{self.api_url}/api/pull",
                    json={"name": self.model}
                )
                response.raise_for_status()
                print("Model pulled successfully!")
        except requests.exceptions.ConnectionError:
            raise Exception(
                "Could not connect to Ollama. Make sure it's running with: "
                "docker-compose up -d"
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to check/pull model: {str(e)}")

    def _clean_response(self, response: str) -> str:
        """Clean and format the response text."""
        formatting_config = self.config.get("formatting", {})
        
        # Remove artifacts if configured
        if formatting_config.get("remove_artifacts", True):
            response = response.replace("speak now", "")
            response = response.replace("Human:", "").replace("Assistant:", "")
            # Remove <think> sections
            if "<think>" in response:
                response = response.split("</think>")[-1].strip()
        
        # Clean whitespace if configured
        if formatting_config.get("clean_whitespace", True):
            response = response.strip()
            # Replace multiple spaces with single space
            response = " ".join(response.split())
        
        # Ensure sentence endings if configured
        if formatting_config.get("ensure_sentence_endings", True):
            if not response.endswith((".", "!", "?")):
                response += "."
        
        # Format line length if configured
        if formatting_config.get("max_line_length"):
            max_length = formatting_config["max_line_length"]
            lines = response.split("\n")
            formatted_lines = []
            for line in lines:
                if len(line) > max_length:
                    # Split long lines at word boundaries
                    words = line.split()
                    current_line = []
                    current_length = 0
                    for word in words:
                        if current_length + len(word) + 1 <= max_length:
                            current_line.append(word)
                            current_length += len(word) + 1
                        else:
                            formatted_lines.append(" ".join(current_line))
                            current_line = [word]
                            current_length = len(word)
                    if current_line:
                        formatted_lines.append(" ".join(current_line))
                else:
                    formatted_lines.append(line)
            response = "\n".join(formatted_lines)
        
        return response

    def _stream_response(
        self,
        response: requests.Response,
        callback: Optional[Callable[[str], None]] = None
    ) -> Generator[str, None, None]:
        """Stream the response from the model."""
        buffer = ""
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line)
                    if "response" in chunk:
                        buffer += chunk["response"]
                        if callback:
                            callback(chunk["response"])
                        yield chunk["response"]
                except json.JSONDecodeError:
                    continue
        
        # Clean and format the complete response
        if buffer:
            yield self._clean_response(buffer)

    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        stream: bool = False,
        callback: Optional[Callable[[str], None]] = None
    ) -> Union[str, Generator[str, None, None]]:
        """
        Generate a response from the model.
        
        Args:
            prompt (str): The user's prompt
            system_prompt (Optional[str]): Optional system prompt to guide the model
            stream (bool): Whether to stream the response
            callback (Optional[Callable[[str], None]]): Optional callback for streaming updates
            
        Returns:
            Union[str, Generator[str, None, None]]: The model's response or a generator for streaming
        """
        try:
            # Use provided system prompt or default from config
            system_prompt = system_prompt or self.system_prompt
            
            # Prepare generation parameters
            params = {
                "model": self.model,
                "prompt": prompt,
                "system": system_prompt,
                "stream": stream
            }
            
            # Add any additional generation parameters from config
            if "generation" in self.config:
                params.update(self.config["generation"])
            
            response = requests.post(
                f"{self.api_url}/api/generate",
                json=params,
                stream=stream
            )
            response.raise_for_status()
            
            if stream:
                return self._stream_response(response, callback)
            else:
                return self._clean_response(response.json()["response"])
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to generate response: {str(e)}")


if __name__ == "__main__":
    # Test the integration
    llm = DeepSeekLLM()
    
    # Test non-streaming response
    print("Testing non-streaming response:")
    response = llm.generate_response("Hello! How are you today?")
    print(f"Response: {response}")
    
    # Test streaming response
    print("\nTesting streaming response:")
    def print_chunk(chunk: str):
        print(chunk, end="", flush=True)
    
    for chunk in llm.generate_response(
        "Tell me a short story about a robot learning to paint.",
        stream=True,
        callback=print_chunk
    ):
        pass 