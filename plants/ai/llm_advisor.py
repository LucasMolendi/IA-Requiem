import os
import json
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """
Tu es un expert agronome et maraîcher connecté à des capteurs IoT.
Tu analyses les données de cultures et de capteurs pour conseiller un agriculteur.
Tu dois répondre UNIQUEMENT en JSON valide, sans markdown, sans explication, avec ce format exact :

{
  "health_score": 75,
  "status": "drought_stress",
  "status_label": "Stress hydrique",
  "advice": "Vos tomates manquent d'eau..."
}

Valeurs possibles pour status :
healthy | drought_stress | overwatered | light_deficiency | heat_stress | nutrient_deficiency | disease_risk
"""

def analyze_and_advise(plant: dict, plants_user: dict, capteurs: dict) -> dict:
    user_message = f"""
Culture : {plant['nom']} (type: {plant['type']})
Besoin en eau : {plant['besoin_eau']}
Ensoleillement requis : {plant['ensoleillement']}
Saisons : {', '.join(plant['saison'])}
Croissance : {plant['croissance_jours']} jours

Informations parcelle :
- Date de plantation : {plants_user['date_plantation']}
- Surface : {plants_user['surface_m2']} m²
- État actuel : {plants_user['etat']}

Données capteurs en temps réel :
- Humidité du sol : {capteurs['humidity']}%
- Humidité de l'air : {capteurs['air_humidity']}%
- Température : {capteurs['temperature']}°C
- Luminosité : {capteurs['light_level']} lux

Analyse et génère ton conseil JSON.
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