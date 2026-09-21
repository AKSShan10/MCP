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
        "transport": "stdio",
    },
    "dictionary": {
        "command": "D:\\BJIT\\MCP\\venv\\Scripts\\python.exe",
        "args": ["D:\\BJIT\\MCP\\dictionary_server.py"],
        "transport": "stdio",
    },
    "deployed-tools": {
        "url": "https://my-custom-tools.fastmcp.app/mcp",
        "transport": "streamable_http",
        "headers": {
            "Authorization": "Bearer " + os.environ.get("FASTMCP_API_TOKEN", ""),
        },
    },
}

# --- LLM Setup ---
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0)

# --- Streamlit UI ---
st.set_page_config(page_title="MCP Client", page_icon="🤖")
st.title("🤖 MCP Streamlit Client")
# st.caption("Connected to: Custom Tools, Weather, and Manim servers")
st.caption("Connected to: Custom Tools, Weather, Manim, Dictionary, and Deployed Server")

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


# async def run_agent(user_input):
#     client = MultiServerMCPClient(MCP_SERVERS)
#     tools = await client.get_tools()
#     agent = create_react_agent(llm, tools)
#     result = await agent.ainvoke({"messages": [{"role": "user", "content": user_input}]})
#     last_message = result["messages"][-1]
#     # Handle different response formats
#     if isinstance(last_message.content, list):
#         return " ".join(block["text"] for block in last_message.content if block.get("text"))
#     return last_message.content


#
# async def run_agent(user_input):
#     client = MultiServerMCPClient(MCP_SERVERS)
#     tools = await client.get_tools()
#     agent = create_react_agent(llm, tools)
#     try:
#         result = await asyncio.wait_for(
#             agent.ainvoke({"messages": [{"role": "user", "content": user_input}]}),
#             timeout=300
#         )
#         last_message = result["messages"][-1]
#         if isinstance(last_message.content, list):
#             return " ".join(block["text"] for block in last_message.content if block.get("text"))
#         return last_message.content
#     except asyncio.TimeoutError:
#         return "Request timed out. Manim videos take too long for the chat interface — try simpler queries or use Claude Desktop for Manim."

async def run_agent(user_input):
    client = MultiServerMCPClient(MCP_SERVERS)
    tools = await client.get_tools()
    agent = create_react_agent(llm, tools)
    try:
        result = await asyncio.wait_for(
            agent.ainvoke({"messages": [{"role": "user", "content": user_input}]}),
            timeout=300
        )
        last_message = result["messages"][-1]
        if isinstance(last_message.content, list):
            return " ".join(block["text"] for block in last_message.content if block.get("text"))
        return last_message.content
    except asyncio.TimeoutError:
        return "Request timed out."
    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            return "Gemini free tier limit reached (20 requests/day). Wait and try again later."
        if "call_tool_result" in str(e):
            return "A tool crashed during execution. The manim server may have encountered an error. Try a simpler request or check the manim server logs."
        return f"Error: {str(e)}"


if user_input := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = asyncio.run(run_agent(user_input))
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})