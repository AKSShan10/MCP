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

import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

async def test():
    client = MultiServerMCPClient({
        "weather": {
            "command": "D:\\BJIT\\MCP\\venv\\Scripts\\python.exe",
            "args": ["D:\\BJIT\\MCP\\weather_server.py"],
            "transport": "stdio",
        },
    })
    tools = await client.get_tools()
    for t in tools:
        print(f"Tool: {t.name}")
        result = await t.ainvoke({"location": "Dhaka"})
        print(f"Result: {result}")

asyncio.run(test())