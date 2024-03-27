########### code utilisant Ollama

import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

# Initialize model and prompt
llm = Ollama(model="llama2")
prompt = ChatPromptTemplate.from_messages([
    ("system", "What is Streamlit?"),
    ("user", "")  # Leave space for LLaMA's response
])

# Create chain
chain = prompt | llm

# Invoke chain and print response
response = chain.invoke({"input": "What is Streamlit?"})
st.write(response)


conn = st.connection("snowflake")
df = conn.query("select current_warehouse()")
st.write(df)