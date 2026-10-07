"""Own short sector list (no KBLI) and Google Places type mapping. Edit freely."""
UNCLEAR = "Other / unclear"
SECTORS = [
    "Construction and contractors", "Manufacturing", "Logistics and transport",
    "IT and software", "Professional services", "Printing and promo materials",
    "Food and beverage", "General trading", "Facility and maintenance",
    "Energy and mining", "Agriculture and plantation", "Marketing and events",
    "Manpower and outsourcing", UNCLEAR,
]
# Maps type -> sector. Only specific types; generic ones fall through to search + AI.
TYPE_MAP = {
    "general_contractor": SECTORS[0], "construction_company": SECTORS[0], "roofing_contractor": SECTORS[0],
    "electrician": SECTORS[0], "plumber": SECTORS[0],
    "manufacturer": SECTORS[1], "factory": SECTORS[1], "steel_fabricator": SECTORS[1],
    "moving_company": SECTORS[2], "courier_service": SECTORS[2], "logistics_service": SECTORS[2],
    "freight_forwarding_service": SECTORS[2], "storage": SECTORS[2], "trucking_company": SECTORS[2],
    "software_company": SECTORS[3], "internet_service_provider": SECTORS[3], "computer_store": SECTORS[3],
    "consultant": SECTORS[4], "lawyer": SECTORS[4], "accounting": SECTORS[4], "market_researcher": SECTORS[4],
    "printing_service": SECTORS[5], "sign_shop": SECTORS[5], "print_shop": SECTORS[5],
    "restaurant": SECTORS[6], "catering_service": SECTORS[6], "food_manufacturer": SECTORS[6], "bakery": SECTORS[6],
    "wholesaler": SECTORS[7], "distributor": SECTORS[7], "supplier": SECTORS[7],
    "cleaning_service": SECTORS[8], "security_service": SECTORS[8], "pest_control_service": SECTORS[8],
    "mining_company": SECTORS[9], "oil_and_gas_company": SECTORS[9], "power_plant": SECTORS[9],
    "farm": SECTORS[10], "plantation": SECTORS[10],
    "advertising_agency": SECTORS[11], "marketing_agency": SECTORS[11], "event_planner": SECTORS[11],
    "employment_agency": SECTORS[12], "staffing_agency": SECTORS[12],
}

# OpenStreetMap "key=value" -> sector (coverage of Indonesian B2B firms is thin; edit freely)
OSM_MAP = {
    "craft=printer": SECTORS[5], "shop=copyshop": SECTORS[5],
    "office=construction_company": SECTORS[0], "craft=builder": SECTORS[0],
    "man_made=works": SECTORS[1], "industrial=factory": SECTORS[1],
    "office=logistics": SECTORS[2], "office=freight_forwarder": SECTORS[2],
    "office=it": SECTORS[3], "office=consulting": SECTORS[4], "office=lawyer": SECTORS[4],
    "craft=caterer": SECTORS[6], "office=advertising_agency": SECTORS[11],
    "office=employment_agency": SECTORS[12],
}
# Category words in a search -> OSM tags to look for (used with a city)
CATEGORY_TAGS = {
    ("percetakan", "cetak", "printing", "print"): ["craft=printer", "shop=copyshop"],
    ("kontraktor", "konstruksi", "contractor", "construction"): ["office=construction_company", "craft=builder"],
    ("pabrik", "manufaktur", "factory", "manufacturing"): ["man_made=works", "industrial=factory"],
    ("logistik", "ekspedisi", "cargo", "logistics", "freight"): ["office=logistics", "office=freight_forwarder"],
    ("software", "it consulting", "teknologi informasi"): ["office=it"],
    ("konsultan", "consultant", "consulting"): ["office=consulting"],
    ("katering", "catering"): ["craft=caterer"],
    ("periklanan", "advertising", "agensi iklan"): ["office=advertising_agency"],
    ("outsourcing", "tenaga kerja", "rekrutmen"): ["office=employment_agency"],
}
