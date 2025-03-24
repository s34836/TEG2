import streamlit as st
import requests
from config_manager import ConfigManager

# Load configuration
config_manager = ConfigManager("config.yml")
config = config_manager.get_config()

class ChatbotApp:
    """Main Streamlit Chatbot Application"""

    def __init__(self):
        """Initialize the chatbot application"""
        st.set_page_config(
            page_title=config.get('app', {}).get('title', "AI Chatbot"),
            layout=config.get('app', {}).get('layout', "wide")
        )

        self.api_url = config.get("api_url", "http://127.0.0.1:5000/api/chat")
        self.default_model = config.get("default_model", "gpt-4o-mini")
        self.available_models = config.get("available_models", ["gpt-4o-mini", "gpt-3.5-turbo"])
        self.default_system_message = config.get("default_system_message", "You are a helpful assistant.")
        self.chat_placeholder = config.get("chat_placeholder", "Hi, how can I help you?")
        self.temperature = config.get("temperature", 0.7)

        self._initialize_session_state()
        self._render_ui()

    def _initialize_session_state(self):
        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = self.default_model
        if "temperature" not in st.session_state:
            st.session_state["temperature"] = self.temperature
        if "system_message" not in st.session_state:
            st.session_state["system_message"] = self.default_system_message
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "system", "content": self.default_system_message}
            ]

    def _render_ui(self):
        st.title(config.get("app_title", "My New Chtbot App"))

        with st.sidebar:
            st.selectbox("Model", options=self.available_models, key="openai_model")
            st.slider("Temperature", 0.0, 1.0, key="temperature")
            st.text_area("System message", key="system_message")

        user_prompt = st.chat_input(self.chat_placeholder)

        if user_prompt:
            with st.spinner("Waiting for response..."):
                payload = {
                    "human_message": user_prompt,
                    "system_message": st.session_state.system_message,
                    "model": st.session_state.openai_model,
                    "temperature": st.session_state.temperature,
                }
                try:
                    res = requests.post(self.api_url, json=payload, timeout=10)
                    if res.status_code == 200:
                        res_json = res.json()
                        reply = res_json.get("response", "[No response]")
                    else:
                        reply = f"Error: Backend returned status code {res.status_code}"
                except requests.exceptions.RequestException:
                    reply = "Error: Lost connection to backend"
                except Exception as e:
                    reply = f"Unexpected error: {str(e)}"

                st.session_state.messages.append({"role": "user", "content": user_prompt})
                st.session_state.messages.append({"role": "assistant", "content": reply})

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

if __name__ == "__main__":
    ChatbotApp()