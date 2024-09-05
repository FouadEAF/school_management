from django.urls import path
from .views import CalendrierView

urlpatterns = [
    path('', CalendrierView.as_view()),
    path('<int:id_calendrier>', CalendrierView.as_view()),
]
