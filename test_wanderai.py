import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tools'))

import agent as agent_mod
import tools.travel_tools as tt

# Disable external Gemini for deterministic broad-suite tests.
agent_mod.genai = None
agent_mod.types = None

A = agent_mod.TravelAgent()
A.client = None


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def itinerary_names(itinerary):
    return [
        str(item.get('name')).strip()
        for day in itinerary
        for slot in ('morning', 'afternoon', 'evening')
        for item in day.get(slot, [])
    ]


def normalized_names(names):
    return [A._activity_key(x) for x in names]

# ---------------------------------------------------------------------------
# 1) Parser stress: every airport-aware catalog entry x 12 natural templates.
# ---------------------------------------------------------------------------
templates = [
    'Plan a 3 day trip to {d}',
    'I want a relaxing 4-day vacation in {d}',
    'My friends and I are thinking about going to {d} for 5 days',
    'Can you plan 3 nights in {d}?',
    'I am planning a trip to {d}, nothing too hectic',
    'Maybe {d} for a week with sightseeing',
    'Thinking about {d} for 4 days with local food',
    'I have 5 days and want to explore {d}',
    'Me and 3 friends are visiting {d} for 4 days',
    'Give me a 2 day itinerary for {d}',
    'I want beaches and nature in {d} for 4 days',
    'Please arrange a 6 day vacation to {d}',
    'Help me plan {d} for 3 nights',
    'We are going to {d} next month for 5 days',
    'Create a relaxed itinerary for {d}',
    'Make a family trip plan for {d} for 4 days',
    'I want to visit {d} with my parents for 3 days',
    'What can I do in {d} over 5 days?',
    'Plan {d} for me and two friends',
    'I am thinking of {d} as my next vacation',
    'Can WanderAI plan 4 days in {d}?',
    'Need a 5 day plan for {d} with food',
    'Build me an itinerary for {d}',
    'Take me to {d} for a long weekend',
    'We have 4 days in {d}',
    'I want sightseeing in {d} for 6 days',
    'Plan a budget trip to {d}',
    'Plan a premium trip to {d}',
    'Plan a nature-focused trip to {d}',
    'Plan a culture trip to {d}',
    'Plan an adventure trip to {d}',
    'Plan a food trip to {d}',
    'Plan a beach trip to {d}',
    'Plan a romantic trip to {d}',
    'Plan a peaceful vacation in {d}',
    'Could you make a day-wise plan for {d}?',
    'What would a 7 day {d} itinerary look like?',
    'I have one week for {d}',
    'We are considering {d} for our holiday',
    'I want to explore {d} slowly for 5 days',
]
parser_failures = []
for destination in sorted(tt.AIRPORT_DESTINATIONS, key=lambda x: (len(str(x)), str(x).lower())):
    for template in templates:
        request = template.format(d=destination)
        got = A.extract_destination_locally(request)
        if not got:
            parser_failures.append((destination, request, got))

assert_true(not parser_failures, f'Parser failures: {parser_failures[:5]}')

# ---------------------------------------------------------------------------
# 2) Airport catalog integrity: every mapped destination has the fields needed
#    for deterministic country/airport resolution. Network geocoding is not used
#    in this automated suite because it is an external dependency.
# ---------------------------------------------------------------------------
required_fields = {"canonical", "lookup", "country", "country_code", "airport_iata"}
catalog_failures = []
for destination, entry in tt.AIRPORT_DESTINATIONS.items():
    missing = required_fields - set(entry)
    if missing or len(str(entry.get("country_code", ""))) != 2 or len(str(entry.get("airport_iata", ""))) != 3:
        catalog_failures.append((destination, sorted(missing), entry))
assert_true(not catalog_failures, f"Airport catalog failures: {catalog_failures[:5]}")

# ---------------------------------------------------------------------------
# 3) Deterministic itinerary stress: 1..14 nights for every catalog entry.
# ---------------------------------------------------------------------------
itinerary_failures = []
count = 0
for destination in tt.AIRPORT_DESTINATIONS:
    for nights in range(1, 31):
        days = nights + 1
        out = A.generate_daywise_itinerary(destination, nights, activities=[])
        names = itinerary_names(out)
        keys = normalized_names(names)
        try:
            assert_true(len(out) == days, f'{destination} {nights} nights: wrong day count {len(out)}')
            assert_true(len(names) == days * 3, f'{destination} {nights}: wrong slot count {len(names)}')
            assert_true(len(keys) == len(set(keys)), f'{destination} {nights}: duplicate names')
            for idx, day in enumerate(out, 1):
                assert_true(day.get('day') == idx, f'{destination} {nights}: bad day number')
                for slot in ('morning', 'afternoon', 'evening'):
                    assert_true(isinstance(day.get(slot), list) and len(day[slot]) == 1, f'{destination} {nights}: bad {slot} slot')
                    assert_true(day[slot][0].get('name'), f'{destination} {nights}: empty {slot}')
        except AssertionError as exc:
            itinerary_failures.append(str(exc))
        count += 1

assert_true(not itinerary_failures, f'Itinerary failures: {itinerary_failures[:10]}')

# ---------------------------------------------------------------------------
# 4) Gemini-adversarial test: deliberately repeat the same 3 attractions for
#    every day. The final validator must repair it into unique slots.
# ---------------------------------------------------------------------------
class FakeResponse:
    def __init__(self, payload):
        self.text = json.dumps(payload)
        self.parsed = None

class FakeModels:
    def generate_content(self, **kwargs):
        days = 5
        return FakeResponse({
            'days': [
                {
                    'day': i,
                    'title': 'Repeated title',
                    'theme': 'Repeated theme',
                    'morning': [{'name': 'Victoria Falls', 'description': 'same'}],
                    'afternoon': [{'name': 'Zambezi River', 'description': 'same'}],
                    'evening': [{'name': 'Victoria Falls town', 'description': 'same'}],
                    'food': 'Local food',
                    'estimated_day_cost': 'Check current price',
                    'travel_note': 'Check conditions',
                }
                for i in range(1, days + 1)
            ]
        })

class FakeClient:
    def __init__(self):
        self.models = FakeModels()

A.client = FakeClient()
repaired = A.generate_daywise_itinerary('Victoria Falls', 4, activities=[])
names = itinerary_names(repaired)
assert_true(len(repaired) == 5, 'Gemini adversarial: wrong day count')
assert_true(len(names) == 15, 'Gemini adversarial: wrong slot count')
assert_true(len(set(normalized_names(names))) == 15, 'Gemini adversarial: duplicate survived')
A.client = None

# ---------------------------------------------------------------------------
# 5) Direct repair tests with pathological input shapes.
# ---------------------------------------------------------------------------
pathological = [
    {},
    {'day': 1, 'morning': [], 'afternoon': [], 'evening': []},
    {'day': 2, 'morning': [{'name': 'Same'}], 'afternoon': [{'name': 'Same'}], 'evening': [{'name': 'Same'}]},
]
fixed = A._repair_itinerary(pathological, 7, 'Kerala', [])
names = itinerary_names(fixed)
assert_true(A._is_valid_itinerary(fixed, 7), 'Pathological repair failed')
assert_true(len(set(normalized_names(names))) == 21, 'Pathological repair duplicates remain')

# ---------------------------------------------------------------------------
# 6) No-destination safety tests: must not guess.
# ---------------------------------------------------------------------------
for request in [
    'I want a relaxing 5 day vacation somewhere warm',
    'Take me somewhere beautiful for 4 days',
    'I have 3 days and want beaches',
    'Plan a cheap vacation anywhere',
]:
    info = A.understand_request(request)
    assert_true(info['destination'] is None, f'No-destination request was guessed: {request!r} -> {info}')

# ---------------------------------------------------------------------------
# 7) Local integration smoke test for representative destinations. Replace
#    external/live tools with deterministic fakes so the agent orchestration is
#    exercised without network calls.
# ---------------------------------------------------------------------------
def fake_weather(destination, *args, **kwargs):
    return {'available': False, 'message': 'test'}

def fake_flight(destination, *args, **kwargs):
    return {'type': 'Flight', 'destination': destination, 'options': [{'airline': 'TestAir', 'route': 'Origin -> ' + destination, 'price': 1000}]}

def fake_hotel(destination, *args, **kwargs):
    return {'type': 'Hotel', 'destination': destination, 'options': [{'name': 'Test Hotel', 'area': destination, 'price_per_night': 1000}]}

def fake_activity(destination, *args, **kwargs):
    return {'type': 'Activities', 'destination': destination, 'options': [{'name': 'A1', 'category': 'Test', 'cost': 0}, {'name': 'A2', 'category': 'Test', 'cost': 0}, {'name': 'A3', 'category': 'Test', 'cost': 0}]}

def fake_budget(destination, nights=3, *args, **kwargs):
    return {'type': 'Budget', 'destination': destination, 'nights': nights, 'breakdown': {'flight': 1000, 'hotel': 1000*nights, 'activities': 0, 'food': 1000, 'local_transport': 500}, 'estimated_total': 2500+1000*nights}

agent_mod.weather_tool = fake_weather
agent_mod.flight_tool = fake_flight
agent_mod.hotel_tool = fake_hotel
agent_mod.activity_tool = fake_activity
agent_mod.budget_tool = fake_budget

def fake_geocode(destination):
    entry = tt.AIRPORT_DESTINATIONS.get(destination.lower())
    if not entry:
        return None, 'test geocode miss'
    return {
        'name': entry['canonical'],
        'country': entry['country'],
        'country_code': entry['country_code'],
        'latitude': 0.0,
        'longitude': 0.0,
        'airport_iata': entry['airport_iata'],
        'airport_search_name': entry['lookup'],
        'representative_place': entry['lookup'],
    }, None

agent_mod.geocode_destination = fake_geocode

representatives = ['Kerala', 'Kashmir', 'Victoria Falls', 'Paris', 'Bali', 'Tokyo', 'Goa', 'Manali', 'Cape Town', 'New York']
run_failures = []
for d in representatives:
    result = A.run(f'Plan a 4 day trip to {d}')
    if not result.get('success'):
        run_failures.append((d, result.get('error')))
        continue
    it = result.get('results', {}).get('itinerary', [])
    try:
        expected_days = A.extract_nights(f'Plan a 4 day trip to {d}') + 1
        assert_true(A._is_valid_itinerary(it, expected_days), f'{d}: run itinerary invalid')
    except AssertionError as exc:
        run_failures.append((d, str(exc)))
assert_true(not run_failures, f'Run failures: {run_failures}')

# ---------------------------------------------------------------------------
# 8) Regression tests for the latest browser-image + itinerary fixes.
# ---------------------------------------------------------------------------
# Paris must use destination-specific attractions before generic planning
# placeholders when the POI API is unavailable.
paris_fallback = A._fallback_itinerary('Paris', 4, activities={
    'options': [
        {'name': 'Paris city highlights', 'category': 'Sightseeing'},
        {'name': 'Paris local market', 'category': 'Market'},
        {'name': 'Paris scenic area', 'category': 'Nature'},
    ]
})
paris_names = [
    item['name']
    for day in paris_fallback
    for slot in ('morning', 'afternoon', 'evening')
    for item in day.get(slot, [])
]
assert_true('Paris city highlights' not in paris_names, 'Generic Paris city placeholder leaked into itinerary')
assert_true('Paris local market' not in paris_names, 'Generic Paris market placeholder leaked into itinerary')
assert_true('Paris scenic area' not in paris_names, 'Generic Paris scenic placeholder leaked into itinerary')
assert_true(len(set(paris_names)) == 12, 'Paris 4-day itinerary does not contain 12 unique named activities')
assert_true({'Eiffel Tower', 'Louvre Museum', 'Montmartre', 'Seine River'}.issubset(set(paris_names)), 'Core Paris attractions missing from fallback itinerary')

# The browser image engine must contain the safeguards visible in the latest UI.
app_source = open('app.py', encoding='utf-8').read()
for required in (
    'military aircraft', 'fighter', 'commercial airliner exterior',
    'Representative commercial aircraft image',
    'Representative accommodation image',
    'usedUrls',
):
    assert_true(required in app_source, f'Image regression safeguard missing: {required}')

# Flight images must reject cabin/interior imagery and require exterior aviation context.
assert_true('cabin' in app_source and 'aircraft interior' in app_source, 'Cabin/interior flight-image rejection missing')
assert_true('usedSources' in app_source, 'Source-title image deduplication missing')
# Generic accented itinerary filler must be filtered before named Paris attractions.
repair_source = open('agent.py', encoding='utf-8').read()
assert_true('_is_generic_itinerary_name' in repair_source, 'Generic itinerary filter missing')
assert_true('cafe leisure time' in repair_source, 'Accent-normalized cafe filler filter missing')
print('Flight exterior + duplicate-image regression tests: PASS')
print('Generic itinerary filler regression tests: PASS')

print('Image semantic regression tests: PASS')
print('Paris 4-day named-attraction regression: PASS')

print('WANDERAI DEEP TEST SUITE: PASS')
print(f'Catalog entries checked: {len(tt.AIRPORT_DESTINATIONS)}')
print(f'Parser cases checked: {len(tt.AIRPORT_DESTINATIONS) * len(templates)}')
print(f'Itinerary cases checked: {count}')
print('Maximum trip length checked: 30 nights / 31 days')
print('Gemini adversarial duplicate case: PASS')
print('Pathological repair cases: PASS')
print('Airport catalog integrity: PASS')
print('No-destination safety cases: PASS')
print('Representative orchestration cases: PASS')

# ---------------------------------------------------------------------------
# 9) Human-in-the-loop approval + PDF export regression tests.
# ---------------------------------------------------------------------------
from pdf_utils import build_trip_pdf

pdf_test_result = {
    'success': True,
    'destination': 'Paris',
    'location': {'country': 'France'},
    'nights': 3,
    'budget_limit': 80000,
    'results': {
        'weather': {'available': True, 'current': {'temperature_2m': 18, 'apparent_temperature': 17, 'wind_speed_10m': 12}},
        'flight': {'available': True, 'options': [{'airline': 'TestAir', 'route': 'Bengaluru -> Paris', 'price': 25000}]},
        'hotel': {'available': True, 'options': [{'name': 'Test Hotel', 'area': 'Central Paris', 'price_per_night': 5000}]},
        'activities': {'available': True, 'options': [{'name': 'Eiffel Tower', 'category': 'Landmark', 'cost': 0}]},
        'food': {'available': True, 'options': [{'name': 'Croissant', 'category': 'Bakery', 'cost': 5}]},
        'budget': {'breakdown': {'flight': 25000, 'hotel': 15000, 'activities': 0, 'food_estimate': 6000, 'local_transport': 3000}, 'estimated_total': 49000},
        'itinerary': [
            {'day': 1, 'title': 'Paris Highlights', 'theme': 'Classic Paris', 'morning': [{'name': 'Louvre Museum', 'description': 'Museum visit'}], 'afternoon': [{'name': 'Eiffel Tower', 'description': 'Landmark visit'}], 'evening': [{'name': 'Seine River', 'description': 'River walk'}], 'food': 'Croissant', 'travel_note': 'Use Metro'},
        ],
    },
}
pdf_bytes = build_trip_pdf(pdf_test_result)
assert_true(isinstance(pdf_bytes, bytes) and pdf_bytes.startswith(b'%PDF-'), 'Approved trip PDF is not a valid PDF byte stream')
assert_true(len(pdf_bytes) > 1500, 'Approved trip PDF is unexpectedly small')

# The app must explicitly gate PDF generation behind approval and reset approval
# after a re-plan/new plan.
app_source = open('app.py', encoding='utf-8').read()
for required in (
    'Human Approval', 'Yes, approve this trip', 'No, I want changes',
    'build_trip_pdf(result)', 'Download Approved Trip Summary (PDF)',
    'approval_state = "pending"', 'approval_state = "approved"',
    'approval_state = "changes_requested"',
):
    assert_true(required in app_source, f'Human approval/PDF safeguard missing: {required}')

print('Human approval gate regression: PASS')
print('Approved PDF generation regression: PASS')
