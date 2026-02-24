# 🌍 DataCenter Site Intelligence Engine

> **AI-powered multi-agent system that analyzes climate, infrastructure, risk, policy & sustainability to identify the world's best data center locations.**

Inspired by the global race to build AI infrastructure — from Google's data centers in India to hyperscale deployments across Southeast Asia and Europe — this tool gives founders, infrastructure teams, and researchers a structured AI engine to evaluate and compare data center sites worldwide.

---

## ✨ What It Does

You input a country (or multiple countries to compare), and 7 specialized AI agents run a deep analysis across every dimension that matters for data center siting — from natural cooling potential and renewable energy availability to seismic risk, government incentives, and carbon neutrality timelines.

The result: a ranked, scored report with an interactive map, detailed site breakdowns, and a strategic recommendation — all generated in under 60 seconds.

---

## 🖥️ Screenshots

> Single country mode → AI discovers top 4 regions, scores them, maps them.

> Compare mode → Pit India vs Germany vs Singapore and get a global ranking.

---

## 🤖 The 7 AI Agents

| Agent | Role |
|---|---|
| 🌍 **Region Discovery** | Identifies the top 4 strategic regions within a country based on tech infrastructure, climate zones, and connectivity |
| 🌡️ **Climate Analysis** | Evaluates natural cooling potential, avg temperature, humidity, PUE estimate, and renewable energy (solar/wind/hydro) |
| ⚠️ **Risk Assessment** | Scores seismic, flood, cyclone, extreme heat, water scarcity, and political stability risks with mitigations |
| ⚡ **Infrastructure** | Analyzes power grid reliability, fiber connectivity, land cost, workforce, IXP proximity, and latency to major hubs |
| 📜 **Policy & Incentives** | Researches government initiatives, tax incentives, data localization laws, and foreign investment openness |
| 🌱 **Sustainability** | Computes carbon footprint, ESG potential, water efficiency strategy, carbon neutrality timeline, and green certifications |
| 🏆 **Final Ranking** | Synthesizes all agent outputs into a strategic recommendation with ranked sites and investment guidance |

---

## 📊 Suitability Score Formula

```
Suitability Score =
    Climate Score        × 0.25
  + (100 − Risk Score)   × 0.25
  + Infrastructure Score × 0.25
  + Policy Score         × 0.15
  + Sustainability Score × 0.10
```

| Grade | Range | Label |
|---|---|---|
| **S** | 85–100 | World-class — Pursue immediately |
| **A** | 70–84 | Excellent — Strong investment case |
| **B** | 55–69 | Good — Manageable trade-offs |
| **C** | 40–54 | Viable — Significant improvements needed |
| **D** | 0–39 | Not recommended |

---

## 🗺️ Three Input Modes

- 🌐 **Single Country** — Enter any country, AI discovers and scores the top 4 best regions automatically
- 📍 **Country + Region** — Specify your own region of interest alongside AI-discovered alternatives
- ⚖️ **Compare Countries** — Enter 2–3 countries, AI picks the top 2 regions per country and ranks them globally

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/datacenter-intelligence.git
cd datacenter-intelligence
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get your free Groq API key
Sign up at **https://console.groq.com** — no credit card required.

### 4. Add your API key
Open `utils/groq_client.py` and paste your key:
```python
GROQ_API_KEY = "gsk_your_key_here"
```

### 5. Run the app
```bash
python app.py
```

### 6. Open in browser
```
http://localhost:5000
```

---

## 🏗️ Project Structure

```
datacenter-intelligence/
│
├── app.py                          ← Flask app + route orchestration
│
├── agents/
│   └── agents.py                   ← All 7 AI agents + orchestration logic
│
├── scoring/
│   └── scoring_engine.py           ← Weighted suitability score formula
│
├── utils/
│   ├── groq_client.py              ← Groq API wrapper with JSON retry logic
│   └── prompt_templates.py         ← Structured prompts for each agent
│
├── templates/
│   ├── index.html                  ← Input form (single / compare modes)
│   └── result.html                 ← Results: map + ranked cards + reports
│
└── requirements.txt
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + Flask |
| LLM | Groq API (Llama 3.3 70B) — **free** |
| Frontend | HTML + CSS + Vanilla JS (Jinja2 templates) |
| Map | Leaflet.js with CartoDB dark tiles |
| Styling | Custom dark UI, IBM Plex Mono + Space Grotesk |

---

## 💡 Example Queries to Try

- `India` → Discovers Rajasthan (solar), Maharashtra (infra), Andhra Pradesh (coast), Himachal Pradesh (cooling)
- `Germany` → Discovers Frankfurt, Berlin, Munich, Hamburg with EU policy analysis
- `Compare: India, Singapore, Germany` → Global cross-country ranking with head-to-head scores

---

## 🔌 JSON API

The app also exposes a REST endpoint for programmatic access:

```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "country": "India",
    "datacenter_type": "hyperscale",
    "scale": "large-scale"
  }'
```

---

## 📝 Notes

- Each analysis runs **7 sequential Groq API calls** — expect ~45–90 seconds total
- All agents enforce **strict JSON output** with automatic retry on parse failure
- Model: `llama-3.3-70b-versatile` via Groq (completely free tier)
- Latency and coordinate data is AI-estimated — validate before production use

---

## 🌱 Roadmap

- [ ] Real-time climate data integration (Open-Meteo API)
- [ ] Power grid data from national energy APIs
- [ ] PDF report export
- [ ] Historical site comparison saved to local DB
- [ ] Docker Compose deployment

---

## 📄 License

MIT License — free to use, modify, and deploy.

---

<p align="center">Built with ⚡ Groq · 🌍 Leaflet · 🐍 Flask · 🤖 Llama 3.3</p>
