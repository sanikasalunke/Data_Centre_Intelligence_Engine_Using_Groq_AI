import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify
from agents.agents import run_region_discovery, run_region_analysis, run_final_recommendation

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        mode = request.form.get("mode", "single")  # single | compare
        datacenter_type = request.form.get("datacenter_type", "hyperscale")
        scale = request.form.get("scale", "large-scale")

        if mode == "compare":
            countries_raw = request.form.get("countries", "")
            countries = [c.strip() for c in countries_raw.split(",") if c.strip()]
            if not countries or len(countries) < 2:
                return render_template("index.html", error="Please enter at least 2 countries to compare.")

            all_results = []
            for country in countries[:3]:  # max 3 for speed
                discovery = run_region_discovery(country, datacenter_type, scale)
                regions = discovery.get("regions", [])[:2]  # top 2 per country in compare mode
                for reg in regions:
                    analysis = run_region_analysis(
                        country=country,
                        region=reg["name"],
                        city=reg["city"],
                        lat=reg["latitude"],
                        lon=reg["longitude"],
                    )
                    analysis["country"] = country
                    all_results.append(analysis)

            all_results.sort(key=lambda x: x["score"]["score"], reverse=True)
            recommendation = run_final_recommendation(
                f"comparison across {', '.join(countries)}", all_results
            )

            return render_template(
                "result.html",
                mode="compare",
                countries=countries,
                regions=all_results,
                recommendation=recommendation,
                datacenter_type=datacenter_type,
                scale=scale,
            )

        else:
            # Single country mode
            country = request.form.get("country", "").strip()
            specific_region = request.form.get("specific_region", "").strip()

            if not country:
                return render_template("index.html", error="Please enter a country.")

            if specific_region:
                # User specified a region — analyze it directly + AI picks 3 more
                discovery = run_region_discovery(country, datacenter_type, scale)
                regions_raw = discovery.get("regions", [])[:3]

                # Prepend user's specified region
                user_region = {
                    "name": specific_region,
                    "city": specific_region,
                    "latitude": regions_raw[0]["latitude"] if regions_raw else 20.0,
                    "longitude": regions_raw[0]["longitude"] if regions_raw else 78.0,
                    "brief": "User-specified region"
                }
                regions_raw = [user_region] + regions_raw[:3]
            else:
                discovery = run_region_discovery(country, datacenter_type, scale)
                regions_raw = discovery.get("regions", [])[:4]

            analyzed = []
            for reg in regions_raw:
                analysis = run_region_analysis(
                    country=country,
                    region=reg["name"],
                    city=reg.get("city", reg["name"]),
                    lat=float(reg.get("latitude", 20.0)),
                    lon=float(reg.get("longitude", 78.0)),
                )
                analysis["country"] = country
                analysis["brief"] = reg.get("brief", "")
                analyzed.append(analysis)

            analyzed.sort(key=lambda x: x["score"]["score"], reverse=True)
            recommendation = run_final_recommendation(country, analyzed)

            return render_template(
                "result.html",
                mode="single",
                country=country,
                regions=analyzed,
                recommendation=recommendation,
                datacenter_type=datacenter_type,
                scale=scale,
            )

    except RuntimeError as e:
        return render_template("index.html", error=str(e))
    except Exception as e:
        return render_template("index.html", error=f"Unexpected error: {str(e)}")


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    try:
        data = request.get_json()
        country = data.get("country", "India")
        datacenter_type = data.get("datacenter_type", "hyperscale")
        scale = data.get("scale", "large-scale")

        discovery = run_region_discovery(country, datacenter_type, scale)
        regions_raw = discovery.get("regions", [])[:4]

        analyzed = []
        for reg in regions_raw:
            analysis = run_region_analysis(
                country=country,
                region=reg["name"],
                city=reg.get("city", reg["name"]),
                lat=float(reg.get("latitude", 20.0)),
                lon=float(reg.get("longitude", 78.0)),
            )
            analysis["country"] = country
            analyzed.append(analysis)

        analyzed.sort(key=lambda x: x["score"]["score"], reverse=True)
        recommendation = run_final_recommendation(country, analyzed)

        return jsonify({"success": True, "regions": analyzed, "recommendation": recommendation})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    print("\n🌍 DataCenter Site Intelligence Engine")
    print("=" * 42)
    print("Open: http://localhost:5000")
    print("=" * 42)
    app.run(debug=True, host="0.0.0.0", port=5000)
