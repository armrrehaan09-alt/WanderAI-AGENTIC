# ============================================================
# WANDERAI HACKATHON - LOCAL TRAVEL TOOLS
# ============================================================
# This file contains demo/local travel data.
# No paid APIs or real-time booking services are used.
#
# The data is for hackathon demonstration purposes only.
# Prices are approximate demo values, not live prices.
# ============================================================


DESTINATIONS = {

    # --------------------------------------------------------
    # GOA
    # --------------------------------------------------------

    "goa": {
        "state": "Goa",
        "type": "Beach / Nightlife",

        "flights": [
            {
                "airline": "IndiGo",
                "route": "Bengaluru → Goa",
                "price": 3200
            },
            {
                "airline": "Air India Express",
                "route": "Bengaluru → Goa",
                "price": 3500
            }
        ],

        "hotels": [
            {
                "name": "Palm Stay Goa",
                "area": "Baga",
                "price_per_night": 2800
            },
            {
                "name": "Goa Beach Resort",
                "area": "Calangute",
                "price_per_night": 3500
            }
        ],

        "activities": [
            {
                "name": "Baga Beach",
                "category": "Beach",
                "cost": 0
            },
            {
                "name": "Calangute Beach",
                "category": "Beach",
                "cost": 0
            },
            {
                "name": "Fort Aguada",
                "category": "Sightseeing",
                "cost": 100
            },
            {
                "name": "Anjuna Night Market",
                "category": "Nightlife",
                "cost": 500
            }
        ]
    },


    # --------------------------------------------------------
    # MANALI
    # --------------------------------------------------------

    "manali": {
        "state": "Himachal Pradesh",
        "type": "Mountains / Adventure",

        "flights": [
            {
                "airline": "IndiGo",
                "route": "Bengaluru → Delhi",
                "price": 4500
            }
        ],

        "hotels": [
            {
                "name": "Mountain View Stay",
                "area": "Old Manali",
                "price_per_night": 2500
            },
            {
                "name": "Snow Valley Resort",
                "area": "Manali",
                "price_per_night": 3200
            }
        ],

        "activities": [
            {
                "name": "Solang Valley",
                "category": "Adventure",
                "cost": 800
            },
            {
                "name": "Hadimba Temple",
                "category": "Sightseeing",
                "cost": 0
            },
            {
                "name": "Mall Road",
                "category": "Shopping",
                "cost": 0
            },
            {
                "name": "Old Manali",
                "category": "Exploration",
                "cost": 0
            }
        ]
    },


    # --------------------------------------------------------
    # JAIPUR
    # --------------------------------------------------------

    "jaipur": {
        "state": "Rajasthan",
        "type": "Heritage / Culture",

        "flights": [
            {
                "airline": "IndiGo",
                "route": "Bengaluru → Jaipur",
                "price": 5000
            }
        ],

        "hotels": [
            {
                "name": "Pink City Residency",
                "area": "MI Road",
                "price_per_night": 2200
            },
            {
                "name": "Royal Jaipur Stay",
                "area": "Bani Park",
                "price_per_night": 3000
            }
        ],

        "activities": [
            {
                "name": "Amber Fort",
                "category": "Heritage",
                "cost": 200
            },
            {
                "name": "Hawa Mahal",
                "category": "Heritage",
                "cost": 100
            },
            {
                "name": "City Palace",
                "category": "Culture",
                "cost": 300
            },
            {
                "name": "Johari Bazaar",
                "category": "Shopping",
                "cost": 0
            }
        ]
    },


    # --------------------------------------------------------
    # UDAIPUR
    # --------------------------------------------------------

    "udaipur": {
        "state": "Rajasthan",
        "type": "Heritage / Lakes",

        "flights": [
            {
                "airline": "IndiGo",
                "route": "Bengaluru → Udaipur",
                "price": 5200
            }
        ],

        "hotels": [
            {
                "name": "Lake View Residency",
                "area": "Lake Pichola",
                "price_per_night": 2800
            },
            {
                "name": "Royal Udaipur Stay",
                "area": "Hathipole",
                "price_per_night": 2400
            }
        ],

        "activities": [
            {
                "name": "Lake Pichola",
                "category": "Nature",
                "cost": 500
            },
            {
                "name": "City Palace",
                "category": "Heritage",
                "cost": 300
            },
            {
                "name": "Jagdish Temple",
                "category": "Culture",
                "cost": 0
            },
            {
                "name": "Bagore Ki Haveli",
                "category": "Culture",
                "cost": 150
            }
        ]
    },


    # --------------------------------------------------------
    # DELHI
    # --------------------------------------------------------

    "delhi": {
        "state": "Delhi",
        "type": "History / Food / Culture",

        "flights": [
            {
                "airline": "IndiGo",
                "route": "Bengaluru → Delhi",
                "price": 4500
            }
        ],

        "hotels": [
            {
                "name": "Delhi Central Stay",
                "area": "Paharganj",
                "price_per_night": 1800
            },
            {
                "name": "Capital Comfort Hotel",
                "area": "Karol Bagh",
                "price_per_night": 2500
            }
        ],

        "activities": [
            {
                "name": "India Gate",
                "category": "Sightseeing",
                "cost": 0
            },
            {
                "name": "Red Fort",
                "category": "History",
                "cost": 150
            },
            {
                "name": "Qutub Minar",
                "category": "History",
                "cost": 200
            },
            {
                "name": "Chandni Chowk",
                "category": "Food / Shopping",
                "cost": 0
            }
        ]
    },


    # --------------------------------------------------------
    # MUMBAI
    # --------------------------------------------------------

    "mumbai": {
        "state": "Maharashtra",
        "type": "City / Food / Entertainment",

        "flights": [
            {
                "airline": "IndiGo",
                "route": "Bengaluru → Mumbai",
                "price": 3800
            }
        ],

        "hotels": [
            {
                "name": "Mumbai City Stay",
                "area": "Andheri",
                "price_per_night": 2500
            },
            {
                "name": "Marine View Hotel",
                "area": "Colaba",
                "price_per_night": 3500
            }
        ],

        "activities": [
            {
                "name": "Gateway of India",
                "category": "Sightseeing",
                "cost": 0
            },
            {
                "name": "Marine Drive",
                "category": "Nature",
                "cost": 0
            },
            {
                "name": "Elephanta Caves",
                "category": "Heritage",
                "cost": 500
            },
            {
                "name": "Colaba Causeway",
                "category": "Shopping",
                "cost": 0
            }
        ]
    },


    # --------------------------------------------------------
    # BENGALURU
    # --------------------------------------------------------

    "bengaluru": {
        "state": "Karnataka",
        "type": "City / Food / Technology",

        "flights": [
            {
                "airline": "IndiGo",
                "route": "Mumbai → Bengaluru",
                "price": 4200
            }
        ],

        "hotels": [
            {
                "name": "City Comfort Hotel",
                "area": "Indiranagar",
                "price_per_night": 2500
            },
            {
                "name": "Bangalore Central Stay",
                "area": "MG Road",
                "price_per_night": 3000
            }
        ],

        "activities": [
            {
                "name": "Lalbagh Botanical Garden",
                "category": "Nature",
                "cost": 50
            },
            {
                "name": "Bangalore Palace",
                "category": "Heritage",
                "cost": 250
            },
            {
                "name": "Cubbon Park",
                "category": "Nature",
                "cost": 0
            },
            {
                "name": "UB City",
                "category": "Shopping",
                "cost": 0
            }
        ]
    },


    # --------------------------------------------------------
    # HYDERABAD
    # --------------------------------------------------------

    "hyderabad": {
        "state": "Telangana",
        "type": "History / Food / City",

        "flights": [
            {
                "airline": "IndiGo",
                "route": "Bengaluru → Hyderabad",
                "price": 3000
            }
        ],

        "hotels": [
            {
                "name": "Hyderabad Central Hotel",
                "area": "Hitech City",
                "price_per_night": 2300
            },
            {
                "name": "Charminar Stay",
                "area": "Old Hyderabad",
                "price_per_night": 1800
            }
        ],

        "activities": [
            {
                "name": "Charminar",
                "category": "Heritage",
                "cost": 50
            },
            {
                "name": "Golconda Fort",
                "category": "History",
                "cost": 100
            },
            {
                "name": "Hussain Sagar",
                "category": "Nature",
                "cost": 0
            },
            {
                "name": "Laad Bazaar",
                "category": "Shopping",
                "cost": 0
            }
        ]
    },


    # --------------------------------------------------------
    # KOCHI
    # --------------------------------------------------------

    "kochi": {
        "state": "Kerala",
        "type": "Coastal / Culture",

        "flights": [
            {
                "airline": "IndiGo",
                "route": "Bengaluru → Kochi",
                "price": 2800
            }
        ],

        "hotels": [
            {
                "name": "Fort Kochi Stay",
                "area": "Fort Kochi",
                "price_per_night": 2200
            },
            {
                "name": "Kerala Comfort Hotel",
                "area": "Ernakulam",
                "price_per_night": 2000
            }
        ],

        "activities": [
            {
                "name": "Fort Kochi",
                "category": "Culture",
                "cost": 0
            },
            {
                "name": "Chinese Fishing Nets",
                "category": "Culture",
                "cost": 0
            },
            {
                "name": "Mattancherry Palace",
                "category": "Heritage",
                "cost": 20
            },
            {
                "name": "Marine Drive",
                "category": "Nature",
                "cost": 0
            }
        ]
    },


    # --------------------------------------------------------
    # MUNNAR
    # --------------------------------------------------------

    "munnar": {
        "state": "Kerala",
        "type": "Hills / Nature",

        "flights": [
            {
                "airline": "IndiGo",
                "route": "Bengaluru → Kochi",
                "price": 2800
            }
        ],

        "hotels": [
            {
                "name": "Munnar Hills Stay",
                "area": "Munnar",
                "price_per_night": 2200
            },
            {
                "name": "Tea Valley Resort",
                "area": "Chithirapuram",
                "price_per_night": 3000
            }
        ],

        "activities": [
            {
                "name": "Tea Gardens",
                "category": "Nature",
                "cost": 0
            },
            {
                "name": "Mattupetty Dam",
                "category": "Nature",
                "cost": 100
            },
            {
                "name": "Echo Point",
                "category": "Nature",
                "cost": 50
            },
            {
                "name": "Eravikulam National Park",
                "category": "Wildlife",
                "cost": 200
            }
        ]
    },


    # --------------------------------------------------------
    # OOTY
    # --------------------------------------------------------

    "ooty": {
        "state": "Tamil Nadu",
        "type": "Hills / Nature",

        "flights": [
            {
                "airline": "IndiGo",
                "route": "Bengaluru → Coimbatore",
                "price": 2500
            }
        ],

        "hotels": [
            {
                "name": "Ooty Hills Hotel",
                "area": "Ooty",
                "price_per_night": 2200
            },
            {
                "name": "Blue Mountain Stay",
                "area": "Coonoor Road",
                "price_per_night": 2600
            }
        ],

        "activities": [
            {
                "name": "Ooty Lake",
                "category": "Nature",
                "cost": 200
            },
            {
                "name": "Botanical Garden",
                "category": "Nature",
                "cost": 50
            },
            {
                "name": "Doddabetta Peak",
                "category": "Nature",
                "cost": 20
            },
            {
                "name": "Nilgiri Mountain Railway",
                "category": "Experience",
                "cost": 500
            }
        ]
    },


    # --------------------------------------------------------
    # MYSURU
    # --------------------------------------------------------

    "mysuru": {
        "state": "Karnataka",
        "type": "Heritage / Culture",

        "flights": [
            {
                "airline": "IndiGo",
                "route": "Bengaluru → Mysuru",
                "price": 1500
            }
        ],

        "hotels": [
            {
                "name": "Mysuru Palace Stay",
                "area": "City Centre",
                "price_per_night": 1800
            },
            {
                "name": "Royal Mysuru Hotel",
                "area": "VV Mohalla",
                "price_per_night": 2200
            }
        ],

        "activities": [
            {
                "name": "Mysore Palace",
                "category": "Heritage",
                "cost": 100
            },
            {
                "name": "Chamundi Hills",
                "category": "Nature",
                "cost": 0
            },
            {
                "name": "Brindavan Gardens",
                "category": "Nature",
                "cost": 50
            },
            {
                "name": "Devaraja Market",
                "category": "Shopping",
                "cost": 0
            }
        ]
    },


    # --------------------------------------------------------
    # RISHIKESH
    # --------------------------------------------------------

    "rishikesh": {
        "state": "Uttarakhand",
        "type": "Adventure / Spiritual",

        "flights": [
            {
                "airline": "IndiGo",
                "route": "Bengaluru → Delhi",
                "price": 4500
            }
        ],

        "hotels": [
            {
                "name": "Ganga Riverside Stay",
                "area": "Tapovan",
                "price_per_night": 2000
            },
            {
                "name": "Rishikesh Adventure Hotel",
                "area": "Laxman Jhula",
                "price_per_night": 2400
            }
        ],

        "activities": [
            {
                "name": "River Rafting",
                "category": "Adventure",
                "cost": 1200
            },
            {
                "name": "Laxman Jhula Area",
                "category": "Sightseeing",
                "cost": 0
            },
            {
                "name": "Ganga Aarti",
                "category": "Spiritual",
                "cost": 0
            },
            {
                "name": "Beatles Ashram",
                "category": "Culture",
                "cost": 150
            }
        ]
    },


    # --------------------------------------------------------
    # DARJEELING
    # --------------------------------------------------------

    "darjeeling": {
        "state": "West Bengal",
        "type": "Hills / Nature",

        "flights": [
            {
                "airline": "IndiGo",
                "route": "Bengaluru → Kolkata",
                "price": 4500
            }
        ],

        "hotels": [
            {
                "name": "Darjeeling Hill View",
                "area": "Darjeeling",
                "price_per_night": 2300
            },
            {
                "name": "Himalayan Comfort Stay",
                "area": "Chowrasta",
                "price_per_night": 2800
            }
        ],

        "activities": [
            {
                "name": "Tiger Hill",
                "category": "Nature",
                "cost": 100
            },
            {
                "name": "Darjeeling Himalayan Railway",
                "category": "Experience",
                "cost": 1200
            },
            {
                "name": "Batasia Loop",
                "category": "Sightseeing",
                "cost": 30
            },
            {
                "name": "Tea Garden Visit",
                "category": "Nature",
                "cost": 100
            }
        ]
    },


    # --------------------------------------------------------
    # VARANASI
    # --------------------------------------------------------

    "varanasi": {
        "state": "Uttar Pradesh",
        "type": "Spiritual / Culture",

        "flights": [
            {
                "airline": "IndiGo",
                "route": "Bengaluru → Varanasi",
                "price": 4800
            }
        ],

        "hotels": [
            {
                "name": "Ganga View Stay",
                "area": "Assi Ghat",
                "price_per_night": 1800
            },
            {
                "name": "Varanasi Heritage Hotel",
                "area": "Godowlia",
                "price_per_night": 2300
            }
        ],

        "activities": [
            {
                "name": "Ganga Aarti",
                "category": "Spiritual",
                "cost": 0
            },
            {
                "name": "Boat Ride",
                "category": "Experience",
                "cost": 500
            },
            {
                "name": "Kashi Vishwanath Temple",
                "category": "Spiritual",
                "cost": 0
            },
            {
                "name": "Assi Ghat",
                "category": "Culture",
                "cost": 0
            }
        ]
    },


    # --------------------------------------------------------
    # AGRA
    # --------------------------------------------------------

    "agra": {
        "state": "Uttar Pradesh",
        "type": "Heritage / History",

        "flights": [
            {
                "airline": "IndiGo",
                "route": "Bengaluru → Delhi",
                "price": 4500
            }
        ],

        "hotels": [
            {
                "name": "Taj View Stay",
                "area": "Tajganj",
                "price_per_night": 2000
            },
            {
                "name": "Agra Heritage Hotel",
                "area": "Fatehabad Road",
                "price_per_night": 2400
            }
        ],

        "activities": [
            {
                "name": "Taj Mahal",
                "category": "Heritage",
                "cost": 250
            },
            {
                "name": "Agra Fort",
                "category": "History",
                "cost": 50
            },
            {
                "name": "Mehtab Bagh",
                "category": "Nature",
                "cost": 30
            },
            {
                "name": "Agra Local Market",
                "category": "Shopping",
                "cost": 0
            }
        ]
    },


    # --------------------------------------------------------
    # AMRITSAR
    # --------------------------------------------------------

    "amritsar": {
        "state": "Punjab",
        "type": "Culture / Food / History",

        "flights": [
            {
                "airline": "IndiGo",
                "route": "Bengaluru → Amritsar",
                "price": 5000
            }
        ],

        "hotels": [
            {
                "name": "Golden Temple Stay",
                "area": "Amritsar",
                "price_per_night": 1800
            },
            {
                "name": "Punjab Heritage Hotel",
                "area": "Lawrence Road",
                "price_per_night": 2500
            }
        ],

        "activities": [
            {
                "name": "Golden Temple",
                "category": "Culture",
                "cost": 0
            },
            {
                "name": "Jallianwala Bagh",
                "category": "History",
                "cost": 0
            },
            {
                "name": "Wagah Border",
                "category": "Experience",
                "cost": 0
            },
            {
                "name": "Amritsari Food Walk",
                "category": "Food",
                "cost": 500
            }
        ]
    },


    # --------------------------------------------------------
    # PONDICHERRY
    # --------------------------------------------------------

    "pondicherry": {
        "state": "Puducherry",
        "type": "Beach / Culture",

        "flights": [
            {
                "airline": "IndiGo",
                "route": "Bengaluru → Chennai",
                "price": 2500
            }
        ],

        "hotels": [
            {
                "name": "French Quarter Stay",
                "area": "White Town",
                "price_per_night": 2500
            },
            {
                "name": "Pondicherry Beach Hotel",
                "area": "Promenade",
                "price_per_night": 3000
            }
        ],

        "activities": [
            {
                "name": "Promenade Beach",
                "category": "Beach",
                "cost": 0
            },
            {
                "name": "Auroville",
                "category": "Culture",
                "cost": 0
            },
            {
                "name": "White Town",
                "category": "Exploration",
                "cost": 0
            },
            {
                "name": "Paradise Beach",
                "category": "Beach",
                "cost": 200
            }
        ]
    },


    # --------------------------------------------------------
    # COORG
    # --------------------------------------------------------

    "coorg": {
        "state": "Karnataka",
        "type": "Nature / Hills",

        "flights": [
            {
                "airline": "IndiGo",
                "route": "Bengaluru → Mysuru",
                "price": 1500
            }
        ],

        "hotels": [
            {
                "name": "Coorg Coffee Estate Stay",
                "area": "Madikeri",
                "price_per_night": 2200
            },
            {
                "name": "Coorg Valley Resort",
                "area": "Kushalnagar",
                "price_per_night": 2800
            }
        ],

        "activities": [
            {
                "name": "Abbey Falls",
                "category": "Nature",
                "cost": 30
            },
            {
                "name": "Raja's Seat",
                "category": "Nature",
                "cost": 20
            },
            {
                "name": "Coffee Estate Visit",
                "category": "Experience",
                "cost": 300
            },
            {
                "name": "Dubare Elephant Camp",
                "category": "Wildlife",
                "cost": 500
            }
        ]
    }
}




# ============================================================
# EXPANDED AIRPORT-AWARE DESTINATION CATALOG
# ============================================================
# These entries extend destination recognition without replacing
# the original local DESTINATIONS catalog above.
#
# Each entry maps a user-facing destination/region to a practical
# representative airport. Live flight/hotel/activity tools continue
# to use the existing functions below.
#
# Prices are NOT stored here; this catalog only improves destination
# recognition and airport routing.
# ============================================================

AIRPORT_DESTINATIONS = {

    # ---------------- INDIA REGIONS / COMMON TRAVEL AREAS ----------------
    "kerala": {"canonical": "Kerala", "lookup": "Kochi", "country": "India", "country_code": "IN", "airport_iata": "COK"},
    "kerala backwaters": {"canonical": "Kerala", "lookup": "Alappuzha", "country": "India", "country_code": "IN", "airport_iata": "COK"},
    "alappuzha": {"canonical": "Alappuzha", "lookup": "Alappuzha", "country": "India", "country_code": "IN", "airport_iata": "COK"},
    "alleppey": {"canonical": "Alappuzha", "lookup": "Alappuzha", "country": "India", "country_code": "IN", "airport_iata": "COK"},
    "wayanad": {"canonical": "Wayanad", "lookup": "Kalpetta", "country": "India", "country_code": "IN", "airport_iata": "CCJ"},
    "varkala": {"canonical": "Varkala", "lookup": "Varkala", "country": "India", "country_code": "IN", "airport_iata": "TRV"},
    "thekkady": {"canonical": "Thekkady", "lookup": "Thekkady", "country": "India", "country_code": "IN", "airport_iata": "COK"},
    "kumarakom": {"canonical": "Kumarakom", "lookup": "Kumarakom", "country": "India", "country_code": "IN", "airport_iata": "COK"},
    "himachal pradesh": {"canonical": "Himachal Pradesh", "lookup": "Manali", "country": "India", "country_code": "IN", "airport_iata": "KUU"},
    "himachal": {"canonical": "Himachal Pradesh", "lookup": "Manali", "country": "India", "country_code": "IN", "airport_iata": "KUU"},
    "uttarakhand": {"canonical": "Uttarakhand", "lookup": "Dehradun", "country": "India", "country_code": "IN", "airport_iata": "DED"},
    "rajasthan": {"canonical": "Rajasthan", "lookup": "Jaipur", "country": "India", "country_code": "IN", "airport_iata": "JAI"},
    "karnataka": {"canonical": "Karnataka", "lookup": "Bengaluru", "country": "India", "country_code": "IN", "airport_iata": "BLR"},
    "tamil nadu": {"canonical": "Tamil Nadu", "lookup": "Chennai", "country": "India", "country_code": "IN", "airport_iata": "MAA"},
    "maharashtra": {"canonical": "Maharashtra", "lookup": "Mumbai", "country": "India", "country_code": "IN", "airport_iata": "BOM"},
    "uttar pradesh": {"canonical": "Uttar Pradesh", "lookup": "Lucknow", "country": "India", "country_code": "IN", "airport_iata": "LKO"},
    "west bengal": {"canonical": "West Bengal", "lookup": "Kolkata", "country": "India", "country_code": "IN", "airport_iata": "CCU"},
    "odisha": {"canonical": "Odisha", "lookup": "Bhubaneswar", "country": "India", "country_code": "IN", "airport_iata": "BBI"},
    "orissa": {"canonical": "Odisha", "lookup": "Bhubaneswar", "country": "India", "country_code": "IN", "airport_iata": "BBI"},
    "sikkim": {"canonical": "Sikkim", "lookup": "Gangtok", "country": "India", "country_code": "IN", "airport_iata": "PYG"},
    "meghalaya": {"canonical": "Meghalaya", "lookup": "Shillong", "country": "India", "country_code": "IN", "airport_iata": "SHL"},
    "assam": {"canonical": "Assam", "lookup": "Guwahati", "country": "India", "country_code": "IN", "airport_iata": "GAU"},
    "andaman and nicobar islands": {"canonical": "Andaman Islands", "lookup": "Port Blair", "country": "India", "country_code": "IN", "airport_iata": "IXZ"},
    "lakshadweep": {"canonical": "Lakshadweep", "lookup": "Agatti", "country": "India", "country_code": "IN", "airport_iata": "AGX"},

    # ---------------- INDIA ----------------
    "goa": {"canonical": "Goa", "lookup": "Goa", "country": "India", "country_code": "IN", "airport_iata": "GOI"},
    "mumbai": {"canonical": "Mumbai", "lookup": "Mumbai", "country": "India", "country_code": "IN", "airport_iata": "BOM"},
    "delhi": {"canonical": "Delhi", "lookup": "Delhi", "country": "India", "country_code": "IN", "airport_iata": "DEL"},
    "new delhi": {"canonical": "Delhi", "lookup": "Delhi", "country": "India", "country_code": "IN", "airport_iata": "DEL"},
    "bengaluru": {"canonical": "Bengaluru", "lookup": "Bengaluru", "country": "India", "country_code": "IN", "airport_iata": "BLR"},
    "bangalore": {"canonical": "Bengaluru", "lookup": "Bengaluru", "country": "India", "country_code": "IN", "airport_iata": "BLR"},
    "mysuru": {"canonical": "Mysuru", "lookup": "Mysuru", "country": "India", "country_code": "IN", "airport_iata": "MYQ"},
    "mysore": {"canonical": "Mysuru", "lookup": "Mysuru", "country": "India", "country_code": "IN", "airport_iata": "MYQ"},
    "hyderabad": {"canonical": "Hyderabad", "lookup": "Hyderabad", "country": "India", "country_code": "IN", "airport_iata": "HYD"},
    "chennai": {"canonical": "Chennai", "lookup": "Chennai", "country": "India", "country_code": "IN", "airport_iata": "MAA"},
    "kolkata": {"canonical": "Kolkata", "lookup": "Kolkata", "country": "India", "country_code": "IN", "airport_iata": "CCU"},
    "pune": {"canonical": "Pune", "lookup": "Pune", "country": "India", "country_code": "IN", "airport_iata": "PNQ"},
    "ahmedabad": {"canonical": "Ahmedabad", "lookup": "Ahmedabad", "country": "India", "country_code": "IN", "airport_iata": "AMD"},
    "surat": {"canonical": "Surat", "lookup": "Surat", "country": "India", "country_code": "IN", "airport_iata": "STV"},
    "vadodara": {"canonical": "Vadodara", "lookup": "Vadodara", "country": "India", "country_code": "IN", "airport_iata": "BDQ"},
    "rajkot": {"canonical": "Rajkot", "lookup": "Rajkot", "country": "India", "country_code": "IN", "airport_iata": "HSR"},
    "bhuj": {"canonical": "Bhuj", "lookup": "Bhuj", "country": "India", "country_code": "IN", "airport_iata": "BHJ"},
    "nashik": {"canonical": "Nashik", "lookup": "Nashik", "country": "India", "country_code": "IN", "airport_iata": "ISK"},
    "nagpur": {"canonical": "Nagpur", "lookup": "Nagpur", "country": "India", "country_code": "IN", "airport_iata": "NAG"},
    "aurangabad": {"canonical": "Aurangabad", "lookup": "Aurangabad", "country": "India", "country_code": "IN", "airport_iata": "IXU"},
    "chhatrapati sambhajinagar": {"canonical": "Chhatrapati Sambhajinagar", "lookup": "Chhatrapati Sambhajinagar", "country": "India", "country_code": "IN", "airport_iata": "IXU"},
    "goa airport": {"canonical": "Goa", "lookup": "Goa", "country": "India", "country_code": "IN", "airport_iata": "GOI"},
    "jaipur": {"canonical": "Jaipur", "lookup": "Jaipur", "country": "India", "country_code": "IN", "airport_iata": "JAI"},
    "jodhpur": {"canonical": "Jodhpur", "lookup": "Jodhpur", "country": "India", "country_code": "IN", "airport_iata": "JDH"},
    "udaipur": {"canonical": "Udaipur", "lookup": "Udaipur", "country": "India", "country_code": "IN", "airport_iata": "UDR"},
    "jaisalmer": {"canonical": "Jaisalmer", "lookup": "Jaisalmer", "country": "India", "country_code": "IN", "airport_iata": "JSA"},
    "kota": {"canonical": "Kota", "lookup": "Kota", "country": "India", "country_code": "IN", "airport_iata": "KTU"},
    "bikaner": {"canonical": "Bikaner", "lookup": "Bikaner", "country": "India", "country_code": "IN", "airport_iata": "BKB"},
    "amritsar": {"canonical": "Amritsar", "lookup": "Amritsar", "country": "India", "country_code": "IN", "airport_iata": "ATQ"},
    "chandigarh": {"canonical": "Chandigarh", "lookup": "Chandigarh", "country": "India", "country_code": "IN", "airport_iata": "IXC"},
    "jammu": {"canonical": "Jammu", "lookup": "Jammu", "country": "India", "country_code": "IN", "airport_iata": "IXJ"},
    "srinagar": {"canonical": "Srinagar", "lookup": "Srinagar", "country": "India", "country_code": "IN", "airport_iata": "SXR"},
    "kashmir": {"canonical": "Kashmir", "lookup": "Srinagar", "country": "India", "country_code": "IN", "airport_iata": "SXR"},
    "jammu and kashmir": {"canonical": "Kashmir", "lookup": "Srinagar", "country": "India", "country_code": "IN", "airport_iata": "SXR"},
    "jammu & kashmir": {"canonical": "Kashmir", "lookup": "Srinagar", "country": "India", "country_code": "IN", "airport_iata": "SXR"},
    "leh": {"canonical": "Leh", "lookup": "Leh", "country": "India", "country_code": "IN", "airport_iata": "IXL"},
    "ladakh": {"canonical": "Ladakh", "lookup": "Leh", "country": "India", "country_code": "IN", "airport_iata": "IXL"},
    "manali": {"canonical": "Manali", "lookup": "Manali", "country": "India", "country_code": "IN", "airport_iata": "KUU"},
    "kullu": {"canonical": "Kullu", "lookup": "Kullu", "country": "India", "country_code": "IN", "airport_iata": "KUU"},
    "shimla": {"canonical": "Shimla", "lookup": "Shimla", "country": "India", "country_code": "IN", "airport_iata": "SLV"},
    "dharamshala": {"canonical": "Dharamshala", "lookup": "Dharamshala", "country": "India", "country_code": "IN", "airport_iata": "DHM"},
    "dharamsala": {"canonical": "Dharamshala", "lookup": "Dharamshala", "country": "India", "country_code": "IN", "airport_iata": "DHM"},
    "dehradun": {"canonical": "Dehradun", "lookup": "Dehradun", "country": "India", "country_code": "IN", "airport_iata": "DED"},
    "rishikesh": {"canonical": "Rishikesh", "lookup": "Rishikesh", "country": "India", "country_code": "IN", "airport_iata": "DED"},
    "agra": {"canonical": "Agra", "lookup": "Agra", "country": "India", "country_code": "IN", "airport_iata": "AGR"},
    "varanasi": {"canonical": "Varanasi", "lookup": "Varanasi", "country": "India", "country_code": "IN", "airport_iata": "VNS"},
    "lucknow": {"canonical": "Lucknow", "lookup": "Lucknow", "country": "India", "country_code": "IN", "airport_iata": "LKO"},
    "ayodhya": {"canonical": "Ayodhya", "lookup": "Ayodhya", "country": "India", "country_code": "IN", "airport_iata": "AYJ"},
    "prayagraj": {"canonical": "Prayagraj", "lookup": "Prayagraj", "country": "India", "country_code": "IN", "airport_iata": "IXD"},
    "kanpur": {"canonical": "Kanpur", "lookup": "Kanpur", "country": "India", "country_code": "IN", "airport_iata": "KNU"},
    "khajuraho": {"canonical": "Khajuraho", "lookup": "Khajuraho", "country": "India", "country_code": "IN", "airport_iata": "HJR"},
    "gaya": {"canonical": "Gaya", "lookup": "Gaya", "country": "India", "country_code": "IN", "airport_iata": "GAY"},
    "patna": {"canonical": "Patna", "lookup": "Patna", "country": "India", "country_code": "IN", "airport_iata": "PAT"},
    "ranchi": {"canonical": "Ranchi", "lookup": "Ranchi", "country": "India", "country_code": "IN", "airport_iata": "IXR"},
    "bhubaneswar": {"canonical": "Bhubaneswar", "lookup": "Bhubaneswar", "country": "India", "country_code": "IN", "airport_iata": "BBI"},
    "puri": {"canonical": "Puri", "lookup": "Puri", "country": "India", "country_code": "IN", "airport_iata": "BBI"},
    "guwahati": {"canonical": "Guwahati", "lookup": "Guwahati", "country": "India", "country_code": "IN", "airport_iata": "GAU"},
    "shillong": {"canonical": "Shillong", "lookup": "Shillong", "country": "India", "country_code": "IN", "airport_iata": "SHL"},
    "imphal": {"canonical": "Imphal", "lookup": "Imphal", "country": "India", "country_code": "IN", "airport_iata": "IMF"},
    "agartala": {"canonical": "Agartala", "lookup": "Agartala", "country": "India", "country_code": "IN", "airport_iata": "IXA"},
    "aizawl": {"canonical": "Aizawl", "lookup": "Aizawl", "country": "India", "country_code": "IN", "airport_iata": "AJL"},
    "kohima": {"canonical": "Kohima", "lookup": "Kohima", "country": "India", "country_code": "IN", "airport_iata": "DMU"},
    "dibrugarh": {"canonical": "Dibrugarh", "lookup": "Dibrugarh", "country": "India", "country_code": "IN", "airport_iata": "DIB"},
    "jorhat": {"canonical": "Jorhat", "lookup": "Jorhat", "country": "India", "country_code": "IN", "airport_iata": "JRH"},
    "silchar": {"canonical": "Silchar", "lookup": "Silchar", "country": "India", "country_code": "IN", "airport_iata": "IXS"},
    "itanagar": {"canonical": "Itanagar", "lookup": "Itanagar", "country": "India", "country_code": "IN", "airport_iata": "HGI"},
    "gangtok": {"canonical": "Gangtok", "lookup": "Gangtok", "country": "India", "country_code": "IN", "airport_iata": "PYG"},
    "siliguri": {"canonical": "Siliguri", "lookup": "Siliguri", "country": "India", "country_code": "IN", "airport_iata": "IXB"},
    "darjeeling": {"canonical": "Darjeeling", "lookup": "Darjeeling", "country": "India", "country_code": "IN", "airport_iata": "IXB"},
    "bagdogra": {"canonical": "Bagdogra", "lookup": "Bagdogra", "country": "India", "country_code": "IN", "airport_iata": "IXB"},
    "kochi": {"canonical": "Kochi", "lookup": "Kochi", "country": "India", "country_code": "IN", "airport_iata": "COK"},
    "cochin": {"canonical": "Kochi", "lookup": "Kochi", "country": "India", "country_code": "IN", "airport_iata": "COK"},
    "munnar": {"canonical": "Munnar", "lookup": "Munnar", "country": "India", "country_code": "IN", "airport_iata": "COK"},
    "thiruvananthapuram": {"canonical": "Thiruvananthapuram", "lookup": "Thiruvananthapuram", "country": "India", "country_code": "IN", "airport_iata": "TRV"},
    "trivandrum": {"canonical": "Thiruvananthapuram", "lookup": "Thiruvananthapuram", "country": "India", "country_code": "IN", "airport_iata": "TRV"},
    "kozhikode": {"canonical": "Kozhikode", "lookup": "Kozhikode", "country": "India", "country_code": "IN", "airport_iata": "CCJ"},
    "calicut": {"canonical": "Kozhikode", "lookup": "Kozhikode", "country": "India", "country_code": "IN", "airport_iata": "CCJ"},
    "mangaluru": {"canonical": "Mangaluru", "lookup": "Mangaluru", "country": "India", "country_code": "IN", "airport_iata": "IXE"},
    "mangalore": {"canonical": "Mangaluru", "lookup": "Mangaluru", "country": "India", "country_code": "IN", "airport_iata": "IXE"},
    "coimbatore": {"canonical": "Coimbatore", "lookup": "Coimbatore", "country": "India", "country_code": "IN", "airport_iata": "CJB"},
    "ooty": {"canonical": "Ooty", "lookup": "Ooty", "country": "India", "country_code": "IN", "airport_iata": "CJB"},
    "madurai": {"canonical": "Madurai", "lookup": "Madurai", "country": "India", "country_code": "IN", "airport_iata": "IXM"},
    "tiruchirappalli": {"canonical": "Tiruchirappalli", "lookup": "Tiruchirappalli", "country": "India", "country_code": "IN", "airport_iata": "TRZ"},
    "trichy": {"canonical": "Tiruchirappalli", "lookup": "Tiruchirappalli", "country": "India", "country_code": "IN", "airport_iata": "TRZ"},
    "tirupati": {"canonical": "Tirupati", "lookup": "Tirupati", "country": "India", "country_code": "IN", "airport_iata": "TIR"},
    "vijayawada": {"canonical": "Vijayawada", "lookup": "Vijayawada", "country": "India", "country_code": "IN", "airport_iata": "VGA"},
    "visakhapatnam": {"canonical": "Visakhapatnam", "lookup": "Visakhapatnam", "country": "India", "country_code": "IN", "airport_iata": "VTZ"},
    "vizag": {"canonical": "Visakhapatnam", "lookup": "Visakhapatnam", "country": "India", "country_code": "IN", "airport_iata": "VTZ"},
    "hubballi": {"canonical": "Hubballi", "lookup": "Hubballi", "country": "India", "country_code": "IN", "airport_iata": "HBX"},
    "belagavi": {"canonical": "Belagavi", "lookup": "Belagavi", "country": "India", "country_code": "IN", "airport_iata": "IXG"},
    "kalaburagi": {"canonical": "Kalaburagi", "lookup": "Kalaburagi", "country": "India", "country_code": "IN", "airport_iata": "GBI"},
    "pondicherry": {"canonical": "Pondicherry", "lookup": "Pondicherry", "country": "India", "country_code": "IN", "airport_iata": "PNY"},
    "puducherry": {"canonical": "Pondicherry", "lookup": "Pondicherry", "country": "India", "country_code": "IN", "airport_iata": "PNY"},
    "port blair": {"canonical": "Port Blair", "lookup": "Port Blair", "country": "India", "country_code": "IN", "airport_iata": "IXZ"},
    "andaman": {"canonical": "Andaman Islands", "lookup": "Port Blair", "country": "India", "country_code": "IN", "airport_iata": "IXZ"},
    "andaman and nicobar": {"canonical": "Andaman Islands", "lookup": "Port Blair", "country": "India", "country_code": "IN", "airport_iata": "IXZ"},
    "coorg": {"canonical": "Coorg", "lookup": "Coorg", "country": "India", "country_code": "IN", "airport_iata": "IXE"},
    "kodagu": {"canonical": "Coorg", "lookup": "Coorg", "country": "India", "country_code": "IN", "airport_iata": "IXE"},

    # ---------------- MIDDLE EAST ----------------
    "dubai": {"canonical": "Dubai", "lookup": "Dubai", "country": "United Arab Emirates", "country_code": "AE", "airport_iata": "DXB"},
    "abu dhabi": {"canonical": "Abu Dhabi", "lookup": "Abu Dhabi", "country": "United Arab Emirates", "country_code": "AE", "airport_iata": "AUH"},
    "doha": {"canonical": "Doha", "lookup": "Doha", "country": "Qatar", "country_code": "QA", "airport_iata": "DOH"},
    "muscat": {"canonical": "Muscat", "lookup": "Muscat", "country": "Oman", "country_code": "OM", "airport_iata": "MCT"},
    "riyadh": {"canonical": "Riyadh", "lookup": "Riyadh", "country": "Saudi Arabia", "country_code": "SA", "airport_iata": "RUH"},
    "jeddah": {"canonical": "Jeddah", "lookup": "Jeddah", "country": "Saudi Arabia", "country_code": "SA", "airport_iata": "JED"},
    "manama": {"canonical": "Manama", "lookup": "Manama", "country": "Bahrain", "country_code": "BH", "airport_iata": "BAH"},
    "bahrain": {"canonical": "Bahrain", "lookup": "Manama", "country": "Bahrain", "country_code": "BH", "airport_iata": "BAH"},
    "kuwait city": {"canonical": "Kuwait City", "lookup": "Kuwait City", "country": "Kuwait", "country_code": "KW", "airport_iata": "KWI"},
    "amman": {"canonical": "Amman", "lookup": "Amman", "country": "Jordan", "country_code": "JO", "airport_iata": "AMM"},
    "tel aviv": {"canonical": "Tel Aviv", "lookup": "Tel Aviv", "country": "Israel", "country_code": "IL", "airport_iata": "TLV"},
    "istanbul": {"canonical": "Istanbul", "lookup": "Istanbul", "country": "Türkiye", "country_code": "TR", "airport_iata": "IST"},

    # ---------------- SOUTHEAST ASIA ----------------
    "singapore": {"canonical": "Singapore", "lookup": "Singapore", "country": "Singapore", "country_code": "SG", "airport_iata": "SIN"},
    "bangkok": {"canonical": "Bangkok", "lookup": "Bangkok", "country": "Thailand", "country_code": "TH", "airport_iata": "BKK"},
    "phuket": {"canonical": "Phuket", "lookup": "Phuket", "country": "Thailand", "country_code": "TH", "airport_iata": "HKT"},
    "chiang mai": {"canonical": "Chiang Mai", "lookup": "Chiang Mai", "country": "Thailand", "country_code": "TH", "airport_iata": "CNX"},
    "kuala lumpur": {"canonical": "Kuala Lumpur", "lookup": "Kuala Lumpur", "country": "Malaysia", "country_code": "MY", "airport_iata": "KUL"},
    "bali": {"canonical": "Bali", "lookup": "Denpasar", "country": "Indonesia", "country_code": "ID", "airport_iata": "DPS"},
    "denpasar": {"canonical": "Denpasar", "lookup": "Denpasar", "country": "Indonesia", "country_code": "ID", "airport_iata": "DPS"},
    "jakarta": {"canonical": "Jakarta", "lookup": "Jakarta", "country": "Indonesia", "country_code": "ID", "airport_iata": "CGK"},
    "hanoi": {"canonical": "Hanoi", "lookup": "Hanoi", "country": "Vietnam", "country_code": "VN", "airport_iata": "HAN"},
    "ho chi minh city": {"canonical": "Ho Chi Minh City", "lookup": "Ho Chi Minh City", "country": "Vietnam", "country_code": "VN", "airport_iata": "SGN"},
    "manila": {"canonical": "Manila", "lookup": "Manila", "country": "Philippines", "country_code": "PH", "airport_iata": "MNL"},
    "cebu": {"canonical": "Cebu", "lookup": "Cebu City", "country": "Philippines", "country_code": "PH", "airport_iata": "CEB"},
    "phnom penh": {"canonical": "Phnom Penh", "lookup": "Phnom Penh", "country": "Cambodia", "country_code": "KH", "airport_iata": "PNH"},
    "siem reap": {"canonical": "Siem Reap", "lookup": "Siem Reap", "country": "Cambodia", "country_code": "KH", "airport_iata": "SAI"},
    "yangon": {"canonical": "Yangon", "lookup": "Yangon", "country": "Myanmar", "country_code": "MM", "airport_iata": "RGN"},

    # ---------------- EAST ASIA ----------------
    "tokyo": {"canonical": "Tokyo", "lookup": "Tokyo", "country": "Japan", "country_code": "JP", "airport_iata": "HND"},
    "osaka": {"canonical": "Osaka", "lookup": "Osaka", "country": "Japan", "country_code": "JP", "airport_iata": "KIX"},
    "kyoto": {"canonical": "Kyoto", "lookup": "Kyoto", "country": "Japan", "country_code": "JP", "airport_iata": "KIX"},
    "seoul": {"canonical": "Seoul", "lookup": "Seoul", "country": "South Korea", "country_code": "KR", "airport_iata": "ICN"},
    "hong kong": {"canonical": "Hong Kong", "lookup": "Hong Kong", "country": "Hong Kong", "country_code": "HK", "airport_iata": "HKG"},
    "beijing": {"canonical": "Beijing", "lookup": "Beijing", "country": "China", "country_code": "CN", "airport_iata": "PEK"},
    "shanghai": {"canonical": "Shanghai", "lookup": "Shanghai", "country": "China", "country_code": "CN", "airport_iata": "PVG"},
    "taipei": {"canonical": "Taipei", "lookup": "Taipei", "country": "Taiwan", "country_code": "TW", "airport_iata": "TPE"},

    # ---------------- SOUTH ASIA ----------------
    "maldives": {"canonical": "Maldives", "lookup": "Malé", "country": "Maldives", "country_code": "MV", "airport_iata": "MLE"},
    "male": {"canonical": "Malé", "lookup": "Malé", "country": "Maldives", "country_code": "MV", "airport_iata": "MLE"},
    "kathmandu": {"canonical": "Kathmandu", "lookup": "Kathmandu", "country": "Nepal", "country_code": "NP", "airport_iata": "KTM"},
    "colombo": {"canonical": "Colombo", "lookup": "Colombo", "country": "Sri Lanka", "country_code": "LK", "airport_iata": "CMB"},
    "dhaka": {"canonical": "Dhaka", "lookup": "Dhaka", "country": "Bangladesh", "country_code": "BD", "airport_iata": "DAC"},

    # ---------------- EUROPE ----------------
    "london": {"canonical": "London", "lookup": "London", "country": "United Kingdom", "country_code": "GB", "airport_iata": "LHR"},
    "paris": {"canonical": "Paris", "lookup": "Paris", "country": "France", "country_code": "FR", "airport_iata": "CDG"},
    "rome": {"canonical": "Rome", "lookup": "Rome", "country": "Italy", "country_code": "IT", "airport_iata": "FCO"},
    "milan": {"canonical": "Milan", "lookup": "Milan", "country": "Italy", "country_code": "IT", "airport_iata": "MXP"},
    "amsterdam": {"canonical": "Amsterdam", "lookup": "Amsterdam", "country": "Netherlands", "country_code": "NL", "airport_iata": "AMS"},
    "frankfurt": {"canonical": "Frankfurt", "lookup": "Frankfurt", "country": "Germany", "country_code": "DE", "airport_iata": "FRA"},
    "munich": {"canonical": "Munich", "lookup": "Munich", "country": "Germany", "country_code": "DE", "airport_iata": "MUC"},
    "zurich": {"canonical": "Zurich", "lookup": "Zurich", "country": "Switzerland", "country_code": "CH", "airport_iata": "ZRH"},
    "geneva": {"canonical": "Geneva", "lookup": "Geneva", "country": "Switzerland", "country_code": "CH", "airport_iata": "GVA"},
    "vienna": {"canonical": "Vienna", "lookup": "Vienna", "country": "Austria", "country_code": "AT", "airport_iata": "VIE"},
    "madrid": {"canonical": "Madrid", "lookup": "Madrid", "country": "Spain", "country_code": "ES", "airport_iata": "MAD"},
    "barcelona": {"canonical": "Barcelona", "lookup": "Barcelona", "country": "Spain", "country_code": "ES", "airport_iata": "BCN"},
    "lisbon": {"canonical": "Lisbon", "lookup": "Lisbon", "country": "Portugal", "country_code": "PT", "airport_iata": "LIS"},
    "athens": {"canonical": "Athens", "lookup": "Athens", "country": "Greece", "country_code": "GR", "airport_iata": "ATH"},
    "prague": {"canonical": "Prague", "lookup": "Prague", "country": "Czechia", "country_code": "CZ", "airport_iata": "PRG"},
    "copenhagen": {"canonical": "Copenhagen", "lookup": "Copenhagen", "country": "Denmark", "country_code": "DK", "airport_iata": "CPH"},
    "stockholm": {"canonical": "Stockholm", "lookup": "Stockholm", "country": "Sweden", "country_code": "SE", "airport_iata": "ARN"},
    "oslo": {"canonical": "Oslo", "lookup": "Oslo", "country": "Norway", "country_code": "NO", "airport_iata": "OSL"},
    "helsinki": {"canonical": "Helsinki", "lookup": "Helsinki", "country": "Finland", "country_code": "FI", "airport_iata": "HEL"},
    "dublin": {"canonical": "Dublin", "lookup": "Dublin", "country": "Ireland", "country_code": "IE", "airport_iata": "DUB"},
    "brussels": {"canonical": "Brussels", "lookup": "Brussels", "country": "Belgium", "country_code": "BE", "airport_iata": "BRU"},
    "budapest": {"canonical": "Budapest", "lookup": "Budapest", "country": "Hungary", "country_code": "HU", "airport_iata": "BUD"},
    "warsaw": {"canonical": "Warsaw", "lookup": "Warsaw", "country": "Poland", "country_code": "PL", "airport_iata": "WAW"},
    "reykjavik": {"canonical": "Reykjavik", "lookup": "Reykjavik", "country": "Iceland", "country_code": "IS", "airport_iata": "KEF"},

    # ---------------- AFRICA ----------------
    "cairo": {"canonical": "Cairo", "lookup": "Cairo", "country": "Egypt", "country_code": "EG", "airport_iata": "CAI"},
    "luxor": {"canonical": "Luxor", "lookup": "Luxor", "country": "Egypt", "country_code": "EG", "airport_iata": "LXR"},
    "sharm el sheikh": {"canonical": "Sharm El Sheikh", "lookup": "Sharm El Sheikh", "country": "Egypt", "country_code": "EG", "airport_iata": "SSH"},
    "marrakech": {"canonical": "Marrakech", "lookup": "Marrakech", "country": "Morocco", "country_code": "MA", "airport_iata": "RAK"},
    "casablanca": {"canonical": "Casablanca", "lookup": "Casablanca", "country": "Morocco", "country_code": "MA", "airport_iata": "CMN"},
    "cape town": {"canonical": "Cape Town", "lookup": "Cape Town", "country": "South Africa", "country_code": "ZA", "airport_iata": "CPT"},
    "johannesburg": {"canonical": "Johannesburg", "lookup": "Johannesburg", "country": "South Africa", "country_code": "ZA", "airport_iata": "JNB"},
    "durban": {"canonical": "Durban", "lookup": "Durban", "country": "South Africa", "country_code": "ZA", "airport_iata": "DUR"},
    "nairobi": {"canonical": "Nairobi", "lookup": "Nairobi", "country": "Kenya", "country_code": "KE", "airport_iata": "NBO"},
    "mombasa": {"canonical": "Mombasa", "lookup": "Mombasa", "country": "Kenya", "country_code": "KE", "airport_iata": "MBA"},
    "zanzibar": {"canonical": "Zanzibar", "lookup": "Zanzibar City", "country": "Tanzania", "country_code": "TZ", "airport_iata": "ZNZ"},
    "dar es salaam": {"canonical": "Dar es Salaam", "lookup": "Dar es Salaam", "country": "Tanzania", "country_code": "TZ", "airport_iata": "DAR"},
    "arusha": {"canonical": "Arusha", "lookup": "Arusha", "country": "Tanzania", "country_code": "TZ", "airport_iata": "ARK"},
    "kilimanjaro": {"canonical": "Kilimanjaro", "lookup": "Kilimanjaro", "country": "Tanzania", "country_code": "TZ", "airport_iata": "JRO"},
    "serengeti": {"canonical": "Serengeti", "lookup": "Serengeti", "country": "Tanzania", "country_code": "TZ", "airport_iata": "JRO"},
    "victoria falls": {"canonical": "Victoria Falls", "lookup": "Victoria Falls", "country": "Zimbabwe", "country_code": "ZW", "airport_iata": "VFA"},
    "livingstone": {"canonical": "Livingstone", "lookup": "Livingstone", "country": "Zambia", "country_code": "ZM", "airport_iata": "LVI"},
    "mauritius": {"canonical": "Mauritius", "lookup": "Port Louis", "country": "Mauritius", "country_code": "MU", "airport_iata": "MRU"},
    "seychelles": {"canonical": "Seychelles", "lookup": "Victoria", "country": "Seychelles", "country_code": "SC", "airport_iata": "SEZ"},
    "victoria seychelles": {"canonical": "Victoria", "lookup": "Victoria", "country": "Seychelles", "country_code": "SC", "airport_iata": "SEZ"},
    "addis ababa": {"canonical": "Addis Ababa", "lookup": "Addis Ababa", "country": "Ethiopia", "country_code": "ET", "airport_iata": "ADD"},
    "accra": {"canonical": "Accra", "lookup": "Accra", "country": "Ghana", "country_code": "GH", "airport_iata": "ACC"},
    "lagos": {"canonical": "Lagos", "lookup": "Lagos", "country": "Nigeria", "country_code": "NG", "airport_iata": "LOS"},
    "abuja": {"canonical": "Abuja", "lookup": "Abuja", "country": "Nigeria", "country_code": "NG", "airport_iata": "ABV"},
    "dakar": {"canonical": "Dakar", "lookup": "Dakar", "country": "Senegal", "country_code": "SN", "airport_iata": "DSS"},
    "tunis": {"canonical": "Tunis", "lookup": "Tunis", "country": "Tunisia", "country_code": "TN", "airport_iata": "TUN"},
    "algiers": {"canonical": "Algiers", "lookup": "Algiers", "country": "Algeria", "country_code": "DZ", "airport_iata": "ALG"},
    "kigali": {"canonical": "Kigali", "lookup": "Kigali", "country": "Rwanda", "country_code": "RW", "airport_iata": "KGL"},
    "kampala": {"canonical": "Kampala", "lookup": "Kampala", "country": "Uganda", "country_code": "UG", "airport_iata": "EBB"},
    "windhoek": {"canonical": "Windhoek", "lookup": "Windhoek", "country": "Namibia", "country_code": "NA", "airport_iata": "WDH"},
    "gaborone": {"canonical": "Gaborone", "lookup": "Gaborone", "country": "Botswana", "country_code": "BW", "airport_iata": "GBE"},
    "maputo": {"canonical": "Maputo", "lookup": "Maputo", "country": "Mozambique", "country_code": "MZ", "airport_iata": "MPM"},
    "cape verde": {"canonical": "Cape Verde", "lookup": "Praia", "country": "Cabo Verde", "country_code": "CV", "airport_iata": "RAI"},

    # ---------------- NORTH AMERICA ----------------
    "new york": {"canonical": "New York", "lookup": "New York", "country": "United States", "country_code": "US", "airport_iata": "JFK"},
    "los angeles": {"canonical": "Los Angeles", "lookup": "Los Angeles", "country": "United States", "country_code": "US", "airport_iata": "LAX"},
    "san francisco": {"canonical": "San Francisco", "lookup": "San Francisco", "country": "United States", "country_code": "US", "airport_iata": "SFO"},
    "chicago": {"canonical": "Chicago", "lookup": "Chicago", "country": "United States", "country_code": "US", "airport_iata": "ORD"},
    "miami": {"canonical": "Miami", "lookup": "Miami", "country": "United States", "country_code": "US", "airport_iata": "MIA"},
    "las vegas": {"canonical": "Las Vegas", "lookup": "Las Vegas", "country": "United States", "country_code": "US", "airport_iata": "LAS"},
    "washington dc": {"canonical": "Washington, D.C.", "lookup": "Washington", "country": "United States", "country_code": "US", "airport_iata": "IAD"},
    "toronto": {"canonical": "Toronto", "lookup": "Toronto", "country": "Canada", "country_code": "CA", "airport_iata": "YYZ"},
    "vancouver": {"canonical": "Vancouver", "lookup": "Vancouver", "country": "Canada", "country_code": "CA", "airport_iata": "YVR"},
    "montreal": {"canonical": "Montreal", "lookup": "Montreal", "country": "Canada", "country_code": "CA", "airport_iata": "YUL"},
    "mexico city": {"canonical": "Mexico City", "lookup": "Mexico City", "country": "Mexico", "country_code": "MX", "airport_iata": "MEX"},

    # ---------------- SOUTH AMERICA ----------------
    "rio de janeiro": {"canonical": "Rio de Janeiro", "lookup": "Rio de Janeiro", "country": "Brazil", "country_code": "BR", "airport_iata": "GIG"},
    "sao paulo": {"canonical": "São Paulo", "lookup": "São Paulo", "country": "Brazil", "country_code": "BR", "airport_iata": "GRU"},
    "buenos aires": {"canonical": "Buenos Aires", "lookup": "Buenos Aires", "country": "Argentina", "country_code": "AR", "airport_iata": "EZE"},
    "lima": {"canonical": "Lima", "lookup": "Lima", "country": "Peru", "country_code": "PE", "airport_iata": "LIM"},
    "santiago": {"canonical": "Santiago", "lookup": "Santiago", "country": "Chile", "country_code": "CL", "airport_iata": "SCL"},

    # ---------------- AUSTRALIA / NEW ZEALAND ----------------
    "sydney": {"canonical": "Sydney", "lookup": "Sydney", "country": "Australia", "country_code": "AU", "airport_iata": "SYD"},
    "melbourne": {"canonical": "Melbourne", "lookup": "Melbourne", "country": "Australia", "country_code": "AU", "airport_iata": "MEL"},
    "brisbane": {"canonical": "Brisbane", "lookup": "Brisbane", "country": "Australia", "country_code": "AU", "airport_iata": "BNE"},
    "perth": {"canonical": "Perth", "lookup": "Perth", "country": "Australia", "country_code": "AU", "airport_iata": "PER"},
    "auckland": {"canonical": "Auckland", "lookup": "Auckland", "country": "New Zealand", "country_code": "NZ", "airport_iata": "AKL"},
    "queenstown": {"canonical": "Queenstown", "lookup": "Queenstown", "country": "New Zealand", "country_code": "NZ", "airport_iata": "ZQN"},
}

# ============================================================
# LIVE DATA TOOL LAYER
# ============================================================

import os
import re
from datetime import date, timedelta
from urllib.parse import urlencode

import requests

REQUEST_TIMEOUT = 12


def _request_json(url, params=None, headers=None):
    """Safe JSON GET helper. Returns (payload, error_message)."""
    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as exc:
        return None, f"Live data request failed: {exc}"
    except ValueError:
        return None, "Live data service returned an invalid response."


def get_destination_data(destination):
    """Return the old local catalog only for backward-compatible internal tests."""
    if not destination:
        return None
    return DESTINATIONS.get(destination.lower().strip())


COUNTRY_DEFAULT_DESTINATIONS = {
    "saudi arabia": "riyadh",
    "united arab emirates": "dubai",
    "uae": "dubai",
    "qatar": "doha",
    "oman": "muscat",
    "japan": "tokyo",
    "france": "paris",
    "italy": "rome",
    "spain": "madrid",
    "germany": "frankfurt",
    "netherlands": "amsterdam",
    "switzerland": "zurich",
    "united kingdom": "london",
    "uk": "london",
    "united states": "new york",
    "usa": "new york",
    "canada": "toronto",
    "australia": "sydney",
    "new zealand": "auckland",
    "singapore": "singapore",
    "malaysia": "kuala lumpur",
    "thailand": "bangkok",
    "indonesia": "bali",
    "philippines": "manila",
    "vietnam": "hanoi",
    "south korea": "seoul",
    "china": "beijing",
    "nepal": "kathmandu",
    "sri lanka": "colombo",
    "maldives": "male",
    "bangladesh": "dhaka",
    "egypt": "cairo",
    "morocco": "marrakech",
    "south africa": "cape town",
    "kenya": "nairobi",
    "tanzania": "dar es salaam",
    "zimbabwe": "victoria falls",
    "zambia": "livingstone",
    "nigeria": "lagos",
    "ghana": "accra",
    "rwanda": "kigali",
    "uganda": "kampala",
    "ethiopia": "addis ababa",
    "brazil": "rio de janeiro",
    "mexico": "mexico city",
    "argentina": "buenos aires",
    "turkey": "istanbul",
    "greece": "athens",
    "portugal": "lisbon",
    "austria": "vienna",
    "ireland": "dublin",
    "india": "delhi",
}

def geocode_destination(destination):
    """Resolve a travel destination to a verified place and country.

    This resolver is intentionally defensive because place names can be
    ambiguous. For known Indian travel destinations, Open-Meteo is queried
    with the documented ``countryCode=IN`` filter and the response is checked
    again locally. If the service still returns a non-Indian result, that
    result is rejected instead of silently showing the wrong country.

    For arbitrary destinations, the search remains global. Explicit country
    qualifiers such as ``Goa, India`` or ``Genoa, Italy`` are respected.
    """
    if not destination or len(destination.strip()) < 2:
        return None, "Please enter a destination with at least two characters."

    query = re.sub(r"\s+", " ", destination.strip()).strip(" ,")
    normalized = query.lower()

    # Country-level requests are valid travel requests too. Resolve them to a
    # representative planning city while preserving the country as the public
    # destination label. This prevents broad inputs such as "Saudi Arabia" from
    # being sent to an unrelated geocoder result.
    country_default_key = COUNTRY_DEFAULT_DESTINATIONS.get(normalized)
    country_query_name = None
    if country_default_key:
        country_query_name = query

    # Common user aliases. The expanded airport-aware catalog below is
    # consulted first, while the original catalog remains untouched.
    aliases = {
        "bangalore": "bengaluru",
        "mysore": "mysuru",
        "puducherry": "pondicherry",
        "kodagu": "coorg",
    }

    # Expanded airport-aware destinations are used to make common travel
    # regions/cities deterministic. The original DESTINATIONS catalog is
    # intentionally preserved for backward compatibility.
    airport_key = re.sub(r"\s+", " ", query.lower()).strip(" ,")
    if country_default_key:
        airport_key = country_default_key
    airport_entry = AIRPORT_DESTINATIONS.get(airport_key)

    # Also support explicit country qualifiers, e.g. "Goa, India".
    # Never let an airport alias override a conflicting country qualifier.
    explicit_country_name = None
    if "," in query:
        raw_parts = [part.strip() for part in query.split(",") if part.strip()]
        if len(raw_parts) >= 2:
            explicit_country_name = raw_parts[-1].lower()
            airport_entry = AIRPORT_DESTINATIONS.get(raw_parts[0].lower())

            if airport_entry:
                country_alias_to_code = {
                    "india": "IN", "italy": "IT", "france": "FR",
                    "philippines": "PH", "japan": "JP", "indonesia": "ID", "thailand": "TH",
                    "singapore": "SG", "maldives": "MV", "nepal": "NP",
                    "sri lanka": "LK", "bangladesh": "BD", "uae": "AE",
                    "united arab emirates": "AE", "qatar": "QA",
                    "oman": "OM", "saudi arabia": "SA", "united kingdom": "GB",
                    "uk": "GB", "united states": "US", "usa": "US",
                    "canada": "CA", "australia": "AU", "germany": "DE",
                    "spain": "ES", "netherlands": "NL", "switzerland": "CH",
                    "south africa": "ZA", "tanzania": "TZ", "kenya": "KE",
                    "zimbabwe": "ZW", "zambia": "ZM", "egypt": "EG",
                    "morocco": "MA", "nigeria": "NG", "ghana": "GH",
                    "rwanda": "RW", "uganda": "UG", "ethiopia": "ET",
                }
                requested_code = country_alias_to_code.get(explicit_country_name)
                if requested_code and requested_code != airport_entry["country_code"]:
                    airport_entry = None

    if airport_entry:
        lookup_name = airport_entry["lookup"]
        lookup_country = airport_entry["country_code"]
        payload, error = _request_json(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": lookup_name,
                "count": 10,
                "language": "en",
                "format": "json",
                "countryCode": lookup_country,
            },
        )
        if error:
            # Deterministic fallback: a temporary geocoding outage must not break
            # destination resolution. Country/airport identity remains verified
            # by the airport-aware catalog; weather simply remains unavailable
            # until coordinates can be obtained.
            return {
                "name": country_query_name or airport_entry["canonical"],
                "country": airport_entry["country"],
                "country_code": airport_entry["country_code"],
                "admin1": "",
                "latitude": None,
                "longitude": None,
                "timezone": "",
                "population": None,
                "airport_iata": airport_entry["airport_iata"],
                "airport_search_name": airport_entry["lookup"],
                "representative_place": airport_entry["lookup"],
                "planning_city": airport_entry["lookup"],
                "resolution_source": "country-to-representative-city" if country_query_name else "airport-aware local catalog",
            }, None

        matches = payload.get("results") or []
        matches = [
            item for item in matches
            if str(item.get("country_code", "")).upper() == lookup_country
        ]
        if not matches:
            return None, (
                f"We could not confidently resolve '{destination}' to "
                f"{airport_entry['country']}."
            )

        target = lookup_name.lower()
        preferred = next(
            (item for item in matches if str(item.get("name", "")).strip().lower() == target),
            matches[0],
        )

        # Keep the user's intended destination name while using the mapped
        # airport/representative city for downstream travel tools.
        return {
            "name": country_query_name or airport_entry["canonical"],
            "country": airport_entry["country"],
            "country_code": airport_entry["country_code"],
            "admin1": preferred.get("admin1", ""),
            "latitude": preferred.get("latitude"),
            "longitude": preferred.get("longitude"),
            "timezone": preferred.get("timezone", ""),
            "population": preferred.get("population"),
            "airport_iata": airport_entry["airport_iata"],
            "airport_search_name": airport_entry["lookup"],
            "representative_place": preferred.get("name", airport_entry["lookup"]),
            "planning_city": preferred.get("name", airport_entry["lookup"]),
            "resolution_source": "country-to-representative-city" if country_query_name else "airport-aware local catalog",
        }, None

    # Original catalog remains available for backward-compatible behavior.
    indian_catalog_keys = set(DESTINATIONS.keys()) | {k for k, v in AIRPORT_DESTINATIONS.items() if v.get("country_code") == "IN"}

    # If the user explicitly supplies a country, respect it. This prevents a
    # rule for a known Indian place from overriding an intentional query such
    # as "Goa, Philippines".
    explicit_country = None
    place_part = query
    if "," in query:
        parts = [part.strip() for part in query.split(",") if part.strip()]
        if len(parts) >= 2:
            place_part = parts[0]
            explicit_country = parts[-1].lower()

    # A small ISO map handles common explicit country qualifiers. The query
    # still remains fully global when the country is not in this map.
    country_aliases = {
        "india": "IN",
        "italy": "IT",
        "philippines": "PH",
        "japan": "JP",
        "france": "FR",
        "united states": "US",
        "usa": "US",
        "united kingdom": "GB",
        "uk": "GB",
        "england": "GB",
        "uae": "AE",
        "united arab emirates": "AE",
        "singapore": "SG",
        "indonesia": "ID",
        "switzerland": "CH",
        "thailand": "TH",
        "australia": "AU",
        "canada": "CA",
        "germany": "DE",
        "spain": "ES",
        "netherlands": "NL",
    }

    country_names = {
        "IN": "India", "IT": "Italy", "PH": "Philippines", "JP": "Japan",
        "FR": "France", "US": "United States", "GB": "United Kingdom",
        "AE": "United Arab Emirates", "SG": "Singapore", "ID": "Indonesia",
        "CH": "Switzerland", "TH": "Thailand", "AU": "Australia",
        "CA": "Canada", "DE": "Germany", "ES": "Spain", "NL": "Netherlands",
        "QA": "Qatar", "OM": "Oman", "SA": "Saudi Arabia", "TZ": "Tanzania",
        "KE": "Kenya", "ZW": "Zimbabwe", "ZM": "Zambia", "ZA": "South Africa",
        "EG": "Egypt", "MA": "Morocco", "NG": "Nigeria", "GH": "Ghana",
        "RW": "Rwanda", "UG": "Uganda", "ET": "Ethiopia", "MV": "Maldives",
        "NP": "Nepal", "LK": "Sri Lanka", "BD": "Bangladesh",
    }

    place_normalized = place_part.lower()
    canonical_name = aliases.get(place_normalized, place_normalized)
    explicit_country_code = country_aliases.get(explicit_country) if explicit_country else None
    known_indian = canonical_name in indian_catalog_keys and explicit_country is None

    # Open-Meteo documents the parameter as countryCode (camelCase), NOT
    # country_code. The latter was the reason the previous attempted fix did
    # not actually filter Goa to India.
    country_code = explicit_country_code or ("IN" if known_indian else None)

    search_name = aliases.get(place_normalized, place_part)
    params = {
        "name": search_name,
        "count": 20 if known_indian else 10,
        "language": "en",
        "format": "json",
    }
    if country_code:
        params["countryCode"] = country_code

    payload, error = _request_json(
        "https://geocoding-api.open-meteo.com/v1/search",
        params=params,
    )

    if error:
        return None, error

    matches = payload.get("results") or []

    # Always normalize country codes before selecting a result.
    normalized_matches = []
    for item in matches:
        item = dict(item)
        item["_country_code"] = str(item.get("country_code", "")).upper()
        item["_name"] = str(item.get("name", "")).strip().lower()
        normalized_matches.append(item)

    # Hard safety check whenever a country constraint was established. Never
    # display a result from another country just because it ranked first.
    if country_code:
        normalized_matches = [
            item for item in normalized_matches
            if item.get("_country_code") == country_code
        ]
        if not normalized_matches:
            country_label = explicit_country or "India"
            return None, (
                f"We could not confidently resolve '{destination}' to {country_label}. "
                "Please check the destination and country name."
            )

        # When the user explicitly names a country, also validate the returned
        # country label when we have a canonical label for that ISO code.
        if explicit_country_code and explicit_country_code in country_names:
            expected_country = country_names[explicit_country_code].lower()
            country_matches = [
                item for item in normalized_matches
                if str(item.get("country", "")).strip().lower() == expected_country
            ]
            if country_matches:
                normalized_matches = country_matches
            else:
                return None, (
                    f"We could not confidently resolve '{destination}' to "
                    f"{explicit_country}. Please check the destination and country name."
                )

    if not normalized_matches:
        return None, f"We could not locate '{destination}'. Please check the spelling."

    # Prefer an exact place-name match.
    target_name = canonical_name
    exact = next(
        (item for item in normalized_matches if item.get("_name") == target_name),
        None,
    )

    # For an alias, also accept the original user spelling if the API returned
    # it exactly (for example, "Bangalore").
    if exact is None:
        exact = next(
            (item for item in normalized_matches if item.get("_name") == normalized),
            None,
        )

    if exact is not None:
        preferred = exact
    else:
        # Prefer populated-place feature codes over a random administrative
        # or similarly named result.
        preferred = next(
            (
                item for item in normalized_matches
                if str(item.get("feature_code", "")).upper()
                in {"PPLC", "PPLA", "PPLA2", "PPLA3", "PPLA4"}
            ),
            normalized_matches[0],
        )

    # Final invariant: when a country was requested or inferred, the returned
    # location MUST have that same country code. This makes a wrong-country
    # result impossible even if an upstream ranking changes later.
    if country_code and preferred.get("_country_code") != country_code:
        country_label = explicit_country or "India"
        return None, (
            f"We could not confidently resolve '{destination}' to {country_label}. "
            "Please check the destination and country name."
        )

    return {
        "name": preferred.get("name", query),
        "country": preferred.get("country", ""),
        "country_code": preferred.get("_country_code", ""),
        "admin1": preferred.get("admin1", ""),
        "latitude": preferred.get("latitude"),
        "longitude": preferred.get("longitude"),
        "timezone": preferred.get("timezone", ""),
        "population": preferred.get("population"),
    }, None

def _today_and_checkout(nights):
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=max(1, int(nights or 1)))
    return check_in.isoformat(), check_out.isoformat()



# Local fallback planning data. These are not live inventory or booking availability.
LOCAL_FOOD = {'agra': ['Petha', 'Mughlai cuisine', 'Bedai-Jalebi', 'Dalmoth'],
 'amritsar': ['Amritsari Kulcha', 'Chole', 'Lassi', 'Tandoori Chicken'],
 'bali': ['Nasi Goreng', 'Mie Goreng', 'Satay', 'Babi Guling'],
 'bengaluru': ['Bisi Bele Bath', 'Masala Dosa', 'Mysore Pak', 'Ragi Mudde'],
 'cape town': ['Bobotie', 'Cape Malay curry', 'Braai', 'Malva pudding'],
 'coorg': ['Pandi Curry', 'Kadambuttu', 'Coorg-style pork dishes', 'Filter coffee'],
 'darjeeling': ['Momos', 'Thukpa', 'Darjeeling tea', 'Tibetan noodles'],
 'delhi': ['Chole Bhature', 'Butter Chicken', 'Paratha', 'Chaat'],
 'dubai': ['Shawarma', 'Machboos', 'Hummus', 'Luqaimat'],
 'goa': ['Goan Fish Curry', 'Prawn Balchão', 'Bebinca', 'Pav Bhaji'],
 'hyderabad': ['Hyderabadi Biryani', 'Haleem', 'Mirchi Ka Salan', 'Qubani Ka Meetha'],
 'jaipur': ['Dal Baati Churma', 'Pyaaz Kachori', 'Ghevar', 'Laal Maas'],
 'kerala': ['Appam with Stew', 'Kerala Sadya', 'Puttu & Kadala Curry', 'Karimeen Pollichathu'],
 'kochi': ['Appam with Stew', 'Kerala Sadya', 'Karimeen Pollichathu', 'Puttu & Kadala Curry'],
 'manali': ['Siddu', 'Trout Curry', 'Thukpa', 'Momos'],
 'mumbai': ['Vada Pav', 'Pav Bhaji', 'Bombay Sandwich', 'Misal Pav'],
 'munnar': ['Appam with Stew', 'Puttu & Kadala Curry', 'Kerala Sadya', 'Tea and local snacks'],
 'mysuru': ['Mysore Masala Dosa', 'Mysore Pak', 'Ragi Mudde', 'Maddur Vada'],
 'new york': ['New York-style pizza', 'Bagel with cream cheese', 'Pastrami sandwich', 'Cheesecake'],
 'ooty': ['Ooty Varkey', 'Homemade chocolates', 'Nilgiri tea', 'South Indian thali'],
 'paris': ['Croissant', 'Crêpe', 'French onion soup', 'Ratatouille'],
 'pondicherry': ['Creole seafood', 'Dosa', 'French pastries', 'South Indian thali'],
 'saudi arabia': ['Kabsa', 'Jareesh', 'Mutabbaq', 'Saudi dates'],
 'riyadh': ['Kabsa', 'Jareesh', 'Mutabbaq', 'Saudi dates'],
 'rishikesh': ['Aloo Puri', 'Kumaoni-style dishes', 'Chole Bhature', 'Lassi'],
 'serengeti': ['Nyama Choma', 'Ugali', 'Pilau', 'Tanzanian chapati'],
 'tokyo': ['Sushi', 'Ramen', 'Tempura', 'Okonomiyaki'],
 'udaipur': ['Dal Baati Churma', 'Gatte Ki Sabzi', 'Mewari Thali', 'Jalebi'],
 'varanasi': ['Kachori Sabzi', 'Banarasi Tamatar Chaat', 'Lassi', 'Banarasi Paan'],
 'victoria falls': ['Sadza', 'Bream fish', 'Nyama', 'Local maize dishes']}

LOCAL_REGION_KEYS = {
    "kerala": ["kochi", "munnar"],
    "karnataka": ["bengaluru", "mysuru", "coorg"],
    "rajasthan": ["jaipur", "udaipur"],
    "tamil nadu": ["ooty"],
}

LOCAL_ATTRACTIONS = {'riyadh': [('Diriyah', 'Explore the historic At-Turaif area and heritage district.'), ('Kingdom Centre', 'See Riyadh from the Kingdom Centre Sky Bridge area, subject to opening hours.'), ('Al Masmak Palace', "Visit the historic fortress and learn about Riyadh's heritage."), ('National Museum of Saudi Arabia', 'Explore Saudi history, culture and archaeology.'), ('Boulevard City', 'Explore a major entertainment and dining district; check current hours.'), ('Riyadh Park', 'Use the leisure and shopping area for relaxed time.'), ('Riyadh local market', 'Browse a suitable local market after checking opening hours.')], 'bali': [('Ubud', 'Explore rice terraces, art spaces and the cultural heart of Bali.'),
          ('Tegallalang Rice Terraces', 'Walk through the famous terraced landscape.'),
          ('Uluwatu Temple', 'Visit the cliffside temple and coastal viewpoints.'),
          ('Seminyak', 'Explore the beachside neighbourhood, cafes and evening atmosphere.'),
          ('Nusa Dua', 'Enjoy a relaxed beach and coastal day.'),
          ('Mount Batur', 'Consider a sunrise mountain experience if conditions permit.')],
 'bengaluru': [('Bengaluru Palace', 'Explore the historic palace and grounds.'),
               ('Lalbagh Botanical Garden', 'Walk through the botanical gardens.'),
               ('Cubbon Park', 'Enjoy a relaxed city-centre park walk.'),
               ('Vidhana Soudha', 'See the landmark government building from outside.'),
               ('Church Street', 'Explore cafes, bookstores and evening city life.')],
 'cape town': [('Table Mountain', "Take in the city's signature mountain and skyline views."),
               ('V&A Waterfront', 'Explore the waterfront, food and harbour area.'),
               ('Bo-Kaap', 'Walk through the colourful historic neighbourhood.'),
               ('Camps Bay', 'Enjoy the coastal scenery and beach atmosphere.'),
               ('Kirstenbosch', 'Explore the botanical garden at the foot of Table Mountain.'),
               ('Cape Point', 'Take a scenic excursion along the peninsula.')],
 'delhi': [('India Gate', 'Visit the landmark and surrounding central Delhi area.'),
           ("Humayun's Tomb", 'Explore the Mughal-era garden tomb complex.'),
           ('Qutub Minar', 'Visit the historic monument complex.'),
           ('Red Fort', 'Explore the historic fort and Old Delhi surroundings.'),
           ('Chandni Chowk', 'Explore Old Delhi food and market lanes.'),
           ('Lotus Temple', 'Visit the distinctive modern temple and gardens.')],
 'dubai': [('Burj Khalifa', "Visit Dubai's landmark tower and downtown area."),
           ('Dubai Marina', 'Explore the waterfront promenade and skyline.'),
           ('Al Fahidi Historical District', 'See an older side of Dubai through heritage lanes.'),
           ('Jumeirah Beach', 'Relax by the coast and enjoy the city skyline.'),
           ('Dubai Mall', "Explore one of the city's major shopping and entertainment areas."),
           ('Desert experience', 'Consider a desert activity with current weather and operator conditions checked.')],
 'goa': [('Baga Beach', 'Relax by the beach and explore the surrounding shoreline.'),
         ('Fort Aguada', 'Explore the historic fort and coastal viewpoints.'),
         ('Calangute Beach', "Spend time along one of North Goa's popular beaches."),
         ('Anjuna', 'Explore the coastal area and local market scene.'),
         ('Panaji & Fontainhas', "Walk through Panaji's colourful Latin Quarter."),
         ('Basilica of Bom Jesus', 'Visit the historic Old Goa church complex.')],
 'jaipur': [('Amber Fort', 'Explore the hilltop fort and its courtyards.'),
            ('City Palace', "Visit Jaipur's historic royal complex."),
            ('Hawa Mahal', 'See the iconic facade and explore the old-city lanes.'),
            ('Jantar Mantar', 'Explore the historic astronomical instruments.'),
            ('Johari Bazaar', 'Browse traditional jewellery, textiles and local crafts.'),
            ('Nahargarh Fort', 'Enjoy elevated views over Jaipur around sunset.')],
 'kashmir': [('Dal Lake & Shikara Ride', "Lake experience and Srinagar's waterfront."),
             ('Mughal Gardens', 'Visit Nishat or Shalimar Gardens for landscaped views.'),
             ('Srinagar Old City', 'Explore local markets, crafts and historic neighbourhoods.'),
             ('Gulmarg', 'Mountain day trip with scenic views and optional cable-car activities.'),
             ('Pahalgam', 'Valley scenery, riverside walks and a relaxed mountain day.'),
             ('Hazratbal Shrine', 'Visit a major Srinagar landmark and the nearby lakefront.'),
             ('Pari Mahal', 'Hilltop viewpoint overlooking Srinagar and Dal Lake.'),
             ('Lal Chowk', 'Central market area for local shopping and city atmosphere.')],
 'kerala': [('Fort Kochi', 'Explore the historic waterfront, heritage streets and Chinese fishing nets.'),
            ('Alappuzha Backwaters', "Enjoy Kerala's backwater scenery and a relaxed waterfront experience."),
            ('Munnar Tea Gardens', 'Take in tea-covered hills and scenic viewpoints around Munnar.'),
            ('Mattancherry Palace', "Explore Kerala's heritage and historic neighbourhoods."),
            ('Varkala Cliff', 'Enjoy the coastal cliff views and sunset atmosphere.'),
            ('Kerala local cuisine', 'Try a Kerala-style meal and local snacks.')],
 'kochi': [('Fort Kochi', 'Walk through the historic waterfront neighbourhood.'),
           ('Chinese Fishing Nets', 'See the iconic waterfront fishing structures.'),
           ('Mattancherry Palace', 'Explore the historic palace and nearby heritage area.'),
           ('Jew Town', 'Browse heritage streets and local shops.'),
           ('Marine Drive', 'Enjoy a relaxed waterfront evening.')],
 'manali': [('Old Manali', 'Walk through the village lanes, cafes and local shops.'),
            ('Hadimba Temple', 'Visit the cedar-forest temple and surrounding area.'),
            ('Solang Valley', 'Enjoy mountain scenery and seasonal adventure activities.'),
            ('Vashisht', 'Explore the village, temple area and hot-spring surroundings.'),
            ('Mall Road', 'Evening stroll for food and local shopping.'),
            ('Sissu', 'Take a scenic mountain excursion through the valley.')],
 'mumbai': [('Gateway of India', 'Start with the waterfront landmark and Colaba area.'),
            ('Colaba Causeway', 'Explore local shopping and street-side browsing.'),
            ('Marine Drive', 'Take an evening walk along the sea-facing promenade.'),
            ('Chhatrapati Shivaji Maharaj Terminus', 'See the historic railway architecture.'),
            ('Elephanta Caves', 'Take a ferry excursion to the historic cave complex.'),
            ('Bandra Bandstand', 'Relax by the coast and explore the nearby neighbourhood.')],
 'new york': [('Central Park', "Explore the city's major urban park."),
              ('Times Square', 'Experience the bright central entertainment district.'),
              ('Statue of Liberty', 'Visit the harbor landmark if tickets and schedules allow.'),
              ('Brooklyn Bridge', 'Walk across the bridge for skyline views.'),
              ('The Metropolitan Museum of Art', 'Explore a major art collection.'),
              ('SoHo', 'Walk through the historic shopping and gallery district.')],
 'paris': [('Eiffel Tower', 'Visit the iconic landmark and surrounding Seine area.'),
           ('Louvre Museum', "Explore one of the world's major art museums."),
           ('Montmartre', 'Walk the artistic neighbourhood and Sacré-Cœur area.'),
           ('Seine River', 'Enjoy a scenic riverside walk or cruise.'),
           ('Le Marais', 'Explore historic streets, cafes and local shops.'),
           ('Latin Quarter', 'Wander through historic streets and food spots.')],
 'serengeti': [('Serengeti National Park', 'Plan a wildlife-focused safari with an authorised operator.'),
               ('Seronera', 'Explore the central Serengeti area known for wildlife viewing.'),
               ('Serengeti plains', 'Spend time observing the landscape and wildlife with a guide.'),
               ('Sunset safari', 'Choose a permitted evening safari experience where available.'),
               ('Local cultural experience', 'Include a respectful, locally guided cultural visit when appropriate.'),
               ('Wildlife photography', 'Use a guided viewing period for landscape and wildlife photography.')],
 'tokyo': [('Asakusa & Senso-ji', "Explore Tokyo's historic temple district and surrounding streets."),
           ('Shibuya Crossing', "Experience one of Tokyo's busiest urban landmarks."),
           ('Meiji Shrine', 'Walk through the forested shrine grounds near Harajuku.'),
           ('Akihabara', 'Explore anime, gaming and electronics culture.'),
           ('Shinjuku', "Explore the city's major entertainment and shopping district."),
           ('Tsukiji Outer Market', 'Browse food stalls and local culinary experiences.')],
 'victoria falls': [('Victoria Falls', 'Visit the waterfall viewpoints and follow current park guidance.'),
                    ('Zambezi River', 'Explore the river area with an authorised activity provider.'),
                    ('Victoria Falls town', 'Walk through the local town and nearby craft areas.'),
                    ('Zambezi sunset', 'Consider a permitted sunset river experience.'),
                    ('Rainforest viewpoints', 'Explore the viewpoints around the falls in suitable weather.'),
                    ('Local market', 'Browse local crafts and food respectfully.')]}

def _local_destination_key(destination):
    return re.sub(r"[^a-z0-9]+", " ", str(destination or "").lower()).strip()

def _local_fallback_attractions(destination):
    rows = LOCAL_ATTRACTIONS.get(_local_destination_key(destination))
    if rows:
        return [{"name": n, "description": d, "category": "Recommended place", "cost": None, "live": False, "source": "local planning data"} for n,d in rows]
    return [
        {"name": f"{destination} city highlights", "description": f"Explore well-known sights and neighbourhoods in {destination}.", "category": "Sightseeing", "cost": None, "live": False, "source": "local planning data"},
        {"name": f"{destination} local market", "description": f"Explore a suitable local market in {destination} after checking opening hours.", "category": "Market", "cost": None, "live": False, "source": "local planning data"},
        {"name": f"{destination} scenic area", "description": f"Choose a suitable scenic area in {destination} based on local conditions.", "category": "Nature", "cost": None, "live": False, "source": "local planning data"},
    ]

def food_tool(destination, location=None):
    key = _local_destination_key(destination)
    foods = LOCAL_FOOD.get(key)
    if not foods:
        country = str((location or {}).get("country") or "").lower()
        defaults = {
            "india": ["Local regional thali", "Street-food specialty", "Regional breakfast", "Local dessert"],
            "france": ["Croissant", "Crêpe", "French cheese", "Regional pastry"],
            "japan": ["Sushi", "Ramen", "Tempura", "Local dessert"],
            "indonesia": ["Nasi Goreng", "Mie Goreng", "Satay", "Local dessert"],
            "united arab emirates": ["Shawarma", "Machboos", "Hummus", "Luqaimat"],
            "south africa": ["Bobotie", "Braai", "Cape Malay curry", "Malva pudding"],
            "tanzania": ["Nyama Choma", "Ugali", "Pilau", "Tanzanian chapati"],
            "zimbabwe": ["Sadza", "Bream fish", "Nyama", "Local maize dishes"],
            "united states": ["Regional specialty", "Local street food", "Classic diner dish", "Local dessert"],
        }
        foods = defaults.get(country, [f"{destination} local specialty", f"{destination} regional dish", "Local breakfast", "Local dessert"])
    return {"type":"Food","destination":destination,"live":False,"available":True,"source":"local planning data","message":"Local food suggestions for planning. Prices and restaurant availability are not live.","options":[{"name":x,"category":"Local food","live":False} for x in foods]}

def flight_tool(destination, location=None):
    """Fetch current flight activity around a destination airport using Aviationstack."""
    api_key = os.getenv("AVIATIONSTACK_API_KEY", "").strip()
    if not api_key:
        key = _local_destination_key((location or {}).get("planning_city") or destination)
        local = DESTINATIONS.get(key, {})
        source_keys = [key] + LOCAL_REGION_KEYS.get(key, [])
        raw_options = []
        for source_key in source_keys:
            raw_options.extend((DESTINATIONS.get(source_key) or {}).get("flights", []) or [])
        options = [{**item, "status":"planning estimate", "live":False, "source":"local planning data"} for item in raw_options]
        if not options:
            options = [
                {"airline":"Flight planning option","route":f"Origin → {destination}","price":None,"status":"price unavailable","live":False,"source":"planning placeholder"},
                {"airline":"Alternative flight option","route":f"Origin → {destination}","price":None,"status":"price unavailable","live":False,"source":"planning placeholder"},
            ]
            message = "Live flight data is not connected. These are route-planning placeholders; no fare is claimed."
        else:
            message = "Showing local planning estimates. Connect AVIATIONSTACK_API_KEY for live flight data."
        return {"type":"Flight","destination":destination,"live":False,"available":True,"source":"local planning data","message":message,"options":options}

    location = location or {}
    mapped_iata = location.get("airport_iata")
    airport_query = location.get("airport_search_name") or location.get("name") or destination

    if mapped_iata:
        airport = {
            "iata_code": mapped_iata,
            "name": location.get("representative_place") or airport_query,
            "country_name": location.get("country", ""),
        }
        airport_payload = {"data": [airport]}
        airport_error = None
    else:
        airport_payload, airport_error = _request_json(
            "https://api.aviationstack.com/v1/airports",
            params={"access_key": api_key, "search": airport_query},
        )

    if airport_error:
        return {
            "type": "Flight",
            "destination": destination,
            "live": True,
            "available": False,
            "message": airport_error,
            "options": [],
        }

    airports = airport_payload.get("data") or []
    if not airports:
        return {
            "type": "Flight",
            "destination": destination,
            "live": True,
            "available": False,
            "message": f"No airport match was returned for {destination}.",
            "options": [],
        }

    airport = airports[0]
    iata = airport.get("iata_code")
    if not iata:
        return {
            "type": "Flight",
            "destination": destination,
            "live": True,
            "available": False,
            "message": f"No IATA airport code was returned for {destination}.",
            "options": [],
        }

    payload, error = _request_json(
        "https://api.aviationstack.com/v1/flights",
        params={
            "access_key": api_key,
            "arr_iata": iata,
            "flight_status": "active",
            "limit": 8,
        },
    )

    if error:
        return {
            "type": "Flight",
            "destination": destination,
            "airport": airport,
            "live": True,
            "available": False,
            "message": error,
            "options": [],
        }

    options = []
    for flight in payload.get("data") or []:
        airline = (flight.get("airline") or {}).get("name") or "Airline"
        flight_number = flight.get("flight", {}).get("iata") or flight.get("flight", {}).get("number") or ""
        departure = flight.get("departure") or {}
        arrival = flight.get("arrival") or {}
        options.append({
            "airline": airline,
            "flight_number": flight_number,
            "route": f"{departure.get('airport', 'Unknown')} → {arrival.get('airport', airport.get('name', destination))}",
            "status": flight.get("flight_status", "unknown"),
            "departure_time": departure.get("scheduled") or departure.get("estimated"),
            "arrival_time": arrival.get("scheduled") or arrival.get("estimated"),
            "departure_terminal": departure.get("terminal"),
            "arrival_terminal": arrival.get("terminal"),
            "gate": arrival.get("gate") or departure.get("gate"),
            "live": True,
        })

    return {
        "type": "Flight",
        "destination": destination,
        "airport": airport,
        "live": True,
        "available": bool(options),
        "options": options,
        "message": "Live active-arrival flight data retrieved." if options else "No active arrival flights were returned for this airport right now.",
    }


def hotel_tool(destination, nights=3, adults=1, location=None):
    """Fetch live accommodation search results through StayingAPI when configured."""
    api_key = os.getenv("STAYINGAPI_KEY", "").strip()
    if not api_key:
        key = _local_destination_key((location or {}).get("planning_city") or destination)
        local = DESTINATIONS.get(key, {})
        source_keys = [key] + LOCAL_REGION_KEYS.get(key, [])
        options=[]
        for source_key in source_keys:
            for item in (DESTINATIONS.get(source_key) or {}).get("hotels", []) or []:
                nightly=item.get("price_per_night") or item.get("price")
                options.append({**item,"price":nightly,"price_per_night":nightly,"currency":"₹","rating":item.get("rating"),"live":False,"source":"local planning data"})
        if options:
            message="Showing local accommodation estimates. Connect STAYINGAPI_KEY for live hotel inventory."
        else:
            options=[{"name":f"{destination} Central Stay","area":destination,"price":None,"price_per_night":None,"currency":"","rating":None,"live":False,"source":"planning placeholder"},{"name":f"{destination} Comfort Residency","area":destination,"price":None,"price_per_night":None,"currency":"","rating":None,"live":False,"source":"planning placeholder"}]
            message="No live hotel inventory is connected. These are planning placeholders; no price is claimed."
        return {"type":"Hotel","destination":destination,"live":False,"available":True,"source":"local planning data","message":message,"options":options}

    location = location or {}
    location_text = destination
    if location.get("country"):
        location_text = f"{destination}, {location['country']}"

    check_in, check_out = _today_and_checkout(nights)
    payload, error = _request_json(
        "https://api.stayingapi.com/v1/search",
        params={
            "location": location_text,
            "platforms": "booking,google",
            "limit": 8,
            "checkIn": check_in,
            "checkOut": check_out,
            "adults": max(1, int(adults or 1)),
        },
        headers={"Authorization": f"Bearer {api_key}"},
    )

    if error:
        return {
            "type": "Hotel",
            "destination": destination,
            "live": True,
            "available": False,
            "message": error,
            "options": [],
        }

    options = []
    for item in payload.get("data") or []:
        price = item.get("price")
        if isinstance(price, dict):
            price_value = price.get("amount") or price.get("value") or price.get("total")
            currency = price.get("currency") or ""
        else:
            price_value = price
            currency = item.get("currency") or ""

        options.append({
            "name": item.get("name") or "Accommodation",
            "area": item.get("location") or item.get("address") or destination,
            "price": price_value,
            "currency": currency,
            "rating": item.get("rating") or item.get("guestRating"),
            "platform": item.get("platform"),
            "listing_id": item.get("platformListingId") or item.get("listingId"),
            "live": True,
            "check_in": check_in,
            "check_out": check_out,
        })

    return {
        "type": "Hotel",
        "destination": destination,
        "live": True,
        "available": bool(options),
        "options": options,
        "message": "Live accommodation results retrieved." if options else "No live accommodation results were returned for these dates.",
    }


def weather_tool(destination, location=None, forecast_days=7):
    """Fetch current and forecast weather from Open-Meteo."""
    location = location or {}
    latitude = location.get("latitude")
    longitude = location.get("longitude")

    if latitude is None or longitude is None:
        return {
            "type": "Weather",
            "destination": destination,
            "live": False,
            "available": False,
            "message": "Weather coordinates are unavailable for this destination.",
            "current": {},
            "daily": [],
        }

    payload, error = _request_json(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "forecast_days": max(1, min(16, int(forecast_days))),
            "timezone": "auto",
        },
    )

    if error:
        return {
            "type": "Weather",
            "destination": destination,
            "live": True,
            "available": False,
            "message": error,
            "current": {},
            "daily": [],
        }

    current = payload.get("current") or {}
    daily = payload.get("daily") or {}
    dates = daily.get("time") or []
    highs = daily.get("temperature_2m_max") or []
    lows = daily.get("temperature_2m_min") or []
    codes = daily.get("weather_code") or []
    rain = daily.get("precipitation_probability_max") or []

    daily_rows = []
    for index, day in enumerate(dates):
        daily_rows.append({
            "date": day,
            "high": highs[index] if index < len(highs) else None,
            "low": lows[index] if index < len(lows) else None,
            "weather_code": codes[index] if index < len(codes) else None,
            "rain_probability": rain[index] if index < len(rain) else None,
        })

    return {
        "type": "Weather",
        "destination": destination,
        "live": True,
        "available": True,
        "timezone": payload.get("timezone"),
        "current": current,
        "daily": daily_rows,
        "message": "Current conditions and forecast retrieved from Open-Meteo.",
    }


def activity_tool(destination, location=None):
    """Fetch live-ish POI/attraction discovery through OpenTripMap when configured."""
    api_key = os.getenv("OPENTRIPMAP_API_KEY", "").strip()
    if not api_key:
        options=_local_fallback_attractions((location or {}).get("planning_city") or destination)
        return {"type":"Activities","destination":destination,"live":False,"available":bool(options),"source":"local planning data","message":"Showing recommended places from local planning data. Connect OPENTRIPMAP_API_KEY for live attraction discovery.","options":options}

    location = location or {}
    lat = location.get("latitude")
    lon = location.get("longitude")
    if lat is None or lon is None:
        return {
            "type": "Activities",
            "destination": destination,
            "live": False,
            "available": False,
            "message": "Attraction coordinates are unavailable for this destination.",
            "options": [],
        }

    payload, error = _request_json(
        "https://api.opentripmap.com/0.1/en/places/radius",
        params={
            "lat": lat,
            "lon": lon,
            "radius": 10000,
            "limit": 12,
            "rate": 2,
            "format": "json",
            "apikey": api_key,
        },
    )

    if error:
        return {
            "type": "Activities",
            "destination": destination,
            "live": True,
            "available": False,
            "message": error,
            "options": [],
        }

    options = []
    for item in payload or []:
        name = item.get("name")
        if not name:
            continue
        options.append({
            "name": name,
            "category": item.get("kinds", "Attraction").replace("_", " "),
            "distance_m": item.get("dist"),
            "xid": item.get("xid"),
            "cost": None,
            "live": True,
        })

    return {
        "type": "Activities",
        "destination": destination,
        "live": True,
        "available": bool(options),
        "options": options,
        "message": "Current attraction data retrieved." if options else "No attraction results were returned.",
    }


def budget_tool(destination, nights=3, flight_result=None, hotel_result=None, activity_result=None):
    """Calculate a transparent budget from live numeric prices when available."""
    nights = max(1, int(nights or 1))
    flight_options = (flight_result or {}).get("options") or []
    hotel_options = (hotel_result or {}).get("options") or []
    activity_options = (activity_result or {}).get("options") or []

    flight_prices = []
    for item in flight_options:
        for key in ("price", "fare", "cost", "amount"):
            value = item.get(key)
            if value is not None:
                try:
                    flight_prices.append(float(value))
                    break
                except (TypeError, ValueError):
                    pass

    hotel_prices = []
    for item in hotel_options:
        for key in ("price_per_night", "price", "nightly_price", "amount"):
            value = item.get(key)
            if value is not None:
                try:
                    hotel_prices.append(float(value))
                    break
                except (TypeError, ValueError):
                    pass

    activity_prices = []
    for item in activity_options:
        value = item.get("cost")
        if value is not None:
            try:
                activity_prices.append(float(value))
            except (TypeError, ValueError):
                pass

    # Food/local transport are intentionally estimates, not presented as live prices.
    food = 1000 * nights
    local_transport = 500 * nights

    breakdown = {
        "flight": min(flight_prices) if flight_prices else None,
        "hotel": (min(hotel_prices) * nights) if hotel_prices else None,
        "activities": sum(activity_prices) if activity_prices else 0,
        "food_estimate": food,
        "local_transport_estimate": local_transport,
    }

    known = [value for value in breakdown.values() if isinstance(value, (int, float))]
    estimated_total = sum(known) if known else None

    return {
        "type": "Budget",
        "destination": destination,
        "nights": nights,
        "live_components": [
            key for key in ("flight", "hotel", "activities")
            if breakdown[key] is not None
        ],
        "estimated_components": ["food_estimate", "local_transport_estimate"],
        "breakdown": breakdown,
        "estimated_total": estimated_total,
        "fully_live": breakdown["flight"] is not None and breakdown["hotel"] is not None,
    }
