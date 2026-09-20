from fastmcp import FastMCP
from datetime import date
import random

# Create the server instance
mcp = FastMCP(name="My Custom Tools Server")


@mcp.tool
def calculate_age(date_of_birth: str) -> str:
    """Calculate a person's current age from their date of birth.
    The date_of_birth must be in YYYY-MM-DD format, for example: 2000-01-15"""

    print(f">>> TOOL CALLED: calculate_age with date_of_birth={date_of_birth}")

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

    # return f"Age: {years} years, {months} months, {days} days"
    return f"Age: {years} years, {months} months, {days} days [Powered by My Custom Tools Server]"

# Tool 2: Random Number Generator
@mcp.tool
def random_number(min_value: int = 0, max_value: int = 100) -> int:
    """Generate a random integer between min_value and max_value (inclusive).
    For example: min_value=1, max_value=10 returns a number from 1 to 10."""

    print(f">>> TOOL CALLED: random_number with min={min_value}, max={max_value}")

    if min_value > max_value:
        raise ValueError("min_value must be less than or equal to max_value")
    return random.randint(min_value, max_value)


# Start the server
if __name__ == "__main__":
    mcp.run()