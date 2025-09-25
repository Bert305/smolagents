import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert currency using ExchangeRate-API."""
    try:
        # Use free tier API
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "rates" in data and to_currency in data["rates"]:
            rate = data["rates"][to_currency]
            converted_amount = amount * rate
            return f"💰 {amount} {from_currency} = {converted_amount:.2f} {to_currency} (Rate: {rate:.4f})"
        else:
            return f"❌ Could not find exchange rate for {from_currency} to {to_currency}"

    except Exception as e:
        return f"❌ Error fetching exchange rate: {e}"

def get_weather(location: str, celsius: bool = False) -> str:
    """Get weather using WeatherStack API."""
    api_key = os.getenv("WEATHERSTACK_API_KEY")
    if not api_key:
        return "❌ Weather API key not configured. Please add WEATHERSTACK_API_KEY to your .env file."
    
    try:
        units = "m" if celsius else "f"
        url = f"http://api.weatherstack.com/current?access_key={api_key}&query={location}&units={units}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            return f"❌ Weather API error: {data['error']['info']}"

        current = data["current"]
        location_info = data["location"]
        temp_unit = "°C" if celsius else "°F"
        
        return f"🌤️ Weather in {location_info['name']}, {location_info['country']}:\n" \
               f"   {current['weather_descriptions'][0]}\n" \
               f"   Temperature: {current['temperature']}{temp_unit} (feels like {current['feelslike']}{temp_unit})\n" \
               f"   Humidity: {current['humidity']}%, Wind: {current['wind_speed']} km/h"

    except Exception as e:
        return f"❌ Error fetching weather: {e}"

def get_joke() -> str:
    """Get a random programming joke."""
    try:
        url = "https://v2.jokeapi.dev/joke/Programming?safe-mode&type=single"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("error"):
            return "😅 Sorry, couldn't fetch a joke right now."
        
        if data["type"] == "single":
            return f"😄 {data['joke']}"
        else:
            return f"😄 {data['setup']}\n   {data['delivery']}"

    except Exception as e:
        # Fallback jokes
        fallback_jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
            "Why do Java developers wear glasses? Because they don't C#!"
        ]
        import random
        return f"😄 {random.choice(fallback_jokes)}"

def get_random_fact() -> str:
    """Get a random fact from multiple sources."""
    try:
        # Try uselessfacts.jsph.pl (no API key required)
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "text" in data:
            return f"🧠 Random Fact: {data['text']}"
        
    except Exception as e:
        print(f"Primary fact API failed: {e}")
    
    # Fallback facts
    fallback_facts = [
        "The first computer bug was an actual bug - a moth trapped in a Harvard Mark II computer in 1947.",
        "Python was named after the British comedy group Monty Python, not the snake.",
        "The term 'debugging' was popularized by Admiral Grace Hopper in the 1940s.",
        "The first programmer was Ada Lovelace, who wrote the first algorithm for Charles Babbage's Analytical Engine in 1843.",
        "The '@' symbol was used in email addresses for the first time by Ray Tomlinson in 1971."
    ]
    import random
    return f"🧠 Random Fact: {random.choice(fallback_facts)}"

def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information."""
    try:
        # Use Wikipedia API with proper headers
        headers = {
            "User-Agent": "SmolagentsDemo/1.0 (https://github.com/huggingface/smolagents)"
        }
        
        # First, search for the page
        search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "extract" in data and data["extract"]:
            title = data.get("title", query)
            extract = data["extract"]
            page_url = data.get("content_urls", {}).get("desktop", {}).get("page", "")
            
            return f"📖 Wikipedia - {title}:\n{extract}\n\n🔗 Read more: {page_url}"
        else:
            return f"❌ No Wikipedia summary found for '{query}'."

    except Exception as e:
        return f"❌ Error searching Wikipedia: {e}"

def calculate(expression: str) -> str:
    """Perform safe mathematical calculations."""
    try:
        # Only allow safe mathematical operations
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            return "❌ Invalid characters in expression. Only numbers and basic math operators are allowed."
        
        # Prevent dangerous operations
        dangerous_terms = ['__', 'import', 'exec', 'eval', 'open', 'file']
        if any(term in expression.lower() for term in dangerous_terms):
            return "❌ Invalid expression detected."
        
        result = eval(expression)
        return f"🧮 {expression} = {result}"
    except Exception as e:
        return f"❌ Error calculating '{expression}': {e}"

def run_comprehensive_demo():
    """Run a comprehensive demo of all tools."""
    print("🚀 Smolagents Multi-Tool Demo")
    print("=" * 50)
    
    demos = [
        ("💱 Currency Conversion", lambda: convert_currency(1000, "USD", "EUR")),
        ("🌡️ Weather Check", lambda: get_weather("London")),
        ("😄 Programming Joke", get_joke),
        ("🧠 Random Fact", get_random_fact),
        ("🔍 Wikipedia Search", lambda: search_wikipedia("Artificial Intelligence")),
        ("🧮 Calculator", lambda: calculate("(1000 * 0.85) + 150")),
    ]
    
    for title, func in demos:
        print(f"\n{title}")
        print("-" * 30)
        try:
            result = func()
            print(result)
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Demo complete! All tools are working independently.")
    print("💡 These tools can be integrated with any LLM agent framework.")

if __name__ == "__main__":
    run_comprehensive_demo()