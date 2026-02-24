"""
DataCenter Suitability Score Formula:

  Suitability Score = (
      climate_score        * 0.25  +
      (100 - risk_score)   * 0.25  +
      infrastructure_score * 0.25  +
      policy_score         * 0.15  +
      sustainability_score * 0.10
  )

Grades:
  85-100 : S  — World-class site, pursue immediately
  70-84  : A  — Excellent, strong investment case
  55-69  : B  — Good with manageable trade-offs
  40-54  : C  — Viable but significant improvements needed
  0-39   : D  — Not recommended
"""


def compute_suitability_score(
    climate_score: int,
    risk_score: int,
    infrastructure_score: int,
    policy_score: int,
    sustainability_score: int,
) -> dict:
    def clamp(v):
        try:
            return max(0, min(100, int(v)))
        except:
            return 50

    c  = clamp(climate_score)
    r  = clamp(risk_score)
    i  = clamp(infrastructure_score)
    p  = clamp(policy_score)
    s  = clamp(sustainability_score)

    weighted = (
        c  * 0.25 +
        (100 - r) * 0.25 +
        i  * 0.25 +
        p  * 0.15 +
        s  * 0.10
    )

    final = round(weighted, 1)

    if final >= 85:
        grade, label, color = "S", "World-class — Pursue immediately", "#00d4aa"
    elif final >= 70:
        grade, label, color = "A", "Excellent — Strong investment case", "#6fdc8c"
    elif final >= 55:
        grade, label, color = "B", "Good — Manageable trade-offs", "#7c6bff"
    elif final >= 40:
        grade, label, color = "C", "Viable — Significant improvements needed", "#f1c21b"
    else:
        grade, label, color = "D", "Not recommended", "#fa4d56"

    return {
        "score": final,
        "grade": grade,
        "label": label,
        "color": color,
        "breakdown": {
            "climate":          {"raw": c,       "weight": "25%", "contribution": round(c * 0.25, 1)},
            "risk_adjusted":    {"raw": 100 - r, "weight": "25%", "contribution": round((100 - r) * 0.25, 1)},
            "infrastructure":   {"raw": i,       "weight": "25%", "contribution": round(i * 0.25, 1)},
            "policy":           {"raw": p,       "weight": "15%", "contribution": round(p * 0.15, 1)},
            "sustainability":   {"raw": s,       "weight": "10%", "contribution": round(s * 0.10, 1)},
        },
    }
