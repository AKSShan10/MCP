from mcp.server.fastmcp import FastMCP
import urllib.request
import json

mcp = FastMCP(name="Weather Server")

API_KEY = "Enter your key here"  # Replace with your actual AccuWeather API key

@mcp.tool()
def get_weather(location: str) -> str:
    """Get the current weather for a city. Example: get_weather("Dhaka")"""
    try:
        # Step 1: Search for city
        search_url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={API_KEY}&q={location}"
        with urllib.request.urlopen(search_url) as resp:
            cities = json.loads(resp.read().decode())

        if not cities:
            return f"City '{location}' not found."

        city_key = cities[0]["Key"]
        city_name = cities[0]["LocalizedName"]
        country = cities[0]["Country"]["LocalizedName"]

        # Step 2: Get current conditions
        weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{city_key}?apikey={API_KEY}"
        with urllib.request.urlopen(weather_url) as resp:
            conditions = json.loads(resp.read().decode())

        if not conditions:
            return f"No weather data available for {city_name}."

        weather = conditions[0]
        temp_c = weather["Temperature"]["Metric"]["Value"]
        temp_f = weather["Temperature"]["Imperial"]["Value"]
        text = weather["WeatherText"]

        return (
            f"Weather for {city_name}, {country}:\n"
            f"Condition: {text}\n"
            f"Temperature: {temp_c}°C ({temp_f}°F)"
        )
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

if __name__ == "__main__":
    mcp.run()