# urls.py

from django.urls import path
from .views import get_assessment_wizard_view, HomeWizard, evaluation_result

urlpatterns = [
    path("", HomeWizard.as_view(), name="home_wizard"),
    path("avaliacao/", get_assessment_wizard_view, name="avaliacao_wizard"),
    path("resultado/<uuid:evaluation_id>/", evaluation_result, name="evaluation_result"),
]
