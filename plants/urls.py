from django.urls import path
from .views import PlantAnalysisView

urlpatterns = [
    path('analyze/', PlantAnalysisView.as_view(), name='analyze'),
]