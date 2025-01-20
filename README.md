# WebGPT App

WebGPT App is an interactive web search assistant that leverages OpenAI's GPT models and DuckDuckGo Search API to provide concise and accurate responses to user queries. The application integrates advanced tools to search for text, images, videos, and news articles directly from the web, providing a user-friendly chat interface powered by Streamlit.

## Features

- **Chat-based Interface:** Communicate with the assistant via a simple chat interface.
- **Web Search Integration:** Perform web searches for text, images, videos, and news using DuckDuckGo API.
- **LLM Function Calling:** Dynamically select and execute functions based on user needs.
- **Configurable Behavior:** Customize the assistant’s behavior through YAML configurations.
- **Streamlit Integration:** Easy-to-use web interface for seamless interaction.

## Project Structu

```markdown
WEB-GPT-Project/
├── .env
├── configs/
│   └── app_configs.yml
├── images/
│   └── logo.png
├── requirements.txt
├── src/
│   ├── utils/
│   │   ├── app_utils.py
│   │   ├── load_config.py
│   │   └── web_search.py
│   └── webgpt_app.py
```

### Key Files

- `.env`: Contains sensitive API keys and environment configurations.
- `configs/app_configs.yml`: Stores configuration settings for the app, such as LLM prompts and model parameters.
- `src/utils/`: Contains utility scripts for loading configurations, performing web searches, and managing app logic.
- `src/webgpt_app.py`: Main Streamlit application script.
- `images/logo.png`: Application logo used in the Streamlit UI.
- `requirements.txt`: Lists required Python dependencies.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- An OpenAI API key
- Langsmith API key for tracing (optional)

### Installation

1. Clone this repository:
    
    ```bash
    git clone https://github.com/othmansamih/WEBGPT.git
    cd webgpt-app
    ```
    
2. Create a virtual environment:
    
    ```bash
    python -m venv venv
    .venv/Scripts/activate  # If you're on Windows
    ```
    
3. Install dependencies:
    
    ```bash
    pip install -r requirements.txt
    ```
    
4. Set up your `.env` file with the required API keys:
    
    ```
    OPENAI_API_KEY="your_openai_api_key"
    LANGSMITH_TRACING=true
    LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
    LANGSMITH_API_KEY="your_langsmith_api_key"
    LANGSMITH_PROJECT="WEB-GPT-Project"
    ```
    

### Usage

1. Run the Streamlit app:
    
    ```bash
    streamlit run src/webgpt_app.py
    ```
    
2. Access the app in your browser at `http://localhost:8501`.
3. Start interacting with the assistant by typing your queries into the chat interface.

## Configuration

The app’s behavior can be customized using `configs/app_configs.yml`. Key parameters include:

- `function_caller_llm_system_prompt`: Instructions for the assistant when determining which web search function to use.
- `llm_system_prompt`: Defines the assistant's general behavior for responses.
- `temperature`: Controls the randomness of responses.
- `model_name`: Specifies the GPT model to use.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for bug fixes or feature enhancements.

## Acknowledgements

- [OpenAI](https://openai.com/)
- [DuckDuckGo Search API](https://pypi.org/project/duckduckgo-search/)
- [Streamlit](https://streamlit.io/)
- [Langsmith](https://smith.langchain.com/)