from django.urls import path, include


urlpatterns = [
    path('observation/', include('observation.urls'), name = 'observation'),
    path('referential/', include('referential.urls'), name = 'referential')
]
