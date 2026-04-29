from django.urls import path
from .views import PlantAnalysisView

urlpatterns = [
    path('plants/<int:plant_id>/analyze/', PlantAnalysisView.as_view(), name='plant-analysis'),
]