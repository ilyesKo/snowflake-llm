from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

st.title("☃️ Data-Major Bot")

# Initialize the chat messages history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How can I help?"}]

# Initialize LLaMA
llm = Ollama(model="llama2")

# Prompt for user input and save
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display the existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def create_prompt(messages):
  prompt_text = ""
  for message in messages:
    role = message["role"]
    content = message["content"]
    prompt_text += f"{role}: {content}\n"
  return prompt_text

# If last message is not from assistant, generate a new response using LLaMA
if st.session_state.messages[-1]["role"] != "assistant":
    # Call LLaMA
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            prompt = create_prompt(st.session_state.messages)
            print("prompt =" + prompt)
            response = llm(prompt=prompt)
            print("reponse =" +response)
            st.write( response)

    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
