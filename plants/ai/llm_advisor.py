import os
import json
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """
Tu es un expert botaniste connecté à des capteurs IoT de plantes.
Tu reçois des données brutes et tu dois répondre UNIQUEMENT en JSON valide,
sans markdown, sans explication, avec ce format exact :

{
  "health_score": 75,
  "status": "drought_stress",
  "status_label": "Stress hydrique",
  "advice": "Votre plante manque d'eau..."
}

Valeurs possibles pour status :
healthy | drought_stress | overwatered | light_deficiency | heat_stress | nutrient_deficiency
"""

def analyze_and_advise(plant_name: str, species: str, reading: dict) -> dict:
    user_message = f"""
Plante : {plant_name} ({species})

Données capteurs :
- Humidité du sol : {reading['humidity']}%
- Humidité de l'air : {reading['air_humidity']}%
- Température : {reading['temperature']}°C
- Luminosité : {reading['light_level']} lux
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
            max_tokens=400
        )

        raw = response.choices[0].message.content
        result = json.loads(raw)
        return result

    except json.JSONDecodeError:
        return {
            "health_score": 50,
            "status": "unknown",
            "status_label": "Analyse indisponible",
            "advice": "Impossible d'analyser les données. Réessaie dans quelques instants."
        }
    except Exception as e:
        raise RuntimeError(f"Erreur API Groq : {str(e)}")