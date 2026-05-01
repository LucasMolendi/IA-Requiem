from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .ai.llm_advisor import analyze_and_advise, chat_with_context


class PlantAnalysisView(APIView):
    def post(self, request):
        try:
            data = request.data

            result = analyze_and_advise(
                plant=data['plant'],
                plants_user=data['plants_user'],
                capteurs=data['capteurs']
            )

            return Response(result, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response(
                {"error": f"Champ manquant : {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PlantChatView(APIView):
    def post(self, request):
        try:
            data = request.data

            question = data['message']
            context  = data['context']   # { plant, plants_user, capteurs }
            history  = data.get('history', [])  # [{ role, content }, ...]

            answer = chat_with_context(
                question=question,
                context=context,
                history=history
            )

            return Response({"answer": answer}, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response(
                {"error": f"Champ manquant : {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )