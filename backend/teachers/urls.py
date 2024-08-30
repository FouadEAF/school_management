# urls.py
from django.urls import path
from .views import ManageTeacherView, ManageMatiereView

urlpatterns = [
    path('', ManageTeacherView.as_view()),
    path('<int:id_teacher>', ManageTeacherView.as_view()),
    path('matieres', ManageMatiereView.as_view()),
    path('matieres/<int:id_matiere>', ManageMatiereView.as_view()),
]
