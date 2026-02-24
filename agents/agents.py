from utils.groq_client import call_groq
from utils.prompt_templates import (
    region_discovery_prompt,
    climate_analysis_prompt,
    risk_analysis_prompt,
    infrastructure_prompt,
    policy_prompt,
    sustainability_prompt,
    final_recommendation_prompt,
)
from scoring.scoring_engine import compute_suitability_score


def run_region_discovery(country: str, datacenter_type: str, scale: str) -> dict:
    prompt = region_discovery_prompt(country, datacenter_type, scale)
    result = call_groq(prompt)
    if not result["success"]:
        raise RuntimeError(f"Region Discovery failed: {result['error']}")
    return result["data"]


def run_region_analysis(country: str, region: str, city: str, lat: float, lon: float) -> dict:
    """Run all 5 analysis agents for a single region."""

    # Agent 1: Climate
    r = call_groq(climate_analysis_prompt(country, region, city))
    if not r["success"]:
        raise RuntimeError(f"Climate agent failed for {region}: {r['error']}")
    climate = r["data"]

    # Agent 2: Risk
    r = call_groq(risk_analysis_prompt(country, region, city))
    if not r["success"]:
        raise RuntimeError(f"Risk agent failed for {region}: {r['error']}")
    risk = r["data"]

    # Agent 3: Infrastructure
    r = call_groq(infrastructure_prompt(country, region, city))
    if not r["success"]:
        raise RuntimeError(f"Infrastructure agent failed for {region}: {r['error']}")
    infra = r["data"]

    # Agent 4: Policy
    r = call_groq(policy_prompt(country, region))
    if not r["success"]:
        raise RuntimeError(f"Policy agent failed for {region}: {r['error']}")
    policy = r["data"]

    # Agent 5: Sustainability
    r = call_groq(sustainability_prompt(country, region, climate, risk, policy))
    if not r["success"]:
        raise RuntimeError(f"Sustainability agent failed for {region}: {r['error']}")
    sustain = r["data"]

    # Scoring
    score = compute_suitability_score(
        climate_score=climate.get("climate_score", 50),
        risk_score=risk.get("risk_score", 50),
        infrastructure_score=infra.get("infrastructure_score", 50),
        policy_score=policy.get("policy_score", 50),
        sustainability_score=sustain.get("sustainability_score", 50),
    )

    return {
        "region": region,
        "city": city,
        "latitude": lat,
        "longitude": lon,
        "climate": climate,
        "risk": risk,
        "infrastructure": infra,
        "policy": policy,
        "sustainability": sustain,
        "score": score,
    }


def run_final_recommendation(country: str, analyzed_regions: list) -> dict:
    summary_list = [
        {
            "region": r["region"],
            "city": r["city"],
            "suitability_score": r["score"]["score"],
            "grade": r["score"]["grade"],
            "climate_score": r["climate"].get("climate_score"),
            "risk_score": r["risk"].get("risk_score"),
            "infrastructure_score": r["infrastructure"].get("infrastructure_score"),
            "policy_score": r["policy"].get("policy_score"),
            "sustainability_score": r["sustainability"].get("sustainability_score"),
            "natural_cooling": r["climate"].get("natural_cooling_potential"),
            "renewable_dominant": r["climate"].get("renewable_energy", {}).get("dominant_source"),
            "political_stability": r["risk"].get("political_stability"),
        }
        for r in analyzed_regions
    ]
    result = call_groq(final_recommendation_prompt(country, summary_list))
    if not result["success"]:
        raise RuntimeError(f"Final recommendation failed: {result['error']}")
    return result["data"]
