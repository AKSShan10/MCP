import streamlit as st
import asyncio
import os
import nest_asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

nest_asyncio.apply()
# load_dotenv()
load_dotenv("D:\\BJIT\\MCP\\.env")

# --- MCP Server Configuration ---
MCP_SERVERS = {
    "my-custom-tools": {
        "command": "D:\\BJIT\\MCP\\venv\\Scripts\\python.exe",
        "args": ["D:\\BJIT\\MCP\\main.py"],
        "transport": "stdio",
    },
    "weather": {
        "command": "D:\\BJIT\\MCP\\venv\\Scripts\\python.exe",
        "args": ["D:\\BJIT\\MCP\\weather_server.py"],
        "transport": "stdio",
    },
    "manim-server": {
        "command": "D:\\BJIT\\MCP\\venv\\Scripts\\python.exe",
        "args": ["D:\\BJIT\\MCP\\manim-mcp-server\\src\\manim_server.py"],
        "env": {
            "MANIM_EXECUTABLE": "D:\\BJIT\\MCP\\venv\\Scripts\\manim.exe"
        },
        "transport": "stdio",
    },
    "dictionary": {
        "command": "D:\\BJIT\\MCP\\venv\\Scripts\\python.exe",
        "args": ["D:\\BJIT\\MCP\\dictionary_server.py"],
        "transport": "stdio",
    },
}

# --- LLM Setup ---
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0)

# --- Streamlit UI ---
st.set_page_config(page_title="MCP Client", page_icon="🤖")
st.title("🤖 MCP Streamlit Client")
st.caption("Connected to: Custom Tools, Weather, and Manim servers")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# async def run_agent(user_input):
#     client = MultiServerMCPClient(MCP_SERVERS)
#     tools = await client.get_tools()
#     agent = create_react_agent(llm, tools)
#     result = await agent.ainvoke({"messages": [{"role": "user", "content": user_input}]})
#     return result["messages"][-1].content
async def run_agent(user_input):
    client = MultiServerMCPClient(MCP_SERVERS)
    tools = await client.get_tools()
    agent = create_react_agent(llm, tools)
    result = await agent.ainvoke({"messages": [{"role": "user", "content": user_input}]})
    last_message = result["messages"][-1]
    # Handle different response formats
    if isinstance(last_message.content, list):
        return " ".join(block["text"] for block in last_message.content if block.get("text"))
    return last_message.content

if user_input := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = asyncio.run(run_agent(user_input))
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})