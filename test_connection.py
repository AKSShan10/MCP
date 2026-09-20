# # import asyncio
# # from langchain_mcp_adapters.client import MultiServerMCPClient
# #
# # async def test():
# #     # Test ONLY custom-tools first
# #     client = MultiServerMCPClient({
# #         "custom-tools": {
# #             "command": "D:\\BJIT\\MCP\\venv\\Scripts\\python.exe",
# #             "args": ["D:\\BJIT\\MCP\\main.py"],
# #             "transport": "stdio",
# #         },
# #     })
# #     tools = await client.get_tools()
# #     print("Tools found:", [t.name for t in tools])
# #
# # asyncio.run(test())
#
#
#
# # import asyncio
# # from langchain_mcp_adapters.client import MultiServerMCPClient
# #
# # async def test():
# #     client = MultiServerMCPClient({
# #         "manim-server": {
# #             "command": "D:\\BJIT\\MCP\\venv\\Scripts\\python.exe",
# #             "args": ["D:\\BJIT\\MCP\\manim-mcp-server\\src\\manim_server.py"],
# #             "env": {
# #                 "MANIM_EXECUTABLE": "D:\\BJIT\\MCP\\venv\\Scripts\\manim.exe"
# #             },
# #             "transport": "stdio",
# #         },
# #     })
# #     tools = await client.get_tools()
# #     print("Tools found:", [t.name for t in tools])
# #
# # asyncio.run(test())
#
#
# import asyncio
# from langchain_mcp_adapters.client import MultiServerMCPClient
#
# async def test():
#     client = MultiServerMCPClient({
#         "weather": {
#             "command": "D:\\BJIT\\MCP\\venv\\Scripts\\uvx.EXE",
#             "args": ["--from", "git+https://github.com/adhikasp/mcp-weather.git", "mcp-weather"],
#             "env": {
#                 "ACCUWEATHER_API_KEY": "your_accuweather_key_here"
#             },
#             "transport": "stdio",
#         },
#     })
#     tools = await client.get_tools()
#     print("Tools found:", [t.name for t in tools])
#
# asyncio.run(test())

# import asyncio
# from langchain_mcp_adapters.client import MultiServerMCPClient
#
# async def test():
#     client = MultiServerMCPClient({
#         "weather": {
#             "command": "D:\\BJIT\\MCP\\venv\\Scripts\\python.exe",
#             "args": ["D:\\BJIT\\MCP\\weather_server.py"],
#             "transport": "stdio",
#         },
#     })
#     tools = await client.get_tools()
#     for t in tools:
#         print(f"Tool: {t.name}")
#         result = await t.ainvoke({"location": "Dhaka"})
#         print(f"Result: {result}")
#
# asyncio.run(test())

# Update test_connection.py to:
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

async def test():
    client = MultiServerMCPClient({
        "dictionary": {
            "command": "D:\\BJIT\\MCP\\venv\\Scripts\\python.exe",
            "args": ["D:\\BJIT\\MCP\\dictionary_server.py"],
            "transport": "stdio",
        },
    })
    tools = await client.get_tools()
    print("Tools:", [t.name for t in tools])
    for t in tools:
        if t.name == "define_word":
            result = await t.ainvoke({"word": "python"})
            print(f"Define result: {result}")
        if t.name == "translate_text":
            result = await t.ainvoke({"text": "Hello world", "target_language": "bn"})
            print(f"Translate result: {result}")

asyncio.run(test())
