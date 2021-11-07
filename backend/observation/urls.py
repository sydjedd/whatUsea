from django.urls import path
from . import views


urlpatterns = [
    path('<int:id>', views.Main, name = 'observation with id'),
    path('', views.Main, name = 'observations'),
]
