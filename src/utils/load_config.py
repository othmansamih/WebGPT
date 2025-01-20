import yaml
from openai import OpenAI
from langsmith.wrappers import wrap_openai
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

class LoadConfig:
    """
    A class to load application configurations from a YAML file 
    and initialize an OpenAI client with the loaded configurations.

    Attributes:
        function_caller_llm_system_prompt (str): System prompt used for function-calling LLMs.
        llm_system_prompt (str): General system prompt for the LLM.
        temperature (float): Temperature setting for controlling randomness in LLM outputs.
        model_name (str): Name of the LLM model to use.
        client (OpenAI): A wrapped OpenAI client for managing LLM calls with tracing enabled.
    """
    
    def __init__(self) -> None:
        """
        Initialize the LoadConfig class by reading configuration from a YAML file 
        and setting up the OpenAI client.
        """
        # Load configuration data from the specified YAML file
        with open('configs/app_configs.yml', 'r') as file:
            data = yaml.safe_load(file)
        
        # Assign configuration values to class attributes
        self.function_caller_llm_system_prompt = data["function_caller_llm_system_prompt"]
        self.llm_system_prompt = data["llm_system_prompt"]
        self.temperature = data["temperature"]
        self.model_name = data["model_name"]
        
        # Initialize an OpenAI client with the API key from environment variables
        # Wrap the client to enable tracing of LLM calls in context
        self.client = wrap_openai(OpenAI(
            api_key=os.environ["OPENAI_API_KEY"]
        ))
