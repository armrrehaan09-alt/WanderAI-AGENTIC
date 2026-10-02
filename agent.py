import json
import os
import re
import unicodedata
from datetime import date
from urllib.parse import urlencode
from urllib.request import Request, urlopen

try:
    from google import genai
    from google.genai import types
except Exception:
    genai = None
    types = None

from tools.travel_tools import (
    AIRPORT_DESTINATIONS,
    activity_tool,
    budget_tool,
    flight_tool,
    food_tool,
    geocode_destination,
    hotel_tool,
    weather_tool,
)


class TravelAgent:
    """WanderAI's request-understanding and live-tool orchestration layer."""

    COUNTRY_PROMPT_ALIASES = {
        "saudi arabia": "Saudi Arabia", "united arab emirates": "United Arab Emirates",
        "uae": "United Arab Emirates", "qatar": "Qatar", "oman": "Oman",
        "japan": "Japan", "france": "France", "italy": "Italy", "spain": "Spain",
        "germany": "Germany", "netherlands": "Netherlands", "switzerland": "Switzerland",
        "united kingdom": "United Kingdom", "uk": "United Kingdom",
        "united states": "United States", "usa": "United States", "canada": "Canada",
        "australia": "Australia", "new zealand": "New Zealand", "singapore": "Singapore",
        "malaysia": "Malaysia", "thailand": "Thailand", "indonesia": "Indonesia",
        "philippines": "Philippines", "vietnam": "Vietnam", "south korea": "South Korea",
        "china": "China", "nepal": "Nepal", "sri lanka": "Sri Lanka", "maldives": "Maldives",
        "bangladesh": "Bangladesh", "egypt": "Egypt", "morocco": "Morocco",
        "south africa": "South Africa", "kenya": "Kenya", "tanzania": "Tanzania",
        "zimbabwe": "Zimbabwe", "zambia": "Zambia", "nigeria": "Nigeria",
        "ghana": "Ghana", "rwanda": "Rwanda", "uganda": "Uganda", "ethiopia": "Ethiopia",
        "brazil": "Brazil", "mexico": "Mexico", "argentina": "Argentina",
        "turkey": "Turkey", "greece": "Greece", "portugal": "Portugal",
        "austria": "Austria", "ireland": "Ireland", "india": "India",
    }

    def __init__(self):
        self.tools = {
            "flight": flight_tool,
            "hotel": hotel_tool,
            "weather": weather_tool,
            "activity": activity_tool,
            "food": food_tool,
        }
        self.client = None
        self.model_name = "gemini-3.8-flash"

        try:
            # Keep Gemini responsive inside Streamlit. The SDK supports a client-level
            # HTTP timeout in milliseconds. If the API is slow/unavailable, WanderAI
            # falls back to its deterministic itinerary instead of hanging the UI.
            if genai is not None:
                if types is not None and hasattr(types, "HttpOptions"):
                    self.client = genai.Client(http_options=types.HttpOptions(timeout=15000))
                else:
                    self.client = genai.Client(http_options={"timeout": 15000})
            else:
                self.client = None
        except Exception:
            self.client = None

    def _safe_json(self, raw):
        raw = (raw or "").strip()
        raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.I)
        raw = re.sub(r"\s*```$", "", raw)
        return json.loads(raw)

    def extract_budget(self, text):
        text_lower = text.lower().replace(",", "")
        patterns = [
            r"(?:under|below|within|budget(?:\s+of)?|less\s+than)\s*(?:₹|rs\.?|rupees)?\s*(\d+(?:\.\d+)?)\s*(k)?",
            r"(?:₹|rs\.?|rupees)\s*(\d+(?:\.\d+)?)\s*(k)?",
        ]
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                value = float(match.group(1))
                if match.group(2) == "k":
                    value *= 1000
                return int(value)
        return None

    def extract_nights(self, text):
        lower = (text or "").lower()
        match = re.search(r"(\d+)\s*night", lower)
        if match:
            return max(1, int(match.group(1)))
        match = re.search(r"(\d+)\s*day", lower)
        if match:
            return max(1, int(match.group(1)) - 1)
        match = re.search(r"(?:for|of|about|around)?\s*(\d+)\s*week", lower)
        if match:
            return max(1, int(match.group(1)) * 7 - 1)
        if re.search(r"\ba\s+week\b|\bone\s+week\b", lower):
            return 6
        if re.search(r"\bweekend\b", lower):
            return 2
        return 3

    def extract_destination_locally(self, text):
        """Extract the intended travel destination from conversational text.

        Strategy:
        1. Match the longest known destination/region from the global airport-aware
           catalog anywhere in the sentence. This is deterministic and prevents
           phrases like "Kerala. Nothing too hectic" or "Paris pls, romantic vibes"
           from leaking into the geocoder.
        2. Handle explicit travel constructions for destinations outside the catalog.
        3. Use a conservative proper-name fallback only when needed.

        The method returns only the place phrase, never the surrounding preferences.
        """
        raw = re.sub(r"\s+", " ", (text or "").strip())
        if not raw:
            return None

        # Normalize apostrophes/dashes and accents so destinations such as
        # Malé / Male and São Paulo / Sao Paulo resolve identically.
        searchable = raw.replace("’", "'").replace("–", "-").replace("—", "-")
        searchable_normalized = unicodedata.normalize("NFKD", searchable).encode("ascii", "ignore").decode("ascii")
        searchable_normalized = re.sub(r"[^A-Za-z0-9]+", " ", searchable_normalized).strip()

        # Explicit "place, country" syntax gets priority over the country name
        # itself. This fixes inputs such as "Male, Maldives" and "Goa, India".
        if "," in raw:
            first_part = re.sub(r"\s+", " ", raw.split(",", 1)[0]).strip()
            first_part = re.sub(r"^(?:plan|travel|trip|go|head|take me to|for|about)\s+", "", first_part, flags=re.I)
            first_part = re.sub(r"^\d+\s+(?:day|days|night|nights)\s+(?:in|at|to)\s+", "", first_part, flags=re.I)
            first_norm = unicodedata.normalize("NFKD", first_part).encode("ascii", "ignore").decode("ascii")
            first_norm = re.sub(r"[^A-Za-z0-9]+", " ", first_norm.lower()).strip()
            for key in sorted((str(k) for k in AIRPORT_DESTINATIONS.keys() if str(k).strip()), key=len, reverse=True):
                key_norm = unicodedata.normalize("NFKD", key).encode("ascii", "ignore").decode("ascii")
                key_norm = re.sub(r"[^a-z0-9]+", " ", key_norm.lower()).strip()
                if first_norm == key_norm:
                    return key

        # ------------------------------------------------------------
        # 1) Deterministic known-destination matching.
        # Longest match wins, so "New York" beats "York", etc.
        # Only match complete word/phrase boundaries.
        # ------------------------------------------------------------
        known_keys = sorted(
            (str(key) for key in AIRPORT_DESTINATIONS.keys()
             if str(key).strip()),
            key=len,
            reverse=True,
        )

        known_matches = []
        for key in known_keys:
            normalized_key = unicodedata.normalize("NFKD", key).encode("ascii", "ignore").decode("ascii")
            normalized_key = re.sub(r"[^a-z0-9]+", " ", normalized_key.lower()).strip()
            pattern = rf"(?<![A-Za-z0-9]){re.escape(normalized_key)}(?![A-Za-z0-9])"
            match = re.search(pattern, searchable_normalized, flags=re.I)
            if match:
                # Never interpret a comparison country in "somewhere outside X"
                # as the destination when the request does not name a destination.
                prefix = searchable_normalized[:match.start()].lower()
                if re.search(r"\bsomewhere\s+outside\s*$", prefix):
                    continue
                known_matches.append((len(key), match.start(), key))

        if known_matches:
            # Prefer the longest name; for equal length, prefer the occurrence
            # closest to the end because destinations are often mentioned last.
            known_matches.sort(key=lambda item: (item[0], item[1]), reverse=True)
            return known_matches[0][2]

        # Also match canonical display names from the airport catalog. This is
        # important for entries such as "Victoria, Seychelles" whose catalog key
        # is "victoria seychelles", and "Washington, D.C." whose key is
        # "washington dc".
        canonical_matches = []
        for catalog_key, entry in AIRPORT_DESTINATIONS.items():
            canonical = str(entry.get("canonical") or "").strip()
            if not canonical:
                continue
            normalized_canonical = unicodedata.normalize("NFKD", canonical).encode("ascii", "ignore").decode("ascii")
            normalized_canonical = re.sub(r"[^a-z0-9]+", " ", normalized_canonical.lower()).strip()
            variants = [normalized_canonical]
            compact_initials = re.sub(r"\b([a-z])\s+([a-z])\b", r"\1\2", normalized_canonical)
            if compact_initials != normalized_canonical:
                variants.append(compact_initials)
            matched = None
            matched_len = 0
            for variant in variants:
                pattern = rf"(?<![A-Za-z0-9]){re.escape(variant)}(?![A-Za-z0-9])"
                candidate_match = re.search(pattern, searchable_normalized, flags=re.I)
                if candidate_match and len(variant) > matched_len:
                    matched = candidate_match
                    matched_len = len(variant)
            if matched:
                canonical_matches.append((matched_len, matched.start(), catalog_key))
        if canonical_matches:
            canonical_matches.sort(key=lambda item: (item[0], item[1]), reverse=True)
            return canonical_matches[0][2]

        # Country-level prompts are supported without pretending that a whole
        # country is one attraction. This check intentionally happens AFTER
        # known city matching, so "Goa, India" still resolves to Goa.
        for country_key, country_label in sorted(self.COUNTRY_PROMPT_ALIASES.items(), key=lambda x: len(x[0]), reverse=True):
            pattern = rf"(?<![A-Za-z0-9]){re.escape(country_key)}(?![A-Za-z0-9])"
            match = re.search(pattern, searchable_normalized, flags=re.I)
            if match:
                prefix = searchable_normalized[:match.start()].lower()
                if re.search(r"\boutside(?:\s+of)?\s*$", prefix):
                    continue
                return country_label

        # ------------------------------------------------------------
        # 2) Explicit travel-language patterns for arbitrary places.
        # ------------------------------------------------------------
        vague_destination_starts = (
            "somewhere", "anywhere", "someplace", "beautiful", "warm",
            "peaceful", "relaxing", "cheap", "affordable", "luxury",
            "nearby", "abroad", "overseas", "local", "random", "unknown",
            "i ", "we ", "want ", "need ", "looking for ", "a ", "an ",
            "the ", "plan ", "please ", "take me ", "give me ",
        )

        def is_vague_candidate(value):
            normalized = re.sub(r"\s+", " ", str(value or "").strip().lower())
            if not normalized:
                return True
            if normalized in {"somewhere", "anywhere", "someplace", "abroad", "overseas"}:
                return True
            return any(normalized.startswith(prefix.strip()) for prefix in vague_destination_starts)

        def clean_candidate(value):
            value = re.sub(r"[\U00010000-\U0010ffff]", " ", value)
            value = re.sub(r"\s+", " ", value).strip(" .,!?:;-")
            value = re.sub(
                r"\s+(?:pls|please|maybe|perhaps|though|lol|thanks)$",
                "",
                value,
                flags=re.I,
            ).strip(" .,!?:;-")
            value = re.sub(r"^(?:the|a|an)\s+", "", value, flags=re.I)
            return value.strip(" .,!?:;-")

        # Words that commonly begin a new constraint/preference clause.
        stop_words = (
            r"with|for|under|below|within|budget|on|from|mainly|mostly|"
            r"especially|focusing|focused|because|since|who|that|but|"
            r"and|this|these|tomorrow|today|tonight|weekend|next|"
            r"nothing|something|some|good|great|romantic|adventure|nature|"
            r"food|shopping|nightlife|culture|beaches|beach"
        )
        stop = rf"(?=\s+(?:{stop_words})\b|\s*(?:[,.!?;:]|$))"

        patterns = [
            rf"\b\d+\s+(?:day|days|night|nights)\s+(?:in|at)\s+"
            rf"([A-Za-z][A-Za-z0-9 .&'/-]{{1,100}}?){stop}",
            rf"\b(?:trip|travel|journey|holiday|vacation)\s+(?:to|in|at)\s+"
            rf"([A-Za-z][A-Za-z0-9 .&'/-]{{1,100}}?){stop}",
            rf"\b(?:go|head|going|fly|travel|escape|escaping|escaped)\s+to\s+"
            rf"([A-Za-z][A-Za-z0-9 .&'/-]{{1,100}}?){stop}",
            rf"\b(?:visit|explore|experience)\s+"
            rf"([A-Za-z][A-Za-z0-9 .&'/-]{{1,100}}?){stop}",
            rf"\b(?:spend|stay)\s+\d+\s+(?:day|days|night|nights)\s+(?:in|at)\s+"
            rf"([A-Za-z][A-Za-z0-9 .&'/-]{{1,100}}?){stop}",
            rf"\b(?:somewhere|anywhere)\s+(?:in|near)\s+"
            rf"([A-Za-z][A-Za-z0-9 .&'/-]{{1,100}}?){stop}",
        ]

        for pattern in patterns:
            match = re.search(pattern, searchable, flags=re.I)
            if match:
                candidate = clean_candidate(match.group(1))
                if candidate and len(candidate.split()) <= 8 and not is_vague_candidate(candidate):
                    return candidate

        # "Paris pls", "Bali maybe", "Thinking about Tokyo"
        soft_patterns = [
            r"\bmaybe\s+([A-Za-z][A-Za-z0-9 .&'/-]{1,80}?)(?=\s*(?:[,.!?;:]|$))",
            r"\bthinking\s+(?:about\s+|of\s+)?([A-Za-z][A-Za-z0-9 .&'/-]{1,80}?)(?=\s*(?:[,.!?;:]|$))",
            r"\bconsidering\s+([A-Za-z][A-Za-z0-9 .&'/-]{1,80}?)(?=\s*(?:[,.!?;:]|$))",
            r"\b(?:choose|chose|pick|picked)\s+([A-Za-z][A-Za-z0-9 .&'/-]{1,80}?)(?=\s+(?:because|since|for|with|and)\b|\s*[,.!?;:]|$)",
            r"\b([A-Za-z][A-Za-z0-9 .&'/-]{1,80}?)\s+(?:sounds good|is on my list|has been on my list)\b",
        ]
        for pattern in soft_patterns:
            match = re.search(pattern, searchable, flags=re.I)
            if match:
                candidate = clean_candidate(match.group(1))
                if candidate:
                    # Do not turn a vague preference such as "somewhere warm"
                    # into a fake destination. Explicit "somewhere in <place>"
                    # requests are handled by the pattern above.
                    if is_vague_candidate(candidate):
                        continue
                    return candidate

        # "Goa trip for 4 days", "Kashmir holiday"
        match = re.search(
            r"\b([A-Za-z][A-Za-z0-9 .&'/-]{1,100}?)\s+"
            r"(?:trip|travel|journey|holiday|vacation)\b",
            searchable,
            flags=re.I,
        )
        if match:
            candidate = clean_candidate(match.group(1))
            candidate = re.sub(
                r"^(?:i\s+(?:want|would like)\s+to|please|plan|a)\s+",
                "",
                candidate,
                flags=re.I,
            ).strip(" .,!?:;-")
            if candidate and len(candidate.split()) <= 8 and not is_vague_candidate(candidate):
                return candidate

        # "I have ... Manali", "week free ... Tokyo". Conservative fallback.
        if re.search(r"\bsomewhere\s+outside\s+[A-Z][A-Za-z-]+", searchable, flags=re.I):
            return None

        common = {
            "I", "Me", "My", "We", "The", "A", "An", "Okay", "If", "Thinking",
            "Maybe", "Please", "Plan", "Want", "Have", "Got", "And", "Nothing",
            "What", "Where", "How", "Finally", "Surprise", "Two", "Three",
            "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
        }
        candidates = []
        for match in re.finditer(
            r"\b([A-Z][a-z]{2,}(?:\s+(?:[A-Z][a-z]{2,}|of|the|and)){0,4})\b",
            searchable,
        ):
            candidate = clean_candidate(match.group(1))
            if not candidate:
                continue
            if candidate.split()[0] in common or match.start() == 0:
                continue
            if is_vague_candidate(candidate):
                continue
            candidates.append(candidate)

        if candidates:
            return candidates[-1]

        match = re.match(
            r"^([A-Za-z][A-Za-z0-9 .&'/-]{1,100}?)"
            r"(?:\s+\d+\s+(?:day|days|night|nights))(?:\s+.*)?$",
            searchable,
            flags=re.I,
        )
        if match:
            candidate = clean_candidate(match.group(1))
            if candidate and candidate.lower() not in {"plan", "a", "trip", "travel"} and not is_vague_candidate(candidate):
                return candidate

        return None

    def select_tools_locally(self, text):
        # These are the core travel-planning tools. The budget calculator is
        # always executed by run(), so keep the selected-tool list consistent.
        return ["weather", "activity", "hotel", "flight", "budget"]

    def understand_request(self, request):
        """Parse the request quickly, using Gemini only when local parsing is insufficient.

        Simple requests such as ``Plan a 3 day trip to Kashmir`` should never wait
        for an LLM call just to identify the destination. This removes the main
        source of the long spinner seen in the Streamlit UI.
        """
        destination = self.extract_destination_locally(request)
        nights = self.extract_nights(request)
        budget_limit = self.extract_budget(request)
        selected_tools = self.select_tools_locally(request)
        gemini_success = False

        # Only ask Gemini to interpret genuinely ambiguous requests. This is a
        # single bounded call; failures immediately fall back to local parsing.
        if not destination and self.client:
            prompt = f"""You extract travel-request fields for WanderAI.
Return ONLY the requested JSON fields.

User request:
{request}

DESTINATION RULES:
- Extract ONLY the actual place/city/country the user wants to travel to.
- Ignore every other word describing the trip, people, budget, duration, mood or interests.
- Examples:
  "Me and 3 friends have 5 days off... Manali" -> destination "Manali"
  "My parents ... 4-day vacation somewhere in Kerala. Nothing too hectic" -> "Kerala"
  "3 days in Paris pls, romantic vibes" -> "Paris"
  "Adventure... Maybe Bali" -> "Bali"
  "I finally have a week free. Thinking Tokyo..." -> "Tokyo"
  "Surprise me... somewhere outside India..." -> destination null because no destination is specified.
- If no destination is explicitly named, return null. Do not guess.

OTHER RULES:
- nights defaults to 3.
- budget_limit may be null.
- tools should normally contain flight, hotel, weather, activity, and budget when a complete trip is requested."""
            try:
                extraction_schema = {
                    "type": "object",
                    "properties": {
                        "destination": {"type": ["string", "null"]},
                        "nights": {"type": "integer"},
                        "budget_limit": {"type": ["integer", "null"]},
                        "tools": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["destination", "nights", "budget_limit", "tools"],
                }
                config = {
                    "temperature": 0.0,
                    "max_output_tokens": 250,
                    "response_mime_type": "application/json",
                    "response_schema": extraction_schema,
                }
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=config,
                )
                data = self._extract_json_response(response)
                destination = data.get("destination") or destination
                nights = data.get("nights") or nights
                budget_limit = data.get("budget_limit") if data.get("budget_limit") is not None else budget_limit
                selected_tools = data.get("tools") or selected_tools
                gemini_success = bool(destination)
            except Exception:
                pass

        # Never allow a clearly invalid multi-word conversational phrase to pass
        # through as a destination. A destination should not contain common request
        # filler such as "have 5 days", "want to", or "romantic vibes".
        if isinstance(destination, str):
            destination = re.sub(r"\s+", " ", destination).strip(" .,!?:;-")
            destination = re.sub(
                r"\s+(?:pls|please|maybe)$", "", destination, flags=re.I
            ).strip(" .,!?:;-")

            # "somewhere warm", "anywhere cheap", etc. are preferences, not
            # destinations. Never send those phrases to the geocoder.
            if re.match(
                r"^(?:somewhere|anywhere|someplace)\b",
                destination,
                flags=re.I,
            ):
                destination = None

            if destination and re.search(
                r"\b(?:i|me|we|my|our|friends|parents|have|want|days|nights|"
                r"budget|romantic|vibes|adventure|food|nature|shopping|nightlife)\b",
                destination,
                flags=re.I,
            ) and len(destination.split()) > 3:
                destination = None

        allowed = {"flight", "hotel", "weather", "activity", "budget"}
        selected_tools = [tool for tool in (selected_tools or []) if tool in allowed]
        if not selected_tools:
            selected_tools = ["flight", "hotel", "weather", "activity"]

        return {
            "destination": destination,
            "nights": max(1, int(nights or 3)),
            "budget_limit": budget_limit,
            "tools": selected_tools,
            "gemini_success": gemini_success,
        }


    def generate_daywise_itinerary(self, destination, nights, interests=None,
                                   weather=None, activities=None, request="", location=None):
        """Generate a useful destination-specific itinerary with layered fallbacks.

        The old implementation silently returned a generic fallback whenever the
        Gemini call failed. That made a Kashmir request look like the model had
        planned Kashmir even when it had not. This version uses three layers:
        1) Gemini structured JSON, 2) Gemini plain JSON retry, 3) deterministic
        destination/activity fallback. The UI always receives the same schema.
        """
        days = max(1, int(nights) + 1)
        interest_text = ", ".join(interests or []) or "general sightseeing, food, culture, nature"
        weather_text = json.dumps(weather, ensure_ascii=False)[:5000] if weather else "No weather data available."

        activity_options = []
        if isinstance(activities, dict):
            activity_options = activities.get("options") or []
        elif isinstance(activities, list):
            activity_options = activities

        clean_activity_options = []
        for item in activity_options:
            if not isinstance(item, dict):
                continue
            name = item.get("name") or item.get("title") or item.get("activity")
            if name:
                clean_activity_options.append({
                    "name": str(name),
                    "category": str(item.get("category") or "Attraction"),
                    "cost": item.get("cost"),
                })

        activity_text = json.dumps(clean_activity_options, ensure_ascii=False)[:9000]
        if not activity_text:
            activity_text = "No attraction tool results are currently available."

        schema = {
            "type": "object",
            "properties": {
                "days": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "day": {"type": "integer"},
                            "title": {"type": "string"},
                            "theme": {"type": "string"},
                            "morning": {"type": "array", "items": {
                                "type": "object",
                                "properties": {"name": {"type": "string"}, "description": {"type": "string"}},
                                "required": ["name", "description"],
                            }},
                            "afternoon": {"type": "array", "items": {
                                "type": "object",
                                "properties": {"name": {"type": "string"}, "description": {"type": "string"}},
                                "required": ["name", "description"],
                            }},
                            "evening": {"type": "array", "items": {
                                "type": "object",
                                "properties": {"name": {"type": "string"}, "description": {"type": "string"}},
                                "required": ["name", "description"],
                            }},
                            "food": {"type": "string"},
                            "estimated_day_cost": {"type": "string"},
                            "travel_note": {"type": "string"},
                        },
                        "required": [
                            "day", "title", "theme", "morning", "afternoon",
                            "evening", "food", "estimated_day_cost", "travel_note",
                        ],
                    },
                }
            },
            "required": ["days"],
        }

        prompt = f"""
You are the itinerary-planning agent inside WanderAI.
Create a practical, destination-specific itinerary.

Destination: {destination}
Trip length: {days} days ({nights} nights)
Traveler interests: {interest_text}
Original request: {request}

Current weather/tool information:
{weather_text}

Attractions returned by the travel tool:
{activity_text}

Important planning rules:
- Return exactly {days} day objects.
- Use specific real attractions and experiences that belong to {destination}.
- If attraction-tool results are present, strongly prefer those exact attraction names.
- Do NOT turn missing live data into fake prices, bookings, hotels or flights.
- Do NOT invent ticket prices. Use "Included", "Free", or "Check current price" when needed.
- Day 1 should be arrival/check-in friendly.
- The final day should be departure-friendly when appropriate.
- Group geographically sensible experiences together and avoid repeating major attractions.
- Keep morning, afternoon and evening concise: normally 1-2 activities each.
- Include a useful local food suggestion and a practical travel note for every day.
- Make the itinerary visibly different for different destinations; never use generic
  labels such as only "Explore {destination}" when a specific attraction is known.

Return ONLY JSON in this exact shape:
{{
  "days": [
    {{
      "day": 1,
      "title": "short title",
      "theme": "short theme",
      "morning": [{{"name":"specific place/activity","description":"short practical description"}}],
      "afternoon": [{{"name":"specific place/activity","description":"short practical description"}}],
      "evening": [{{"name":"specific place/activity","description":"short practical description"}}],
      "food": "local food suggestion",
      "estimated_day_cost": "Free / Included / Check current price",
      "travel_note": "short practical note"
    }}
  ]
}}
"""

        # Layer 1: structured output. Google documents response_mime_type +
        # response_schema for predictable JSON output in generate_content.
        if self.client:
            try:
                # Use a plain config dictionary so response_schema and the
                # per-request HTTP timeout work across recent google-genai SDKs.
                # There is deliberately only ONE Gemini itinerary request here.
                config = {
                    "temperature": 0.25,
                    "max_output_tokens": 900,
                    "response_mime_type": "application/json",
                    "response_schema": schema,
                    "http_options": {"timeout": 15000},
                }

                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=config,
                )
                data = self._extract_json_response(response)
                normalized = self._normalize_generated_days(data, days, destination)
                if normalized and self._has_specific_itinerary(normalized, destination):
                    # Defense-in-depth: never trust the model output directly.
                    # Repair it into exactly `days` x 3 unique itinerary slots.
                    repaired = self._repair_itinerary(
                        normalized,
                        days,
                        destination,
                        clean_activity_options,
                    )
                    if self._is_valid_itinerary(repaired, days):
                        return repaired
            except Exception:
                pass

        # Layer 3: use actual tool activities first, then a destination-specific
        # knowledge fallback. This prevents the UI from displaying misleading
        # generic text when Gemini or the attraction API is temporarily unavailable.
        return self._fallback_itinerary(destination, days, clean_activity_options, location=location)

    @staticmethod
    def _extract_json_response(response):
        """Extract JSON from a Gemini response, including parsed structured output."""
        parsed = getattr(response, "parsed", None)
        if parsed is not None:
            if isinstance(parsed, dict):
                return parsed
            try:
                if hasattr(parsed, "model_dump"):
                    return parsed.model_dump()
                if hasattr(parsed, "dict"):
                    return parsed.dict()
            except Exception:
                pass

        raw = (getattr(response, "text", None) or "").strip()
        if not raw:
            raise ValueError("Gemini returned an empty itinerary response")
        raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.I)
        raw = re.sub(r"\s*```$", "", raw)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", raw, flags=re.S)
            if not match:
                raise
            return json.loads(match.group(0))

    def _normalize_generated_days(self, data, days, destination):
        if not isinstance(data, dict):
            return []
        generated_days = data.get("days")
        if not isinstance(generated_days, list) or len(generated_days) < days:
            return []

        normalized = []
        for index, item in enumerate(generated_days[:days], start=1):
            if not isinstance(item, dict):
                continue
            normalized.append({
                "day": int(item.get("day") or index),
                "title": str(item.get("title") or f"Explore {destination}"),
                "theme": str(item.get("theme") or "Sightseeing & local experiences"),
                "morning": self._normalize_itinerary_items(item.get("morning")),
                "afternoon": self._normalize_itinerary_items(item.get("afternoon")),
                "evening": self._normalize_itinerary_items(item.get("evening")),
                "food": str(item.get("food") or "Try a local specialty"),
                "estimated_day_cost": str(item.get("estimated_day_cost") or "Check current price"),
                "travel_note": str(item.get("travel_note") or "Confirm opening hours and local travel time before visiting."),
            })

        return normalized if len(normalized) == days else []

    @staticmethod
    @staticmethod
    def _normalize_itinerary_items(items):
        if not isinstance(items, list):
            return []
        normalized = []
        for item in items[:3]:
            if isinstance(item, dict):
                name = item.get("name") or item.get("title") or item.get("activity")
                description = item.get("description") or item.get("category") or "Recommended experience"
            else:
                name = str(item)
                description = "Recommended experience"
            if name:
                normalized.append({"name": str(name), "description": str(description)})
        return normalized

    @staticmethod
    def _activity_key(name):
        return re.sub(r"[^a-z0-9]+", " ", str(name).lower()).strip()

    def _unique_fallback_pool(self, destination):
        """Return extra non-repeating planning slots for long trips.

        These are deliberately framed as experiences/free time rather than
        pretending they are named attractions. They are used only after the
        available named attractions have been consumed.
        """
        return [
            {
                "name": f"{destination} local food experience",
                "description": f"Try a locally associated dish or neighbourhood dining area in {destination}.",
            },
            {
                "name": f"{destination} neighbourhood walk",
                "description": f"Take a relaxed walk through a suitable local neighbourhood in {destination}.",
            },
            {
                "name": f"{destination} café & leisure time",
                "description": f"Keep some unhurried time for a café, rest or spontaneous local stop in {destination}.",
            },
            {
                "name": f"{destination} local market experience",
                "description": f"Browse a suitable local market or shopping area after checking opening hours.",
            },
            {
                "name": f"{destination} sunset / evening walk",
                "description": f"Choose a safe, accessible evening spot based on local weather and conditions.",
            },
            {
                "name": f"{destination} relaxed morning",
                "description": f"Start slowly and leave flexible time for the area around your accommodation.",
            },
            {
                "name": f"{destination} departure preparation",
                "description": "Pack, check transport timing and leave buffer time before departure.",
            },
        ]

    @staticmethod
    def _slot_score(item, slot):
        """Score an itinerary candidate for a time of day. Higher is better."""
        text = (str(item.get("name", "")) + " " + str(item.get("description", ""))).lower()
        morning = ("morning", "breakfast", "sunrise", "temple", "museum", "garden", "market", "old town", "palace", "heritage", "fort", "monument")
        afternoon = ("museum", "shopping", "market", "beach", "waterfront", "garden", "palace", "city", "mall", "cafe", "sightseeing")
        evening = ("sunset", "evening", "night", "nightlife", "corniche", "waterfront", "beach", "boulevard", "skyline", "dinner", "cafe", "market")
        if slot == "morning":
            return sum(3 for token in morning if token in text) - sum(6 for token in ("sunset", "night", "evening") if token in text)
        if slot == "afternoon":
            return sum(3 for token in afternoon if token in text) - sum(5 for token in ("sunrise", "sunset", "night") if token in text)
        return sum(3 for token in evening if token in text) - sum(6 for token in ("sunrise", "breakfast", "morning") if token in text)

    def _assign_time_slots(self, candidates):
        remaining = list(candidates)
        assigned = {}
        for slot in ("morning", "afternoon", "evening"):
            if not remaining:
                break
            ranked = sorted(enumerate(remaining), key=lambda pair: (self._slot_score(pair[1], slot), -pair[0]), reverse=True)
            index, item = ranked[0]
            assigned[slot] = dict(item)
            remaining.pop(index)
        return assigned

    @staticmethod
    def _is_generic_itinerary_name(name):
        """Identify generic filler that should not displace named attractions."""
        normalized = unicodedata.normalize("NFKD", str(name or "")).encode("ascii", "ignore").decode("ascii").lower()
        normalized = re.sub(r"[^a-z0-9]+", " ", normalized).strip()
        markers = (
            "local food experience", "neighbourhood walk", "neighborhood walk",
            "cafe leisure time", "local market experience", "sunset evening walk",
            "relaxed morning", "departure preparation", "city area exploration",
            "city highlights", "local market", "scenic area", "local exploration",
            "flexible experience", "cultural or scenic area", "local specialty",
            "regional dish", "market or neighbourhood", "market or neighborhood",
            "evening viewpoint",
        )
        return any(marker in normalized for marker in markers)

    def _repair_itinerary(self, days_data, days, destination, activity_options=None):
        """Harden an itinerary against repetition, missing slots and bad model output.

        This is the final itinerary gate. It does not assume Gemini followed the
        prompt. It builds one global unique candidate pool and then fills exactly
        three slots per day without ever reusing a normalized activity name.
        """
        days = max(1, int(days or 1))
        source_days = days_data if isinstance(days_data, list) else []

        # Candidate priority: model suggestions first, then tool results, then
        # destination-specific knowledge, then safe flexible experiences.
        candidates = []

        def add_candidate(item):
            if not isinstance(item, dict):
                return
            name = str(item.get("name") or item.get("title") or item.get("activity") or "").strip()
            if not name:
                return

            # When destination-specific named places are available, do not let
            # generic LLM filler consume itinerary slots before those places.
            # This fixes outputs such as "Paris neighbourhood walk" appearing
            # while real Paris attractions are still unused.
            normalized_name = self._activity_key(name)
            destination_key = re.sub(r"[^a-z0-9]+", " ", str(destination).lower()).strip()
            if self.DESTINATION_FALLBACKS.get(destination_key) and self._is_generic_itinerary_name(name):
                return

            desc = str(item.get("description") or item.get("category") or "Recommended experience").strip()
            candidates.append({"name": name, "description": desc})

        # Preserve the model's first-seen suggestions.
        for day in source_days:
            if not isinstance(day, dict):
                continue
            for slot in ("morning", "afternoon", "evening"):
                for item in day.get(slot, []) or []:
                    add_candidate(item)

        # Then prefer exact attraction-tool names.
        for item in activity_options or []:
            if isinstance(item, dict):
                add_candidate({
                    "name": item.get("name") or item.get("title") or item.get("activity"),
                    "description": item.get("description") or item.get("category") or "Current attraction result.",
                })

        # Then destination-specific safety-net knowledge.
        key = re.sub(r"[^a-z0-9]+", " ", str(destination).lower()).strip()
        for name, desc in self.DESTINATION_FALLBACKS.get(key, []):
            add_candidate({"name": name, "description": desc})

        for item in self._unique_fallback_pool(destination):
            add_candidate(item)

        # De-duplicate the candidate pool itself.
        unique_candidates = []
        seen = set()
        for item in candidates:
            activity_key = self._activity_key(item["name"])
            if not activity_key or activity_key in seen:
                continue
            seen.add(activity_key)
            unique_candidates.append(item)

        # Guarantee enough unique slots for even unusually long trips. These are
        # explicitly labelled flexible experiences, not fake named attractions.
        required = days * 3
        flexible_index = 1
        while len(unique_candidates) < required:
            item = {
                "name": f"{destination} flexible experience {flexible_index}",
                "description": f"Keep this time flexible for a local experience in {destination} based on current conditions.",
            }
            activity_key = self._activity_key(item["name"])
            if activity_key not in seen:
                seen.add(activity_key)
                unique_candidates.append(item)
            flexible_index += 1

        # Build a fast lookup of the model's per-slot suggestions so we preserve
        # sensible morning/afternoon/evening placement when those suggestions are
        # unique. Duplicates fall through to the global candidate pool.
        used = set()
        pool_index = 0
        repaired = []

        def take_candidate(preferred_items):
            nonlocal pool_index
            for item in preferred_items:
                key2 = self._activity_key(item.get("name"))
                if key2 and key2 not in used:
                    used.add(key2)
                    return {"name": item["name"], "description": item.get("description", "Recommended experience")}
            while pool_index < len(unique_candidates):
                item = unique_candidates[pool_index]
                pool_index += 1
                key2 = self._activity_key(item["name"])
                if key2 and key2 not in used:
                    used.add(key2)
                    return dict(item)
            return {
                "name": f"{destination} flexible experience {len(used) + 1}",
                "description": f"Keep this time flexible for a local experience in {destination} based on current conditions.",
            }

        for index in range(days):
            source = source_days[index] if index < len(source_days) and isinstance(source_days[index], dict) else {}
            if index == 0:
                default_title = "Arrival & First Exploration"
                default_theme = "Settle in and discover the destination"
            elif index == days - 1:
                default_title = "Final Exploration & Departure"
                default_theme = "Relax, explore and wrap up"
            else:
                default_title = f"{destination} Highlights"
                default_theme = "Signature sights & local experiences"

            row = {
                "day": index + 1,
                "title": str(source.get("title") or default_title),
                "theme": str(source.get("theme") or default_theme),
                "morning": [],
                "afternoon": [],
                "evening": [],
                "food": str(source.get("food") or f"Try a local specialty in {destination}"),
                "estimated_day_cost": str(source.get("estimated_day_cost") or "Check current price"),
                "travel_note": str(source.get("travel_note") or "Confirm opening hours, local travel time and weather before visiting."),
            }

            # Collect any model suggestions for this day, but re-assign the final
            # three activities by semantic time-of-day. This prevents a model or
            # fallback from putting "sunset" in the morning or "morning" at night.
            preferred_all = []
            for source_slot in ("morning", "afternoon", "evening"):
                for item in source.get(source_slot, []) or []:
                    if isinstance(item, dict):
                        name = str(item.get("name") or item.get("title") or item.get("activity") or "").strip()
                        if name:
                            destination_key = re.sub(r"[^a-z0-9]+", " ", str(destination).lower()).strip()
                            if self.DESTINATION_FALLBACKS.get(destination_key) and self._is_generic_itinerary_name(name):
                                continue
                            preferred_all.append({
                                "name": name,
                                "description": str(item.get("description") or item.get("category") or "Recommended experience"),
                            })
            selected = []
            while len(selected) < 3:
                candidate = take_candidate(preferred_all if preferred_all else [])
                if candidate:
                    selected.append(candidate)
                    preferred_all = [x for x in preferred_all if self._activity_key(x.get("name")) != self._activity_key(candidate.get("name"))]
                else:
                    break
            # If model suggestions were exhausted, take fresh candidates from the
            # global pool until all three slots are filled.
            while len(selected) < 3:
                candidate = take_candidate([])
                selected.append(candidate)
            assigned = self._assign_time_slots(selected)
            row["morning"] = [assigned["morning"]]
            row["afternoon"] = [assigned["afternoon"]]
            row["evening"] = [assigned["evening"]]

            repaired.append(row)

        return repaired

    @staticmethod
    def _is_valid_itinerary(days_data, days):
        if not isinstance(days_data, list) or len(days_data) != int(days):
            return False
        names = []
        for index, day in enumerate(days_data, start=1):
            if not isinstance(day, dict) or int(day.get("day") or 0) != index:
                return False
            for slot in ("morning", "afternoon", "evening"):
                items = day.get(slot)
                if not isinstance(items, list) or len(items) != 1:
                    return False
                item = items[0]
                if not isinstance(item, dict) or not str(item.get("name") or "").strip():
                    return False
                names.append(TravelAgent._activity_key(item["name"]))
        return len(names) == len(set(names))

    @staticmethod
    def _has_sufficient_unique_itinerary(days_data):
        names = []
        for day in days_data or []:
            for slot in ("morning", "afternoon", "evening"):
                for item in day.get(slot, []):
                    if isinstance(item, dict) and item.get("name"):
                        names.append(re.sub(r"[^a-z0-9]+", " ", str(item["name"]).lower()).strip())
        return bool(names) and len(names) == len(set(names))

    # Deterministic safety-net knowledge for common travel destinations. This is
    # deliberately used only when live attraction data and Gemini are unavailable.
    DESTINATION_FALLBACKS = {
        "kashmir": [
            ("Dal Lake & Shikara Ride", "Lake experience and Srinagar's waterfront."),
            ("Mughal Gardens", "Visit Nishat or Shalimar Gardens for landscaped views."),
            ("Srinagar Old City", "Explore local markets, crafts and historic neighbourhoods."),
            ("Gulmarg", "Mountain day trip with scenic views and optional cable-car activities."),
            ("Pahalgam", "Valley scenery, riverside walks and a relaxed mountain day."),
            ("Hazratbal Shrine", "Visit a major Srinagar landmark and the nearby lakefront."),
            ("Pari Mahal", "Hilltop viewpoint overlooking Srinagar and Dal Lake."),
            ("Lal Chowk", "Central market area for local shopping and city atmosphere."),
        ],
        "goa": [
            ("Baga Beach", "Relax by the beach and explore the surrounding shoreline."),
            ("Fort Aguada", "Explore the historic fort and coastal viewpoints."),
            ("Calangute Beach", "Spend time along one of North Goa's popular beaches."),
            ("Anjuna", "Explore the coastal area and local market scene."),
            ("Panaji & Fontainhas", "Walk through Panaji's colourful Latin Quarter."),
            ("Basilica of Bom Jesus", "Visit the historic Old Goa church complex."),
        ],
        "manali": [
            ("Old Manali", "Walk through the village lanes, cafes and local shops."),
            ("Hadimba Temple", "Visit the cedar-forest temple and surrounding area."),
            ("Solang Valley", "Enjoy mountain scenery and seasonal adventure activities."),
            ("Vashisht", "Explore the village, temple area and hot-spring surroundings."),
            ("Mall Road", "Evening stroll for food and local shopping."),
            ("Sissu", "Take a scenic mountain excursion through the valley."),
        ],
        "jaipur": [
            ("Amber Fort", "Explore the hilltop fort and its courtyards."),
            ("City Palace", "Visit Jaipur's historic royal complex."),
            ("Hawa Mahal", "See the iconic facade and explore the old-city lanes."),
            ("Jantar Mantar", "Explore the historic astronomical instruments."),
            ("Johari Bazaar", "Browse traditional jewellery, textiles and local crafts."),
            ("Nahargarh Fort", "Enjoy elevated views over Jaipur around sunset."),
        ],
        "mumbai": [
            ("Gateway of India", "Start with the waterfront landmark and Colaba area."),
            ("Colaba Causeway", "Explore local shopping and street-side browsing."),
            ("Marine Drive", "Take an evening walk along the sea-facing promenade."),
            ("Chhatrapati Shivaji Maharaj Terminus", "See the historic railway architecture."),
            ("Elephanta Caves", "Take a ferry excursion to the historic cave complex."),
            ("Bandra Bandstand", "Relax by the coast and explore the nearby neighbourhood."),
        ],
        "delhi": [
            ("India Gate", "Visit the landmark and surrounding central Delhi area."),
            ("Humayun's Tomb", "Explore the Mughal-era garden tomb complex."),
            ("Qutub Minar", "Visit the historic monument complex."),
            ("Red Fort", "Explore the historic fort and Old Delhi surroundings."),
            ("Chandni Chowk", "Explore Old Delhi food and market lanes."),
            ("Lotus Temple", "Visit the distinctive modern temple and gardens."),
        ],
        "bengaluru": [
            ("Bengaluru Palace", "Explore the historic palace and grounds."),
            ("Lalbagh Botanical Garden", "Walk through the botanical gardens."),
            ("Cubbon Park", "Enjoy a relaxed city-centre park walk."),
            ("Vidhana Soudha", "See the landmark government building from outside."),
            ("Church Street", "Explore cafes, bookstores and evening city life."),
        ],
        "kochi": [
            ("Fort Kochi", "Walk through the historic waterfront neighbourhood."),
            ("Chinese Fishing Nets", "See the iconic waterfront fishing structures."),
            ("Mattancherry Palace", "Explore the historic palace and nearby heritage area."),
            ("Jew Town", "Browse heritage streets and local shops."),
            ("Marine Drive", "Enjoy a relaxed waterfront evening."),
        ],
        "riyadh": [
            ("Diriyah", "Explore the historic At-Turaif area and heritage district."),
            ("Kingdom Centre", "See Riyadh from the Kingdom Centre Sky Bridge area, subject to opening hours."),
            ("Al Masmak Palace", "Visit the historic fortress and learn about Riyadh's heritage."),
            ("National Museum of Saudi Arabia", "Explore Saudi history, culture and archaeology."),
            ("Boulevard City", "Explore a major entertainment and dining district; check current hours."),
            ("Riyadh local market", "Browse a suitable local market after checking opening hours."),
            ("Edge of the World", "Consider a guided desert escarpment excursion with a licensed operator and current safety conditions."),
            ("Riyadh Park", "Use the mall and leisure area for relaxed shopping and dining time."),
        ],
        "jeddah": [
            ("Al-Balad", "Explore Jeddah's historic old town and traditional architecture."),
            ("Jeddah Corniche", "Walk along the Red Sea waterfront and public spaces."),
            ("King Fahd Fountain viewpoint", "See the famous waterfront landmark from suitable public viewpoints."),
            ("Red Sea waterfront", "Enjoy a relaxed coastal experience with current conditions checked."),
            ("Jeddah Art Promenade", "Explore public art, cafes and waterfront spaces where available."),
            ("Jeddah local market", "Browse a local shopping area and traditional goods."),
        ],
        "alula": [
            ("Hegra", "Explore the UNESCO-listed Nabataean archaeological area with authorised access."),
            ("AlUla Old Town", "Walk through the historic old town and local cultural spaces."),
            ("Elephant Rock", "Visit the natural rock landmark around sunset when conditions permit."),
            ("AlUla Oasis", "Explore the oasis landscape and heritage environment."),
            ("Maraya", "See the mirrored cultural venue and surrounding desert landscape, subject to access."),
            ("AlUla desert landscape", "Choose a guided desert experience with current weather and safety conditions checked."),
        ],
        "kerala": [
            ("Fort Kochi", "Explore the historic waterfront, heritage streets and Chinese fishing nets."),
            ("Alappuzha Backwaters", "Enjoy Kerala's backwater scenery and a relaxed waterfront experience."),
            ("Munnar Tea Gardens", "Take in tea-covered hills and scenic viewpoints around Munnar."),
            ("Mattancherry Palace", "Explore Kerala's heritage and historic neighbourhoods."),
            ("Varkala Cliff", "Enjoy the coastal cliff views and sunset atmosphere."),
            ("Kerala local cuisine", "Try a Kerala-style meal and local snacks."),
        ],
        "bali": [
            ("Ubud", "Explore rice terraces, art spaces and the cultural heart of Bali."),
            ("Tegallalang Rice Terraces", "Walk through the famous terraced landscape."),
            ("Uluwatu Temple", "Visit the cliffside temple and coastal viewpoints."),
            ("Seminyak", "Explore the beachside neighbourhood, cafes and evening atmosphere."),
            ("Nusa Dua", "Enjoy a relaxed beach and coastal day."),
            ("Mount Batur", "Consider a sunrise mountain experience if conditions permit."),
        ],
        "tokyo": [
            ("Asakusa & Senso-ji", "Explore Tokyo's historic temple district and surrounding streets."),
            ("Shibuya Crossing", "Experience one of Tokyo's busiest urban landmarks."),
            ("Meiji Shrine", "Walk through the forested shrine grounds near Harajuku."),
            ("Akihabara", "Explore anime, gaming and electronics culture."),
            ("Shinjuku", "Explore the city's major entertainment and shopping district."),
            ("Tsukiji Outer Market", "Browse food stalls and local culinary experiences."),
        ],
        "paris": [
            ("Eiffel Tower", "Visit the iconic landmark and surrounding Seine area."),
            ("Louvre Museum", "Explore one of the world's major art museums."),
            ("Montmartre", "Walk the artistic neighbourhood and Sacré-Cœur area."),
            ("Seine River", "Enjoy a scenic riverside walk or cruise."),
            ("Le Marais", "Explore historic streets, cafes and local shops."),
            ("Latin Quarter", "Wander through historic streets and food spots."),
            ("Arc de Triomphe", "See the monumental arch and the Champs-Élysées area."),
            ("Musée d'Orsay", "Explore major Impressionist and Post-Impressionist works."),
            ("Sainte-Chapelle", "Visit the Gothic chapel known for its stained-glass windows."),
            ("Sacré-Cœur Basilica", "Visit the hilltop basilica and enjoy views across Paris."),
            ("Champs-Élysées", "Walk along the famous avenue toward the Arc de Triomphe."),
            ("Palace of Versailles", "Take a day-trip option to the historic royal palace and gardens."),
        ],
        "dubai": [
            ("Burj Khalifa", "Visit Dubai's landmark tower and downtown area."),
            ("Dubai Marina", "Explore the waterfront promenade and skyline."),
            ("Al Fahidi Historical District", "See an older side of Dubai through heritage lanes."),
            ("Jumeirah Beach", "Relax by the coast and enjoy the city skyline."),
            ("Dubai Mall", "Explore one of the city's major shopping and entertainment areas."),
            ("Desert experience", "Consider a desert activity with current weather and operator conditions checked."),
        ],
        "new york": [
            ("Central Park", "Explore the city's major urban park."),
            ("Times Square", "Experience the bright central entertainment district."),
            ("Statue of Liberty", "Visit the harbor landmark if tickets and schedules allow."),
            ("Brooklyn Bridge", "Walk across the bridge for skyline views."),
            ("The Metropolitan Museum of Art", "Explore a major art collection."),
            ("SoHo", "Walk through the historic shopping and gallery district."),
        ],
        "cape town": [
            ("Table Mountain", "Take in the city's signature mountain and skyline views."),
            ("V&A Waterfront", "Explore the waterfront, food and harbour area."),
            ("Bo-Kaap", "Walk through the colourful historic neighbourhood."),
            ("Camps Bay", "Enjoy the coastal scenery and beach atmosphere."),
            ("Kirstenbosch", "Explore the botanical garden at the foot of Table Mountain."),
            ("Cape Point", "Take a scenic excursion along the peninsula."),
        ],
        "serengeti": [
            ("Serengeti National Park", "Plan a wildlife-focused safari with an authorised operator."),
            ("Seronera", "Explore the central Serengeti area known for wildlife viewing."),
            ("Serengeti plains", "Spend time observing the landscape and wildlife with a guide."),
            ("Sunset safari", "Choose a permitted evening safari experience where available."),
            ("Local cultural experience", "Include a respectful, locally guided cultural visit when appropriate."),
            ("Wildlife photography", "Use a guided viewing period for landscape and wildlife photography."),
        ],
        "victoria falls": [
            ("Victoria Falls", "Visit the waterfall viewpoints and follow current park guidance."),
            ("Zambezi River", "Explore the river area with an authorised activity provider."),
            ("Victoria Falls town", "Walk through the local town and nearby craft areas."),
            ("Zambezi sunset", "Consider a permitted sunset river experience."),
            ("Rainforest viewpoints", "Explore the viewpoints around the falls in suitable weather."),
            ("Local market", "Browse local crafts and food respectfully."),
        ],
    }

    @staticmethod
    def _dynamic_wikipedia_attractions(destination, location=None, limit=18):
        """Find nearby named places without requiring a destination-specific catalog or API key.

        Wikipedia's public geosearch is used only as a safety-net source. It supplies
        names of nearby pages/landmarks; it is not treated as booking or price data.
        If unavailable, the itinerary still works using a generic destination-safe plan.
        """
        location = location or {}
        lat = location.get("latitude")
        lon = location.get("longitude")
        if lat is None or lon is None:
            return []
        try:
            params = urlencode({
                "action": "query",
                "list": "geosearch",
                "gscoord": f"{float(lat)}|{float(lon)}",
                "gsradius": 10000,
                "gslimit": max(5, min(30, int(limit))),
                "gsnamespace": 0,
                "format": "json",
                "origin": "*",
            })
            request = Request(
                f"https://en.wikipedia.org/w/api.php?{params}",
                headers={"User-Agent": "WanderAI/1.0 travel-planner"},
            )
            with urlopen(request, timeout=5) as response:
                import json as _json
                payload = _json.loads(response.read().decode("utf-8"))
            rows = (payload.get("query") or {}).get("geosearch") or []
            result = []
            seen = set()
            for row in rows:
                name = str(row.get("title") or "").strip()
                if not name:
                    continue
                key = re.sub(r"[^a-z0-9]+", " ", name.lower()).strip()
                if key in seen:
                    continue
                seen.add(key)
                distance = row.get("dist")
                distance_text = f" About {round(float(distance) / 1000, 1)} km away." if distance is not None else ""
                result.append({
                    "name": name,
                    "description": f"Nearby point of interest for {destination}.{distance_text}"
                })
            return result
        except Exception:
            return []

    @staticmethod
    def _has_specific_itinerary(days_data, destination):
        """Reject an LLM response if it is structurally valid but still generic."""
        if not days_data:
            return False
        generic_phrases = {
            f"explore {destination}".lower(),
            f"{destination} local exploration".lower(),
            f"{destination} cultural or scenic spot".lower(),
            "local food experience",
            "local market or neighbourhood walk",
            "sunset / evening viewpoint",
        }
        names = []
        for day in days_data:
            for slot in ("morning", "afternoon", "evening"):
                for item in day.get(slot, []):
                    name = str(item.get("name", "")).strip().lower()
                    if name and name not in generic_phrases:
                        names.append(name)
        return len(set(names)) >= min(3, len(days_data) + 1)

    def _fallback_itinerary(self, destination, days, activities=None, location=None):
        options = []
        if isinstance(activities, dict):
            options = activities.get("options") or []
        elif isinstance(activities, list):
            options = activities

        clean = []
        for item in options:
            if not isinstance(item, dict):
                continue
            name = item.get("name") or item.get("title") or item.get("activity")
            if name:
                clean.append({
                    "name": str(name),
                    "description": str(item.get("description") or item.get("category") or "Current attraction result."),
                })

        key = re.sub(r"[^a-z0-9]+", " ", str(destination).lower()).strip()
        seed = self.DESTINATION_FALLBACKS.get(key, [])
        if seed:
            # Local tools may return generic placeholders such as
            # "Paris city highlights" when no live POI API is connected.
            # Never let those placeholders outrank the destination-specific
            # attraction catalog. Keep only specific tool results here.
            generic_markers = (
                "city highlights", "local market", "scenic area",
                "city/area exploration", "local exploration",
                "flexible experience", "cultural or scenic area",
                "local food experience", "neighbourhood walk",
                "neighborhood walk", "cafe leisure time",
                "café leisure time", "evening viewpoint",
                "market or neighbourhood", "market or neighborhood",
            )
            clean = [
                item for item in clean
                if not self._is_generic_itinerary_name(item.get("name", ""))
            ]
            # Destination-specific seed attractions are the deterministic
            # safety net and are intentionally placed before generic extras.
            clean = [{"name": name, "description": desc} for name, desc in seed] + clean

        # Do not make itinerary rendering depend on an unrelated external
        # website. If the attraction API is unavailable and no local seed exists,
        # use the safe generic destination plan below. This keeps the app fast and
        # deterministic even when internet access is slow or unavailable.
        if not clean:
            clean = [
                {"name": f"{destination} city/area exploration", "description": f"Explore a well-known area around {destination} and your accommodation."},
                {"name": f"{destination} local food experience", "description": f"Try a locally associated dish or neighbourhood dining area in {destination}."},
                {"name": f"{destination} cultural or scenic area", "description": f"Choose a notable local sight after checking current opening hours and access."},
                {"name": f"{destination} market or neighbourhood", "description": f"Spend relaxed time exploring a local market or walkable neighbourhood."},
                {"name": f"{destination} evening viewpoint", "description": f"Choose a safe, accessible evening spot based on local conditions."},
            ]

        # Build one sufficiently large, unique activity pool. The previous
        # implementation used modulo indexing, which caused the same three
        # attractions to repeat once a trip became longer than the activity
        # list. Never cycle back to the first attraction.
        pool = []
        seen = set()
        for item in clean + self._unique_fallback_pool(destination):
            activity_key = self._activity_key(item.get("name"))
            if not activity_key or activity_key in seen:
                continue
            seen.add(activity_key)
            pool.append(item)

        required_slots = days * 3
        # For unusually long trips, create additional unique flexible slots
        # rather than repeating a named attraction.
        extra_index = 1
        while len(pool) < required_slots:
            candidate = {
                "name": f"{destination} flexible experience {extra_index}",
                "description": f"Keep this time flexible for a local experience in {destination} based on current conditions.",
            }
            candidate_key = self._activity_key(candidate["name"])
            if candidate_key not in seen:
                seen.add(candidate_key)
                pool.append(candidate)
            extra_index += 1

        result = []
        cursor = 0
        for index in range(days):
            if index == 0:
                title = "Arrival & First Exploration"
                theme = "Settle in and discover the destination"
            elif index == days - 1:
                title = "Final Exploration & Departure"
                theme = "Relax, explore and wrap up"
            else:
                title = f"{destination} Highlights"
                theme = "Signature sights & local experiences"

            picks = pool[cursor:cursor + 3]
            cursor += 3
            result.append({
                "day": index + 1,
                "title": title,
                "theme": theme,
                "morning": [picks[0]],
                "afternoon": [picks[1]],
                "evening": [picks[2]],
                "food": f"Try a local specialty in {destination}",
                "estimated_day_cost": "Check current price",
                "travel_note": "Confirm opening hours, local travel time and weather before visiting.",
            })

        repaired = self._repair_itinerary(result, days, destination, clean)
        if not self._is_valid_itinerary(repaired, days):
            raise RuntimeError("Internal itinerary validation failed")
        return repaired


    # ------------------------------------------------------------------
    # ADAPTIVE RE-PLANNING
    # ------------------------------------------------------------------
    def _classify_replan_request(self, instruction):
        """Convert a natural-language follow-up into a small, deterministic set
        of changes. This is intentionally transparent and does not expose model
        chain-of-thought.
        """
        s = re.sub(r"\s+", " ", (instruction or "").strip().lower())
        changes = {
            "hotel": None,
            "activities": None,
            "budget": None,
            "pace": None,
            "add_days": 0,
            "remove_days": 0,
            "preferences": [],
        }

        if not s:
            return changes

        if re.search(r"\b(cheaper|lower|reduce|less expensive|save money|cut cost|economical)\b", s):
            changes["hotel"] = "cheaper"
            changes["budget"] = "reduce"

        if re.search(r"\b(better|nicer|upgrade|premium|higher rated|more comfortable)\b", s):
            changes["hotel"] = "better"

        if re.search(r"\b(more\s+beach|beaches|beach)\b", s):
            changes["activities"] = "beach"
            changes["preferences"].append("beaches")

        if re.search(r"\b(more\s+food|food|restaurants|cuisine|culinary)\b", s):
            changes["activities"] = "food"
            changes["preferences"].append("food")

        if re.search(r"\b(nightlife|clubs|bars|evening\s+life)\b", s):
            changes["activities"] = "nightlife"
            changes["preferences"].append("nightlife")

        if re.search(r"\b(nature|scenic|mountains|wildlife|outdoors)\b", s):
            changes["activities"] = "nature"
            changes["preferences"].append("nature")

        if re.search(r"\b(culture|cultural|heritage|museum|museums)\b", s):
            changes["activities"] = "culture"
            changes["preferences"].append("culture")

        if re.search(r"\b(photo|photos|photography|photogenic|pictures|picture spots|instagram)\b", s):
            changes["activities"] = "photography"
            changes["preferences"].append("photography")

        if re.search(r"\b(shopping|shop|markets|market)\b", s):
            changes["activities"] = "shopping"
            changes["preferences"].append("shopping")

        if re.search(r"\b(family|kids|children|child friendly)\b", s):
            changes["activities"] = "family"
            changes["preferences"].append("family")

        if re.search(r"\b(romantic|couple|honeymoon|date)\b", s):
            changes["activities"] = "romantic"
            changes["preferences"].append("romantic")

        if re.search(r"\b(more\s+relax|relaxed|relaxing|less\s+hectic|slow\s+down|not\s+too\s+hectic)\b", s):
            changes["pace"] = "relaxed"

        if re.search(r"\b(more\s+adventure|adventure|adventurous|thrill|active)\b", s):
            changes["pace"] = "active"

        m = re.search(r"\b(?:add|extend|increase)\s+(?:the\s+trip\s+by\s+)?(\d+)\s+(?:day|days|night|nights)\b", s)
        if m:
            amount = max(1, int(m.group(1)))
            changes["add_days"] = amount

        m = re.search(r"\b(?:remove|shorten|reduce)\s+(?:the\s+trip\s+by\s+)?(\d+)\s+(?:day|days|night|nights)\b", s)
        if m:
            changes["remove_days"] = max(1, int(m.group(1)))

        # "keep budget same" means do not alter the budget constraint.
        if re.search(r"\b(keep|same|unchanged).{0,20}\bbudget\b", s):
            changes["budget"] = "keep"

        return changes

    def _replan_unique_pool(self, destination, current_itinerary, activity_result):
        pool = []
        seen = set()

        def add(item):
            if not isinstance(item, dict):
                return
            name = str(item.get("name") or item.get("title") or "").strip()
            if not name:
                return
            key = self._activity_key(name)
            if not key or key in seen:
                return
            seen.add(key)
            pool.append({
                "name": name,
                "description": str(item.get("description") or item.get("category") or "Recommended experience")
            })

        for day in current_itinerary or []:
            for slot in ("morning", "afternoon", "evening"):
                for item in day.get(slot, []) or []:
                    add(item)

        options = activity_result.get("options", []) if isinstance(activity_result, dict) else []
        for item in options:
            add(item)

        key = re.sub(r"[^a-z0-9]+", " ", str(destination).lower()).strip()
        for name, desc in self.DESTINATION_FALLBACKS.get(key, []):
            add({"name": name, "description": desc})

        for item in self._unique_fallback_pool(destination):
            add(item)

        return pool

    @staticmethod
    def _activity_matches_preference(name, preference):
        s = str(name or "").lower()
        groups = {
            "beach": ("beach", "coast", "shore", "island", "waterfront", "sea", "cliff"),
            "food": ("food", "market", "cuisine", "restaurant", "street food", "cafe", "culinary"),
            "nightlife": ("night", "club", "bar", "evening", "nightlife"),
            "nature": ("nature", "garden", "park", "mountain", "lake", "river", "wildlife", "forest", "waterfall", "valley", "tea"),
            "culture": ("museum", "palace", "fort", "temple", "heritage", "old city", "historic", "market"),
            "photography": ("photo", "photography", "view", "viewpoint", "scenic", "sunset", "skyline", "landscape", "waterfront", "garden"),
            "shopping": ("market", "shopping", "mall", "bazaar", "souq", "street"),
            "family": ("park", "museum", "beach", "garden", "zoo", "aquarium", "family"),
            "romantic": ("sunset", "beach", "seine", "waterfront", "garden", "view", "cafe", "cruise"),
        }
        return any(token in s for token in groups.get(preference, ()))

    def _rebuild_itinerary_for_replan(self, current, destination, days, activity_result, changes):
        """Rebuild the itinerary with hard uniqueness and simple preference scoring."""
        days = max(1, min(30, int(days)))
        pool = self._replan_unique_pool(destination, current, activity_result)

        # Score candidates according to the follow-up while keeping existing
        # destination-specific candidates available.
        preferred = [p for p in changes.get("preferences", []) if p]
        if preferred:
            pool.sort(
                key=lambda item: sum(
                    self._activity_matches_preference(item["name"], pref)
                    for pref in preferred
                ),
                reverse=True,
            )

        if changes.get("pace") == "relaxed":
            # Move flexible/low-intensity experiences ahead of strenuous ones.
            relaxed_tokens = ("walk", "garden", "market", "cafe", "beach", "lake", "waterfront", "food", "museum")
            pool.sort(
                key=lambda item: (
                    -int(any(t in item["name"].lower() for t in relaxed_tokens)),
                )
            )

        if changes.get("pace") == "active":
            active_tokens = ("adventure", "mountain", "waterfall", "safari", "hike", "river", "wildlife")
            pool.sort(
                key=lambda item: (
                    -int(any(t in item["name"].lower() for t in active_tokens)),
                )
            )

        # Guarantee enough unique slots.
        used = {self._activity_key(item["name"]) for item in pool}
        required = days * 3
        index = 1
        while len(pool) < required:
            name = f"{destination} flexible experience {index}"
            key = self._activity_key(name)
            if key not in used:
                used.add(key)
                pool.append({
                    "name": name,
                    "description": f"Flexible time for a local experience in {destination}."
                })
            index += 1

        rebuilt = []
        cursor = 0
        for day_index in range(days):
            if day_index == 0:
                title = "Arrival & First Exploration"
                theme = "Settle in and discover the destination"
            elif day_index == days - 1:
                title = "Final Exploration & Departure"
                theme = "Relax, explore and wrap up"
            else:
                title = f"{destination} Highlights"
                theme = "Signature sights & local experiences"

            row = {
                "day": day_index + 1,
                "title": title,
                "theme": theme,
                "morning": [dict(pool[cursor])],
                "afternoon": [dict(pool[cursor + 1])],
                "evening": [dict(pool[cursor + 2])],
                "food": f"Try a local specialty in {destination}",
                "estimated_day_cost": "Check current price",
                "travel_note": "Confirm opening hours, local travel time and weather before visiting.",
            }
            cursor += 3
            rebuilt.append(row)

        return rebuilt

    def replan(self, previous_result, instruction):
        """Adapt an existing successful trip without losing its core constraints."""
        if not isinstance(previous_result, dict) or not previous_result.get("success"):
            return {
                "success": False,
                "error": "Create a trip first, then tell WanderAI what you want to change."
            }

        instruction = re.sub(r"\s+", " ", (instruction or "").strip())
        if not instruction:
            return {
                "success": False,
                "error": "Tell me what you want to change, for example: 'make the hotel cheaper' or 'add more beaches'."
            }

        changes = self._classify_replan_request(instruction)
        if not any([
            changes["hotel"], changes["activities"], changes["budget"],
            changes["pace"], changes["add_days"], changes["remove_days"],
            changes["preferences"]
        ]):
            return {
                "success": False,
                "error": "I couldn't identify a trip change. Try 'cheaper hotel', 'better hotel', 'more beaches', 'more relaxing', or 'add 1 day'."
            }

        destination = previous_result["destination"]
        location = previous_result.get("location") or {}
        planning_destination = previous_result.get("planning_destination") or location.get("planning_city") or location.get("representative_place") or destination
        old_nights = int(previous_result.get("nights") or 3)
        nights = old_nights + changes["add_days"] - changes["remove_days"]
        nights = max(1, min(30, nights))

        # Keep the original budget limit unless the user explicitly provides a new one.
        budget_limit = previous_result.get("budget_limit")
        explicit_budget = self.extract_budget(instruction)
        if explicit_budget is not None:
            budget_limit = explicit_budget

        results = previous_result.get("results") or {}

        # Re-query tools so this is a genuine new planning action rather than
        # merely changing text on the screen.
        flight = self._safe_tool_call(self.tools["flight"], planning_destination, location)
        hotel = self._safe_tool_call(self.tools["hotel"], planning_destination, nights=nights, adults=1, location=location)
        weather = self._safe_tool_call(self.tools["weather"], planning_destination, location, forecast_days=min(16, nights + 2))
        activities = self._safe_tool_call(self.tools["activity"], planning_destination, location)
        food = self._safe_tool_call(self.tools["food"], planning_destination, location)

        if changes["hotel"] == "cheaper" and isinstance(hotel, dict):
            options = list(hotel.get("options") or [])
            options.sort(key=lambda x: float(x.get("price") if x.get("price") not in (None, "") else x.get("price_per_night") if x.get("price_per_night") not in (None, "") else float("inf")))
            hotel["options"] = options
            hotel["selection_reason"] = "Lower-cost accommodation options are shown first."

        elif changes["hotel"] == "better" and isinstance(hotel, dict):
            options = list(hotel.get("options") or [])
            def quality_key(x):
                try:
                    rating = float(x.get("rating") or 0)
                except (TypeError, ValueError):
                    rating = 0
                try:
                    price = float(x.get("price") if x.get("price") not in (None, "") else x.get("price_per_night") if x.get("price_per_night") not in (None, "") else float("inf"))
                except (TypeError, ValueError):
                    price = float("inf")
                return (-rating, price)
            options.sort(key=quality_key)
            hotel["options"] = options
            hotel["selection_reason"] = "Higher-rated accommodation options are shown first where ratings are available."

        itinerary = self._rebuild_itinerary_for_replan(
            results.get("itinerary") or [],
            planning_destination,
            nights + 1,
            activities,
            changes,
        )

        budget = budget_tool(
            planning_destination,
            nights=nights,
            flight_result=flight,
            hotel_result=hotel,
            activity_result=activities,
        )

        # If the user asked to reduce cost, use the cheapest hotel as the active
        # reference and expose the recalculated budget transparently.
        if changes["budget"] == "reduce" and isinstance(hotel, dict):
            options = hotel.get("options") or []
            if options:
                hotel["options"] = sorted(
                    options,
                    key=lambda x: float(x.get("price") if x.get("price") not in (None, "") else x.get("price_per_night") if x.get("price_per_night") not in (None, "") else float("inf"))
                )
                budget = budget_tool(
                    planning_destination,
                    nights=nights,
                    flight_result=flight,
                    hotel_result=hotel,
                    activity_result=activities,
                )

        live_sources = []
        for key, item in (
            ("flight", flight), ("hotel", hotel),
            ("weather", weather), ("activities", activities)
        ):
            if isinstance(item, dict) and item.get("live") and item.get("available"):
                live_sources.append(key)

        new_results = {
            "flight": flight,
            "hotel": hotel,
            "weather": weather,
            "activities": activities,
            "food": food,
            "budget": budget,
            "itinerary": itinerary,
        }

        return {
            **previous_result,
            "success": True,
            "request": f"{previous_result.get('request', '')} | Follow-up: {instruction}",
            "nights": nights,
            "planning_destination": planning_destination,
            "budget_limit": budget_limit,
            "results": new_results,
            "live_sources": live_sources,
            "data_mode": "live" if live_sources else "partial",
            "agent_steps": [
                "Follow-up request understood",
                "Original trip constraints preserved",
                "Travel options re-checked",
                "Requested preferences applied",
                "Budget recalculated",
                "Itinerary rebuilt without repeated activities",
                "Updated plan ready",
            ],
            "replan_instruction": instruction,
            "replan_changes": changes,
        }

    @staticmethod
    def _safe_tool_call(tool, *args, **kwargs):
        try:
            value = tool(*args, **kwargs)
            return value if isinstance(value, dict) else {"available": False, "live": False, "message": "Travel source returned an unexpected result.", "options": []}
        except Exception as exc:
            return {
                "available": False,
                "live": False,
                "message": f"This travel source could not be loaded right now: {exc}",
                "options": [],
            }

    def run(self, request):
        info = self.understand_request(request)
        destination_input = info["destination"]
        nights = info["nights"]
        budget_limit = info["budget_limit"]
        selected_tools = info["tools"]

        if not destination_input:
            return {
                "success": False,
                "error": "Please tell me where you want to travel. For example: 'Plan 5 nights in Goa.'",
            }

        location, location_error = geocode_destination(destination_input)
        if not location:
            return {
                "success": False,
                "error": location_error or "We could not locate that destination.",
            }

        # Never allow an empty/unknown country to be presented as a successful
        # destination resolution.
        if not str(location.get("country", "")).strip():
            return {
                "success": False,
                "error": f"We could not confidently determine the country for '{destination_input}'.",
            }

        destination = location["name"]
        planning_destination = location.get("planning_city") or location.get("representative_place") or destination
        results = {}

        if "flight" in selected_tools:
            results["flight"] = self._safe_tool_call(flight_tool, planning_destination, location)
        if "hotel" in selected_tools:
            results["hotel"] = self._safe_tool_call(hotel_tool, planning_destination, nights=nights, adults=1, location=location)
        if "weather" in selected_tools:
            results["weather"] = self._safe_tool_call(weather_tool, planning_destination, location, forecast_days=min(16, nights + 2))
        if "activity" in selected_tools:
            results["activities"] = self._safe_tool_call(activity_tool, planning_destination, location)
        results["food"] = self._safe_tool_call(food_tool, planning_destination, location)

        # The current request parser does not maintain a separate preferences
        # object yet. Keep this explicit and safe until conversational
        # preference memory is added in the next phase.
        preferences = {"interests": []}

        results["itinerary"] = self.generate_daywise_itinerary(
            destination=planning_destination,
            nights=nights,
            interests=preferences.get("interests"),
            weather=results.get("weather"),
            activities=results.get("activities"),
            request=request,
            location=location,
        )

        results["budget"] = budget_tool(
            planning_destination,
            nights=nights,
            flight_result=results.get("flight"),
            hotel_result=results.get("hotel"),
            activity_result=results.get("activities"),
        )

        live_sources = []
        for key in ("flight", "hotel", "weather", "activities"):
            item = results.get(key, {})
            if item.get("live") and item.get("available"):
                live_sources.append(key)

        return {
            "success": True,
            "request": request,
            "destination": destination,
            "planning_destination": planning_destination,
            "location": location,
            "nights": nights,
            "budget_limit": budget_limit,
            "tools": selected_tools,
            "gemini_success": info["gemini_success"],
            "results": results,
            "live_sources": live_sources,
            "data_mode": "live" if live_sources else "partial",
            "agent_steps": [
                "Request understood",
                "Destination resolved",
                "Live travel tools checked",
                "Travel information collected",
                "Budget inputs prepared",
            ],
        }
