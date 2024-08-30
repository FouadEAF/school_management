from django.urls import path
from .views import ManageStudentView, ManageNoteView, ManageAbsenceView

urlpatterns = [
    # Student paths
    path('', ManageStudentView.as_view()),
    path('<int:id_student>', ManageStudentView.as_view()),

    # Notes paths
    path('notes', ManageNoteView.as_view()),
    path('notes/<int:id_note>', ManageNoteView.as_view()),

    # Absence paths
    path('absences', ManageAbsenceView.as_view()),
    path('absences/<int:id_absence>', ManageAbsenceView.as_view()),
]
