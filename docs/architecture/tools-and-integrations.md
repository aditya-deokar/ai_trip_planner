# Tools and integrations

Tools are defined in `tools/*` and exposed to the agent in [`agent/agentic_workflow.py`](../../agent/agentic_workflow.py).

## Places (Google Places + Tavily fallback)

Source:

- [`tools/place_search_tool.py`](../../tools/place_search_tool.py)
- Google wrapper: [`utils/place_info_search.py`](../../utils/place_info_search.py)

Env vars:

- `GPLACES_API_KEY` (Google Places)
- `TAVILY_API_KEY` (Tavily Search; used by `langchain_tavily`)

Tools (names as the agent sees them):

- `search_attractions(place: str) -> str`
- `search_restaurants(place: str) -> str`
- `search_activities(place: str) -> str`
- `search_transportation(place: str) -> str`

Fallback behavior:

- Try Google Places first.
- On exception, call Tavily and return a combined message noting the fallback.

## Weather (OpenWeatherMap)

Source:

- [`tools/weather_info_tool.py`](../../tools/weather_info_tool.py)
- API wrapper: [`utils/weather_info.py`](../../utils/weather_info.py)

Env var:

- `OPENWEATHERMAP_API_KEY`

Tools:

- `get_current_weather(city: str) -> str`
- `get_weather_forecast(city: str) -> str`

Notes:

- Forecast uses `/forecast` with `cnt=10` and `units=metric`.

## Currency conversion (ExchangeRate-API)

Source:

- [`tools/currency_conversion_tool.py`](../../tools/currency_conversion_tool.py)
- API wrapper: [`utils/currency_convertor.py`](../../utils/currency_convertor.py)

Env var:

- `EXCHANGE_RATE_API_KEY`

Tool:

- `convert_currency(amount: float, from_currency: str, to_currency: str) -> float`

Notes:

- Wrapper calls `https://v6.exchangerate-api.com/v6/<key>/latest/<from_currency>`.

## Expense calculations

Source:

- [`tools/expense_calculator_tool.py`](../../tools/expense_calculator_tool.py)
- helper: [`utils/calculator.py`](../../utils/calculator.py)

Tools:

- `estimate_total_hotel_cost(price_per_night: str, total_days: float) -> float`
- `calculate_total_expense(*costs: float) -> float`
- `calculate_daily_expense_budget(total_cost: float, days: int) -> float`

Notes:

- `estimate_total_hotel_cost` delegates to `Calculator.multiply`. (Be mindful: current types accept `str` for `price_per_night` in the tool signature.)

