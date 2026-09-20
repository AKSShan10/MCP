from fastmcp import FastMCP
from datetime import date
import random

mcp = FastMCP(name="My Custom Tools Server")

@mcp.resource("resource://server-info")
def get_server_info() -> str:
    """Returns information about this MCP server and its available tools."""
    return (
        "This is My Custom Tools Server deployed on Prefect Horizon. "
        "Available tools: calculate_age (calculates age from date of birth), "
        "random_number (generates a random integer in a given range)."
    )

@mcp.tool
def calculate_age(date_of_birth: str) -> str:
    """Calculate a person's current age from their date of birth.
    The date_of_birth must be in YYYY-MM-DD format, for example: 2000-01-15"""
    birth = date.fromisoformat(date_of_birth)
    today = date.today()
    years = today.year - birth.year
    months = today.month - birth.month
    days = today.day - birth.day
    if days < 0:
        months -= 1
        days += 30
    if months < 0:
        years -= 1
        months += 12
    return f"Age: {years} years, {months} months, {days} days [Powered by My Custom Tools Server]"

@mcp.tool
def random_number(min_value: int = 0, max_value: int = 100) -> int:
    """Generate a random integer between min_value and max_value (inclusive).
    For example: min_value=1, max_value=10 returns a number from 1 to 10."""
    if min_value > max_value:
        raise ValueError("min_value must be less than or equal to max_value")
    result = random.randint(min_value, max_value)
    return f"{result} [Powered by My Custom Tools Server]"

# if __name__ == "__main__":
#     mcp.run(transport="http", port=8000)

if __name__ == "__main__":
    import sys
    if "--http" in sys.argv:
        mcp.run(transport="http", port=8000)
    else:
        mcp.run()