from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
from prompts import get_system_prompt  # Assuming this function remains the same
import re

st.title("☃️ Frosty")

# Initialize the chat messages history
if "messages" not in st.session_state:
  # System prompt included in separate function
  st.session_state.messages = [{"role": "system", "content": get_system_prompt()}]

# Initialize LLaMA
llm = Ollama(model="llama2")

# Prompt for user input and save
if prompt := st.chat_input():
  st.session_state.messages.append({"role": "user", "content": prompt})

# Display the existing chat messages
for message in st.session_state.messages:
  if message["role"] == "system":
    continue
  with st.chat_message(message["role"]):
    st.write(message["content"])
    if "results" in message:
      st.dataframe(message["results"])

def create_prompt(messages):
  prompt_text = ""
  for message in messages:
    role = message["role"]
    content = message["content"]
    prompt_text += f"{role}: {content}\n"
  return prompt_text

# If last message is not from assistant, generate a new response using LLaMA
if st.session_state.messages[-1]["role"] != "assistant":
  with st.chat_message("assistant"):
    response = ""
    resp_container = st.empty()
    # Create prompt from chat history
    prompt = create_prompt(st.session_state.messages)
    for chunk in llm(prompt=prompt).split("\n\n"):  # Process response in chunks
      response += chunk + "\n\n"
      resp_container.markdown(response)

    message = {"role": "assistant", "content": response}
    # Parse the response for a SQL query and execute if available
    sql_match = re.search(r"`sql\n(.*)\n`", response, re.DOTALL)
    if sql_match:
      sql = sql_match.group(1)
      conn = st.connection("snowflake")
      message["results"] = conn.query(sql)
      st.dataframe(message["results"])
    st.session_state.messages.append(message)
