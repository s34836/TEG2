print("Start")
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

print("Start")
# Load environment variables
dotenv_path = os.path.join('../', 'config', '.env')
load_dotenv(dotenv_path)
api_key = os.getenv('OPENAI_API_KEY_TEG')

print("Start")
def get_openai_response(prompt: str, system_context:str = None):

    try:
        chat = ChatOpenAI(
            api_key = api_key,
            model="gpt-4o-mini",        # Model to be chosen, example gpt-4o or gpt-3.5-turbo
            temperature=0.9,            # 0-1: the higher the more creative model
            # max_tokens=150,           # 1-n: Limit response length
            # top_p=1.0,                # 0-1: Alternative randomness control (nucleus sampling)
            # frequency_penalty=0.0,    # 0-1: Reduce repetitive text, the lower the least repetitive it is
            # presence_penalty=0.0,     # 0-1: Encourage new topics, the lower the more new topics
        )
        
        messages = []
        
        # Add system message if provided
        if system_context:
            messages.append(SystemMessage(content=system_context))
        
        # Add human message
        messages.append(HumanMessage(content=prompt))
        
        # Get response
        response = chat.invoke(messages)
        
        return response.content
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None




system_context = "You are a helpful assistant who explains things in a way that a 5-year-old would understand."
prompt = "What are the multi-agents structures in AI?"
print("Start")
response = get_openai_response(prompt, system_context)

if response:
    print("Prompt:", prompt)
    print("System Context:", system_context)
    print("\n\nResponse:", response)