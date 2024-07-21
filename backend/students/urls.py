from django.urls import path
from . import views

urlpatterns = [
    # Student paths
    path('', views.manage_student, name='student_create'),
    path('<int:id_student>', views.manage_student, name='manage_student'),

    # Notes paths
    path('notes/', views.manage_note, name='student_create'),
    path('notes/<int:id_note>', views.manage_note, name='manage_note'),

    # Absence paths
    path('absences/', views.manage_absence, name='student_create'),
    path('absences/<int:id_absence>',
         views.manage_absence, name='manage_absence'),
]
