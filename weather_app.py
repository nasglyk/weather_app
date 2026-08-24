from langchain.tools import tool
from typing import Dict, Any
from tavily import TavilyClient
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver  
from langchain.messages import HumanMessage
from langchain.agents import create_agent
import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path="C:\\Users\\nasso\\Desktop\\langchain\\lca-lc-foundations\\example.env", override=True)

# Weather api tool set up -----------------------------------------------------------------------------------------

@tool
def get_current_weather(city: str) -> str:
    """
    Get the current weather conditions for a given city using OpenWeatherMap

    Args:
        city: name of the city
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: openwweather key is not set"

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric" # parameters found in 'Built-in API request by city name' https://openweathermap.org/api/current?collection=current_forecast#geo
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if response.status_code == 404:
            return f"Error: City '{city}' not found"
        elif response.status_code != 200:
            return f"Error: Failed to retrieve data ({data.get('message', 'Unknown error')})."

        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        condition = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        return (
            f"Weather in {city.title()}:\n"
            f"- Temperature: {temp}°C (feels like {feels_like}°C)\n"
            f"- Condition: {condition}\n"
            f"- Humidity: {humidity}%"
            f"- Wind Speed: {wind_speed} m/s"
        )

    except requests.exceptions.RequestException as e:
        return f"Network error while fetching weather data: {str(e)}"

# Model configuration -----------------------------------------------------------------------------------------

system_prompt = """ 
You are a weather telling agent. The user will give you a city name and you will return the current weather conditions for that city and clothing suggestions.
Do not mention anything else.
"""

agent = create_agent(
    model="gpt-5-nano",
    tools=[get_current_weather],
    system_prompt=system_prompt
)

def get_weather(city: str) -> str:
    """
    Get the current weather for a specified city using the agent.

    Args:
        city (str): The name of the city (e.g., 'Athens').
    """

    return 

# Main App -----------------------------------------------------------------------------------------

def main():
    print("Welcome to the Weather App! Type 'exit' to quit.")

    while True:
        print('')
        user_question = input("Type your text: ")
        print('')
        if user_question.lower() == 'exit':
            print("Exiting the weather application.")
            break
        weather_info = agent.invoke({"messages": [HumanMessage(content=user_question)]})
        print(weather_info["messages"][-1].content)

if __name__ == "__main__":
    main()