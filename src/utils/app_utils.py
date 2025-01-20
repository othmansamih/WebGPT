from inspect import signature
from typing import Any
from utils.web_search import WebSearch
from utils.load_config import LoadConfig
from langsmith import traceable
import json
import copy

# Initialize the application configuration
APP_CONFIG = LoadConfig()

class AppUtils:
    """
    A utility class to handle various operations related to function transformation,
    LLM interaction, and function calling.

    Methods:
        function_to_tool(func: Any) -> dict: Transforms a Python function into the format
                                            required for the OpenAI API's `tools` argument.
        functions_to_tools() -> list: Transforms predefined functions into tools for LLM.
        call_function(name, args): Calls the corresponding function based on the function name.
        ask_llm_function_caller(messages): Sends a request to the LLM function caller to process the messages.
        ask_llm(messages): Sends a request to the LLM for a standard completion.
        get_response(messages): Handles the entire process of calling functions and querying the LLM.
    """
    
    @staticmethod
    def function_to_tool(func: Any) -> dict:
        """
        Transforms a Python function into the format required for the OpenAI API's `tools` argument.

        Args:
            func (Any): The function to transform.

        Returns:
            dict: A dictionary representing the function in the `tools` format.
        """
        # Get function metadata (name and description)
        func_name = func.__name__
        func_doc = func.__doc__.strip() if func.__doc__ else "No description provided."
        
        # Extract function parameters and build the parameters schema
        sig = signature(func)
        parameters = {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }

        for param_name, param in sig.parameters.items():
            # Determine parameter type from the function signature
            param_type = str(param.annotation).lower() if param.annotation != param.empty else "string"
    
            # Map type hints to JSON schema types
            if "str" in param_type:
                param_type = "string"
            elif "int" in param_type or "float" in param_type:
                param_type = "number"
            elif "bool" in param_type:
                param_type = "boolean"
            elif "list" in param_type:
                param_type = "array"
            elif "dict" in param_type:
                param_type = "object"

            parameters["properties"][param_name] = {"type": param_type}
            parameters["required"].append(param_name)

        # Build the tool structure for the function
        return {
            "type": "function",
            "function": {
                "name": func_name,
                "description": func_doc,
                "parameters": parameters,
                "strict": True
            }
        }
    
    @staticmethod
    def functions_to_tools():
        """
        Transforms predefined functions into the tools format required for the OpenAI API.

        Returns:
            list: A list of tools representing functions for LLM usage.
        """
        return [
            AppUtils.function_to_tool(WebSearch.web_search_text),
            AppUtils.function_to_tool(WebSearch.web_search_images),
            AppUtils.function_to_tool(WebSearch.web_search_videos),
            AppUtils.function_to_tool(WebSearch.web_search_news)
        ]
    
    @staticmethod
    def call_function(name, args):
        """
        Calls the appropriate function based on the name and arguments passed.

        Args:
            name (str): The name of the function to call.
            args (dict): The arguments to pass to the function.

        Returns:
            Any: The result of the function call.
        """
        if name == "web_search_text":
            return WebSearch.web_search_text(**args)
        elif name == "web_search_images":
            return WebSearch.web_search_images(**args)
        elif name == "web_search_videos":
            return WebSearch.web_search_videos(**args)
        elif name == "web_search_news":
            return WebSearch.web_search_news(**args)
        else:
            raise ValueError(f"Function {name} not found.")

    
    @traceable
    @staticmethod
    def ask_llm_function_caller(messages):
        """
        Sends a request to the LLM function caller, using the specified messages.

        Args:
            messages (list): A list of messages to send to the LLM.

        Returns:
            completion: The response from the LLM with the tool calls.
        """
        client = APP_CONFIG.client
        completion = client.chat.completions.create(
            model=APP_CONFIG.model_name,
            messages=[{"role": "system", "content": APP_CONFIG.function_caller_llm_system_prompt}] + messages,
            tools=AppUtils.functions_to_tools(),
            temperature=APP_CONFIG.temperature
        )
        return completion
    
    @traceable
    @staticmethod
    def ask_llm(messages):
        """
        Sends a request to the LLM for a standard completion, without function calling.

        Args:
            messages (list): A list of messages to send to the LLM.

        Returns:
            completion: The LLM response based on the provided messages.
        """
        client = APP_CONFIG.client
        completion = client.chat.completions.create(
            model=APP_CONFIG.model_name,
            messages=[{"role": "system", "content": APP_CONFIG.llm_system_prompt}] + messages,
            temperature=APP_CONFIG.temperature
        )
        return completion
    
    @staticmethod
    def get_response(messages):
        """
        Handles the entire process of calling functions, querying the LLM, and returning the final result.

        Args:
            messages (list): A list of messages to send to the LLM.

        Returns:
            str: The content of the final LLM response after processing any tool calls.
        """
        msgs = copy.deepcopy(messages)
        completion = AppUtils.ask_llm_function_caller(messages)
        tool_calls = completion.choices[0].message.tool_calls
        if tool_calls is not None:
            # Process tool calls and fetch corresponding results
            for tool_call in tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                search_results = AppUtils.call_function(name, args)
                msgs.append(completion.choices[0].message)
                msgs.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(search_results, indent=4)
                })
            completion = AppUtils.ask_llm(msgs)
            
        return completion.choices[0].message.content
