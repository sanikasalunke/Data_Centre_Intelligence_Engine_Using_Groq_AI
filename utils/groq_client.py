from groq import Groq
import json
import re
import time
import httpx

GROQ_MODEL = "llama-3.3-70b-versatile"

# Paste your Groq API key here
GROQ_API_KEY = ""


def get_client():
    http_client = httpx.Client()
    return Groq(api_key=GROQ_API_KEY, http_client=http_client)


def call_groq(prompt: str, system: str = "", max_retries: int = 3) -> dict:
    client = get_client()

    system_prompt = system if system else (
        "You are a structured AI data analysis agent specializing in infrastructure and sustainability. "
        "You MUST respond with valid JSON only. "
        "Do NOT include markdown code fences, explanations, or any text outside the JSON object."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    for attempt in range(1, max_retries + 1):
        try:
            response = get_client().chat.completions.create(
                model=GROQ_MODEL,
                max_tokens=4096,
                messages=messages,
                temperature=0.4,
            )
            raw = response.choices[0].message.content.strip()
            raw = re.sub(r"^```(?:json)?\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw)
            raw = raw.strip()
            parsed = json.loads(raw)
            return {"success": True, "data": parsed, "raw": raw}

        except json.JSONDecodeError as e:
            if attempt == max_retries:
                return {"success": False, "error": f"JSON parse failed: {str(e)}", "raw": raw if "raw" in locals() else ""}
            time.sleep(1)

        except Exception as e:
            return {"success": False, "error": str(e), "raw": ""}

    return {"success": False, "error": "Unknown failure", "raw": ""}
