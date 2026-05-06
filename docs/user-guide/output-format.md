# Output format

The backend returns a single field `answer` that contains **Markdown**. The content is produced by the LLM guided by the system prompt in [`prompt_library/prompt.py`](../../prompt_library/prompt.py).

## What the agent aims to include

The system prompt requests:

- Day-by-day itinerary
- Two variants: **tourist** + **off-beat**
- Hotels with approx per-night cost
- Attractions, restaurants, activities, transportation options
- Weather details
- Detailed cost breakdown + daily expense budget

## How to store the output

- Save the raw Markdown as a `.md` file.
- For programmatic use, consider post-processing headings into a structured format.

## Exporting to a file

There is a helper in [`utils/save_to_document.py`](../../utils/save_to_document.py) that writes the response as a Markdown file under `./output` (timestamped name).

## Important disclaimer

The agent uses live sources and APIs. Always verify:

- prices and availability
- opening hours
- travel advisories and entry requirements

