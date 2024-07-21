from django.db import models

from api.models import Helpers


class Teacher(Helpers):
    full_name = models.CharField(max_length=50)
    cnie = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50)
    date_admission = models.CharField(max_length=50)
    date_demission = models.CharField(max_length=50, null=True, blank=True)


class Diplome(Helpers):
    option = models.CharField(max_length=50)
    annee_obtenu = models.CharField(max_length=50)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name='diplomes')


class Matiere(Helpers):
    matiere_name = models.CharField(max_length=50)
    duree_program = models.CharField(max_length=50)


class TeacherMatiere(Helpers):  # Changed name to follow Python naming conventions
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name='teacher_matieres')
    matiere = models.ForeignKey(
        Matiere, on_delete=models.CASCADE, related_name='teacher_matieres')

    def __str__(self):
        return f'{self.teacher.full_name} teaches {self.matiere.matiere_name}'
