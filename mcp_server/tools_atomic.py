"""
Atomic Travel Domain Tools for MCP Server.
Exposes weather, place search, currency conversion, and budget estimation.
"""
from typing import Optional
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool

# Initialize underlying tool classes
_weather_tool = WeatherInfoTool()
_place_tool = PlaceSearchTool()
_calculator_tool = CalculatorTool()
_currency_tool = CurrencyConverterTool()

def get_destination_weather(city: str, forecast: bool = True) -> str:
    """
    Get current weather and optional 5-day weather forecast for any destination city.

    Args:
        city: The name of the city (e.g. "Tokyo", "Paris", "Goa").
        forecast: If True, returns multi-day temperature and condition forecast. If False, returns current weather only.
    """
    try:
        if forecast:
            forecast_tool = _weather_tool.weather_tool_list[1]
            return forecast_tool.invoke({"city": city})
        else:
            current_tool = _weather_tool.weather_tool_list[0]
            return current_tool.invoke({"city": city})
    except Exception as e:
        return f"Error retrieving weather for '{city}': {str(e)}"


def search_destination_attractions(place: str) -> str:
    """
    Search top tourist attractions and landmarks for a destination (Google Places with Tavily web fallback).

    Args:
        place: Name of the destination, city, or area (e.g. "Kyoto", "Rome").
    """
    try:
        attraction_tool = _place_tool.place_search_tool_list[0]
        return attraction_tool.invoke({"place": place})
    except Exception as e:
        return f"Error searching attractions for '{place}': {str(e)}"


def search_destination_restaurants(place: str) -> str:
    """
    Search top-rated restaurants, eateries, and culinary hotspots for a destination.

    Args:
        place: Name of the city or locality (e.g. "Barcelona", "Mumbai").
    """
    try:
        restaurants_tool = _place_tool.place_search_tool_list[1]
        return restaurants_tool.invoke({"place": place})
    except Exception as e:
        return f"Error searching restaurants for '{place}': {str(e)}"


def search_destination_activities(place: str) -> str:
    """
    Search outdoor, cultural, sightseeing, and adventure activities in and around a destination.

    Args:
        place: Name of the destination or area (e.g. "Interlaken", "Bali").
    """
    try:
        activities_tool = _place_tool.place_search_tool_list[2]
        return activities_tool.invoke({"place": place})
    except Exception as e:
        return f"Error searching activities for '{place}': {str(e)}"


def search_destination_transportation(place: str) -> str:
    """
    Search available public transportation, metro, cabs, and transit options for a destination.

    Args:
        place: Destination name (e.g. "London", "Bangkok").
    """
    try:
        transport_tool = _place_tool.place_search_tool_list[3]
        return transport_tool.invoke({"place": place})
    except Exception as e:
        return f"Error searching transportation for '{place}': {str(e)}"


def convert_travel_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Convert a monetary travel expense from one currency to another using live foreign exchange rates.

    Args:
        amount: Numerical amount of money (e.g. 1500.0).
        from_currency: 3-letter source ISO code (e.g. "USD", "EUR", "INR", "JPY").
        to_currency: 3-letter target ISO code (e.g. "INR", "USD", "EUR", "GBP").
    """
    try:
        currency_converter = _currency_tool.currency_converter_tool_list[0]
        converted = currency_converter.invoke({
            "amount": amount,
            "from_currency": from_currency.upper(),
            "to_currency": to_currency.upper()
        })
        return f"{amount} {from_currency.upper()} = {converted:.2f} {to_currency.upper()}"
    except Exception as e:
        return f"Error converting {amount} {from_currency} to {to_currency}: {str(e)}"


def calculate_trip_budget(
    price_per_night: float,
    total_days: int,
    estimated_daily_food_and_activities: float = 0.0,
    transit_cost: float = 0.0
) -> str:
    """
    Calculate full accommodation costs, daily spending budget, and total estimated trip expense.

    Args:
        price_per_night: Approximate hotel/accommodation cost per night.
        total_days: Number of trip days.
        estimated_daily_food_and_activities: Expected daily food, tickets, and miscellaneous spend.
        transit_cost: Total local transportation and flight/train expenses.
    """
    try:
        hotel_total = price_per_night * max(total_days - 1, 1)
        daily_total = estimated_daily_food_and_activities * total_days
        grand_total = hotel_total + daily_total + transit_cost
        per_day_average = grand_total / max(total_days, 1)

        return (
            f"Trip Budget Breakdown ({total_days} days):\n"
            f"- Accommodation ({total_days - 1} nights @ {price_per_night:.2f}/night): {hotel_total:.2f}\n"
            f"- Daily Expenses & Food ({total_days} days @ {estimated_daily_food_and_activities:.2f}/day): {daily_total:.2f}\n"
            f"- Transport & Transit: {transit_cost:.2f}\n"
            f"-----------------------------------------\n"
            f"- Grand Total Estimated Expense: {grand_total:.2f}\n"
            f"- Average Cost Per Day: {per_day_average:.2f}"
        )
    except Exception as e:
        return f"Error calculating budget: {str(e)}"
