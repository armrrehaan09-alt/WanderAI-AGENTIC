# WanderAI Hackathon

AI-powered agentic travel planner with human approval and PDF trip-summary generation.

## Project structure

- `app.py` — Streamlit UI, image rendering, human approval flow and PDF download
- `agent.py` — travel agent, parsing, orchestration, itinerary and replanning logic
- `pdf_utils.py` — approved-trip PDF generation
- `tools/travel_tools.py` — travel, flight, hotel, activity, food, weather and budget tools
- `test_wanderai.py` — regression and reliability test suite
- `requirements.txt` — Python dependencies

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Set `GEMINI_API_KEY` in the environment before using Gemini-backed planning.

## Human-in-the-loop flow

1. User submits a natural-language travel request.
2. WanderAI plans the trip and gathers tool results.
3. The user reviews the proposed trip.
4. Approval is required before PDF generation.
5. If the user requests changes, WanderAI replans and asks for approval again.
6. After approval, the user can download the trip summary PDF.

## Testing

```bash
python test_wanderai.py
```

The suite covers destination parsing, itinerary generation, airport catalog integrity, failure handling, image semantics, regression scenarios, human approval gating and PDF generation.
