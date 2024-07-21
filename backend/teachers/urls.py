from django.urls import path
from .views import manage_teacher, manage_matiere  # , manage_diplome

urlpatterns = [
    # Teacher path
    path('', manage_teacher, name='create_teacher'),
    path('<int:id_teacher>', manage_teacher, name='manage_teacher'),
    # path('<int:id_teacher>/diplomes', manage_diplome, name='diplome-list-create'),

    # Matiere path
    path('matiere/', manage_matiere, name='create_matiere'),
    path('matiere/<int:id_matiere>', manage_matiere, name='manage_matiere'),
]
