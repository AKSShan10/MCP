from mcp.server.fastmcp import FastMCP
import urllib.request
import json

mcp = FastMCP(name="Dictionary & Translate Server")

@mcp.tool()
def define_word(word: str) -> str:
    """Look up the definition of an English word. Example: define_word("python")"""
    try:
        url = f"https://api.datamuse.com/words?sp={word}&md=d&max=1"
        req = urllib.request.Request(url, headers={"User-Agent": "MCP-Dictionary/1.0"})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())

        if not data or "defs" not in data[0]:
            return f"No definition found for '{word}'."

        result = f"Word: {data[0]['word']}\n"
        for defn in data[0]["defs"]:
            parts = defn.split("\t", 1)
            if len(parts) == 2:
                result += f"\n({parts[0]}) {parts[1]}"
            else:
                result += f"\n{defn}"
        return result.strip()
    except Exception as e:
        return f"Error looking up '{word}': {str(e)}"


@mcp.tool()
def translate_text(text: str, target_language: str) -> str:
    """Translate text to another language.
    target_language should be a language code like: es (Spanish), fr (French),
    de (German), ja (Japanese), bn (Bengali), hi (Hindi), ar (Arabic),
    zh (Chinese), ko (Korean), pt (Portuguese).
    Example: translate_text("Hello world", "es")"""
    try:
        encoded_text = urllib.parse.quote(text)
        url = f"https://api.mymemory.translated.net/get?q={encoded_text}&langpair=en|{target_language}"
        with urllib.request.urlopen(url) as resp:
            data = json.loads(resp.read().decode())

        translated = data["responseData"]["translatedText"]
        return f"Original: {text}\nTranslated ({target_language}): {translated}"
    except Exception as e:
        return f"Error translating: {str(e)}"


if __name__ == "__main__":
    mcp.run()