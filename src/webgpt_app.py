import streamlit as st
from utils.app_utils import AppUtils

def main():
    """
    The main function that sets up the Streamlit app, handles user input,
    displays chat messages, and interacts with the AppUtils class to process 
    responses and maintain session state.
    """
    
    # Set the configuration for the Streamlit page
    st.set_page_config(
        page_title="WebGPT App",  # Title of the web app
        page_icon="images/logo.png"  # Icon displayed in the browser tab
    )

    # Set the title of the app displayed on the page
    st.title("WebGPT App")

    # Initialize the session state for messages if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display all previous messages from the session state (chat history)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Capture the user's input
    user_prompt = st.chat_input()
    
    # If there is a user prompt, process it
    if user_prompt:
        # Display the user's message in the chat
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Append the user's message to the session state
        st.session_state.messages.append(
            {"role": "user", "content": user_prompt}
        )

        # Generate a response from the assistant using AppUtils
        with st.chat_message("assistant"):
            response = AppUtils.get_response(st.session_state.messages)
            st.markdown(response)

        # Append the assistant's response to the session state
        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )

# Run the app by calling the main function when this file is executed
if __name__ == "__main__":
    main()
