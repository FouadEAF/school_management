from django.urls import path
from .views import ManageCohortView

urlpatterns = [
    # Paths for Cohort management
    path('cohort', ManageCohortView.as_view(), name='manage_cohort'),
    path('cohort/<int:id_cohort>',
         ManageCohortView.as_view(), name='manage_cohort'),



    #     # Paths for Classe management
    #     path('classe',
    #          views.manage_classe, name='create_classe'),
    #     path('classe/<int:id_classe>',
    #          views.manage_classe, name='manage_classe'),

    #     # Paths for SalleFormation management
    #     path('salle', views.manage_salle_formation,
    #          name='manage_salle_formation'),
    #     path('salle/<int:id_salle>',
    #          views.manage_salle_formation, name='manage_salle_formation'),

    #     # Paths for Material management
    #     path('material', views.manage_material, name='manage_material'),
    #     path('material/<int:id_material>',
    #          views.manage_material, name='manage_material'),

    #     # Paths for MaterialSalleFormation management
    #     #     path('materialsalle/', views.manage_material_salle_formation,
    #     #          name='manage_material_salle_formation'),
    #     #     path('materialsalle/<int:id_material_salle_formation>/',
    #     #          views.manage_material_salle_formation, name='manage_material_salle_formation'),

    #     # Paths for Seance management
    #     path('seance', views.manage_seance, name='manage_seance'),
    #     path('seance/<int:id_seance>', views.manage_seance, name='manage_seance'),


]
