from django.urls import path
from .views import manage_calendrier

urlpatterns = [

    path('', manage_calendrier, name='calendrier_create'),
    path('<int:id_calendrier>/',
         manage_calendrier, name='manage_calendrier'),
]
