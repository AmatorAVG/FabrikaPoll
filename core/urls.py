from django.urls import path, include
from .views import survey_list_api, answer_list_api, register_answer


urlpatterns = [
    path('active_surveys/', survey_list_api),
    path('answers/<int:author>/', answer_list_api),
    path('answer/', register_answer),
]
