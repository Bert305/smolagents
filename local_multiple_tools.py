import requests
import os
from dotenv import load_dotenv

# Import smolagents components
from smolagents import CodeAgent, tool

# Try to use a free local model first, fall back to simple responses if not available
try:
    # Try using HuggingFace's free models (no inference API)
    from smolagents import HfApiModel
    model = HfApiModel("microsoft/DialoGPT-medium")  # Free model
except Exception as e:
    print(f"Could not load HF model: {e}")
    # Fallback: create a simple mock model for demonstration
    class MockModel:
        def generate(self, messages, **kwargs):
            return "I'll help you with that task."
        
        def generate_stream(self, messages, **kwargs):
            yield "I'll help you with that task."
    
    model = MockModel()

# Load environment variables
load_dotenv()

@tool
def get_weather(location: str, celsius: bool | None = False) -> str:
    """
    Get the current weather at the given location using the WeatherStack API.

    Args:
        location: The location (city name).
        celsius: Whether to return the temperature in Celsius (default is False, which returns Fahrenheit).

    Returns:
        A string describing the current weather at the location.
    """
    api_key = os.getenv("WEATHERSTACK_API_KEY")
    if not api_key:
        return f"Weather API key not configured. Please add WEATHERSTACK_API_KEY to your .env file."
    
    units = "m" if celsius else "f"  # 'm' for Celsius, 'f' for Fahrenheit
    url = f"http://api.weatherstack.com/current?access_key={api_key}&query={location}&units={units}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            return f"Error fetching weather data: {data['error']['info']}"

        current = data["current"]
        location_info = data["location"]
        
        temp_unit = "°C" if celsius else "°F"
        return f"Weather in {location_info['name']}, {location_info['country']}: {current['weather_descriptions'][0]}, Temperature: {current['temperature']}{temp_unit}, Feels like: {current['feelslike']}{temp_unit}, Humidity: {current['humidity']}%"

    except requests.RequestException as e:
        return f"Error fetching weather data: {e}"

@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Convert currency using ExchangeRate-API.

    Args:
        amount: The amount to convert.
        from_currency: The source currency code (e.g., 'USD').
        to_currency: The target currency code (e.g., 'EUR').

    Returns:
        A string with the converted amount.
    """
    api_key = os.getenv("EXCHANGE_API_KEY")
    
    # Use free tier without API key if not provided
    if api_key:
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}"
    else:
        # Use free tier (limited requests)
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if api_key:
            # Paid API response format
            if "result" in data and data["result"] == "success":
                rate = data["conversion_rate"]
                converted_amount = amount * rate
                return f"{amount} {from_currency} = {converted_amount:.2f} {to_currency} (Rate: {rate})"
            else:
                return f"Error: {data.get('error-type', 'Unknown error')}"
        else:
            # Free API response format
            if "rates" in data and to_currency in data["rates"]:
                rate = data["rates"][to_currency]
                converted_amount = amount * rate
                return f"{amount} {from_currency} = {converted_amount:.2f} {to_currency} (Rate: {rate})"
            else:
                return f"Error: Could not find exchange rate for {from_currency} to {to_currency}"

    except requests.RequestException as e:
        return f"Error fetching exchange rate: {e}"

@tool
def get_joke() -> str:
    """
    Get a random joke from JokeAPI.

    Returns:
        A random joke.
    """
    url = "https://v2.jokeapi.dev/joke/Any?safe-mode&type=single"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data["error"]:
            return "Sorry, couldn't fetch a joke right now."
        
        if data["type"] == "single":
            return data["joke"]
        else:
            return f"{data['setup']} - {data['delivery']}"

    except requests.RequestException as e:
        return f"Error fetching joke: {e}"

@tool
def get_random_fact() -> str:
    """
    Get a random fact from API Ninjas.

    Returns:
        A random fact.
    """
    api_key = os.getenv("API_NINJAS_KEY")
    headers = {}
    
    if api_key:
        headers["X-Api-Key"] = api_key
    
    url = "https://api.api-ninjas.com/v1/facts"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data and len(data) > 0:
            return data[0]["fact"]
        else:
            return "Sorry, couldn't fetch a random fact right now."

    except requests.RequestException as e:
        return f"Error fetching random fact: {e}"

@tool
def search_wikipedia(query: str) -> str:
    """
    Search Wikipedia for information.

    Args:
        query: The search query.

    Returns:
        A summary from Wikipedia.
    """
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "extract" in data:
            return f"Wikipedia summary for '{query}': {data['extract']}"
        else:
            return f"No Wikipedia summary found for '{query}'."

    except requests.RequestException as e:
        return f"Error searching Wikipedia: {e}"

@tool
def calculate(expression: str) -> str:
    """
    Perform simple mathematical calculations.

    Args:
        expression: A mathematical expression to evaluate (e.g., "5000 * 0.85").

    Returns:
        The result of the calculation.
    """
    try:
        # Only allow safe mathematical operations
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression. Only numbers and basic math operators are allowed."
        
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error calculating '{expression}': {e}"

# Simple demo function that doesn't require LLM
def run_tool_demos():
    """Run demonstrations of each tool without requiring an LLM."""
    print("=== Tool Demonstrations ===\n")
    
    print("1. Currency Conversion (5000 USD to EUR):")
    result = convert_currency(5000, "USD", "EUR")
    print(f"   {result}\n")
    
    print("2. Simple Calculation:")
    result = calculate("5000 * 0.85")
    print(f"   {result}\n")
    
    print("3. Random Joke:")
    result = get_joke()
    print(f"   {result}\n")
    
    print("4. Random Fact:")
    result = get_random_fact()
    print(f"   {result}\n")
    
    print("5. Wikipedia Search (Python):")
    result = search_wikipedia("Python_programming_language")
    print(f"   {result[:200]}...\n")
    
    print("6. Weather (if API key configured):")
    result = get_weather("New York")
    print(f"   {result}\n")

if __name__ == "__main__":
    print("Multiple Tools Demo - Local Version")
    print("====================================\n")
    
    # First, demonstrate the tools directly
    run_tool_demos()
    
    print("\n=== Agent Integration ===")
    print("Note: Agent functionality requires a working LLM model.")
    print("The tools above work independently and can be integrated with any agent framework.")