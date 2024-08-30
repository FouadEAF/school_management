from django.urls import path
from .views import ManageCohortView, ManageClasseView, ManageMaterialView, ManageSalleFormationView, ManageSeanceView

urlpatterns = [
    # Paths for Cohort management
    path('cohort', ManageCohortView.as_view()),
    path('cohort/<int:id_cohort>', ManageCohortView.as_view()),

    # Paths for Classe management
    path('classe', ManageClasseView.as_view()),
    path('classe/<int:id_classe>', ManageClasseView.as_view()),

    # Paths for Material management
    path('material', ManageMaterialView.as_view()),
    path('material/<int:id_material>', ManageMaterialView.as_view()),

    # Paths for SalleFormation management
    path('salle_formation', ManageSalleFormationView.as_view()),
    path('salle_formation/<int:id_salle>', ManageSalleFormationView.as_view()),

    # Paths for Seance management
    path('seance', ManageSeanceView.as_view()),
    path('seance/<int:id_seance>', ManageSeanceView.as_view()),
]
