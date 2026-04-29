from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Plant, PlantReading, AIAdvice
from .ai.llm_advisor import analyze_and_advise


class PlantAnalysisView(APIView):
    def post(self, request, plant_id):
        try:
            plant = Plant.objects.get(id=plant_id)
            data = request.data

            # Appel à l'IA
            result = analyze_and_advise(
                plant_name=plant.name,
                species=plant.species,
                reading=data
            )

            # Sauvegarder la lecture
            reading = PlantReading.objects.create(
                plant=plant,
                humidity=data['humidity'],
                air_humidity=data['air_humidity'],
                temperature=data['temperature'],
                light_level=data['light_level'],
                health_score=result['health_score'],
                health_status=result['status']
            )

            # Sauvegarder le conseil
            AIAdvice.objects.create(
                reading=reading,
                advice_text=result['advice']
            )

            return Response(result, status=status.HTTP_200_OK)

        except Plant.DoesNotExist:
            return Response(
                {"error": "Plante introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )