from django.urls import path
from .views import PlantAnalysisView, PlantChatView

urlpatterns = [
    path('analyze/', PlantAnalysisView.as_view(), name='plant-analyze'),
    path('chat/',    PlantChatView.as_view(),    name='plant-chat'),
]