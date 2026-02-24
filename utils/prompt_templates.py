def region_discovery_prompt(country: str, datacenter_type: str, scale: str) -> str:
    return f"""
You are a geospatial infrastructure analyst. For the country "{country}", identify the TOP 4 most strategic regions/states for building a {scale} {datacenter_type} data center.

Consider: climate zones, existing tech hubs, power infrastructure, connectivity, land availability, and government policies.

Output ONLY this JSON:
{{
  "country": "{country}",
  "regions": [
    {{
      "name": "Region/State name",
      "city": "Nearest major city",
      "latitude": 0.0,
      "longitude": 0.0,
      "brief": "One sentence why this region is promising"
    }}
  ]
}}

Return exactly 4 regions. Latitude and longitude must be accurate floating point numbers.
"""


def climate_analysis_prompt(country: str, region: str, city: str) -> str:
    return f"""
You are a climate and energy analyst. Analyze {region}, {country} (near {city}) for data center suitability from a climate and energy perspective.

Output ONLY this JSON:
{{
  "avg_temperature_celsius": 0,
  "climate_type": "e.g. Tropical/Arid/Temperate/Continental",
  "natural_cooling_potential": "excellent/good/moderate/poor",
  "natural_cooling_explanation": "How natural cooling can be leveraged here",
  "humidity_level": "low/moderate/high",
  "humidity_impact": "Impact on cooling systems",
  "renewable_energy": {{
    "solar": {{"availability": "excellent/good/moderate/poor", "capacity_gw_estimate": 0.0, "notes": ""}},
    "wind": {{"availability": "excellent/good/moderate/poor", "capacity_gw_estimate": 0.0, "notes": ""}},
    "hydro": {{"availability": "excellent/good/moderate/poor", "notes": ""}},
    "dominant_source": "solar/wind/hydro/mixed"
  }},
  "pue_estimate": 1.0,
  "pue_explanation": "Why this PUE (Power Usage Effectiveness, ideal is 1.0, typical is 1.2-1.8)",
  "climate_score": 0,
  "climate_score_rationale": "Why this score (0-100)"
}}

Set climate_score as integer 0-100. PUE should be realistic float like 1.15, 1.3, etc.
"""


def risk_analysis_prompt(country: str, region: str, city: str) -> str:
    return f"""
You are a risk assessment specialist for critical infrastructure. Analyze {region}, {country} for data center risk factors.

Output ONLY this JSON:
{{
  "seismic_risk": "very low/low/moderate/high/very high",
  "seismic_explanation": "Seismic activity details for this region",
  "flood_risk": "very low/low/moderate/high/very high",
  "flood_explanation": "Flood risk context",
  "cyclone_risk": "very low/low/moderate/high/very high",
  "extreme_heat_risk": "very low/low/moderate/high/very high",
  "water_availability": "abundant/adequate/limited/scarce",
  "water_explanation": "Water sources for cooling, scarcity concerns",
  "political_stability": "very stable/stable/moderate/unstable",
  "political_notes": "Key political/regulatory considerations",
  "overall_risks": [
    {{"risk": "Risk name", "severity": "high/medium/low", "mitigation": "How to address it"}}
  ],
  "risk_score": 0,
  "risk_score_rationale": "Why this score (0-100, higher = riskier)"
}}

Provide at least 4 overall_risks. risk_score as integer 0-100.
"""


def infrastructure_prompt(country: str, region: str, city: str) -> str:
    return f"""
You are an infrastructure and logistics analyst. Evaluate {region}, {country} (near {city}) for data center infrastructure readiness.

Output ONLY this JSON:
{{
  "power_grid_reliability": "excellent/good/moderate/poor",
  "grid_notes": "Power grid quality, outage frequency, expansion plans",
  "fiber_connectivity": "excellent/good/moderate/poor",
  "fiber_notes": "Existing fiber, submarine cables, latency to major hubs",
  "land_cost": "very low/low/moderate/high/very high",
  "land_cost_usd_per_acre": "$X,XXX - $XX,XXX",
  "construction_cost_index": "low/moderate/high",
  "labor_availability": "excellent/good/moderate/poor",
  "skilled_tech_workforce": "large/moderate/limited/scarce",
  "nearest_internet_exchange": "Name and distance",
  "latency_to_major_hubs": {{
    "mumbai_or_nearest": "X ms",
    "singapore": "X ms",
    "london": "X ms"
  }},
  "existing_data_centers": "none/few/several/many",
  "infrastructure_score": 0,
  "infrastructure_score_rationale": "Why this score (0-100)"
}}

infrastructure_score as integer 0-100.
"""


def policy_prompt(country: str, region: str) -> str:
    return f"""
You are a policy and regulatory analyst. Research government policies, incentives, and regulatory environment for data centers in {region}, {country}.

Output ONLY this JSON:
{{
  "data_center_policy": "supportive/neutral/restrictive",
  "government_initiatives": ["initiative 1", "initiative 2", "initiative 3"],
  "tax_incentives": "Description of tax breaks, SEZ benefits, etc.",
  "data_localization_laws": "Any data sovereignty/localization requirements",
  "foreign_investment": "open/conditional/restricted",
  "environmental_regulations": "strict/moderate/lenient",
  "green_certifications_available": ["LEED", "ISO 50001", "others"],
  "recent_announcements": ["Any recent gov announcements about digital infrastructure"],
  "ease_of_doing_business": "excellent/good/moderate/difficult",
  "policy_score": 0,
  "policy_score_rationale": "Why this score (0-100)"
}}

policy_score as integer 0-100.
"""


def sustainability_prompt(country: str, region: str, climate: dict, risk: dict, policy: dict) -> str:
    return f"""
You are a sustainability strategist for green data centers. Synthesize a sustainability assessment for {region}, {country}.

CLIMATE DATA: {climate}
RISK DATA: {risk}
POLICY DATA: {policy}

Output ONLY this JSON:
{{
  "green_energy_potential": "excellent/good/moderate/poor",
  "carbon_footprint_estimate": "X gCO2/kWh equivalent",
  "water_efficiency_strategy": "Best water cooling strategy for this region",
  "recommended_cooling_tech": ["cooling tech 1", "cooling tech 2"],
  "sustainability_certifications": ["certifications to pursue"],
  "esg_score_potential": "high/medium/low",
  "carbon_neutral_timeline": "Realistic timeline to carbon neutrality",
  "key_sustainability_wins": ["win 1", "win 2", "win 3"],
  "sustainability_challenges": ["challenge 1", "challenge 2"],
  "sustainability_score": 0,
  "sustainability_score_rationale": "Why this score (0-100)"
}}

sustainability_score as integer 0-100.
"""


def final_recommendation_prompt(country: str, analyzed_regions: list) -> str:
    return f"""
You are a chief infrastructure strategist. Based on the multi-dimensional analysis of regions in {country}, provide final strategic recommendations.

ANALYZED REGIONS: {analyzed_regions}

Output ONLY this JSON:
{{
  "executive_summary": "2-3 sentence overview of findings",
  "top_recommendation": "Name of the single best region and why in 2 sentences",
  "ranking": [
    {{
      "rank": 1,
      "region": "region name",
      "one_liner": "Why this rank in one sentence",
      "best_for": "hyperscale/edge/colocation/green-focused"
    }}
  ],
  "comparative_insight": "Key insight comparing the regions (2-3 sentences)",
  "investment_timeline": "Recommended phased approach for development",
  "watch_out": "The single biggest risk to watch across all sites"
}}

Provide ranking for all analyzed regions.
"""
