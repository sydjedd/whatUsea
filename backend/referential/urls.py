from django.urls import path
from . import views


urlpatterns = [
    path('', views.GetAll, name = 'all'),
    path('quality/', views.GetQuality, name = 'quality'),
    path('family/', views.GetFamily, name = 'family'),
    path('species/', views.GetSpecies, name = 'species')
]
