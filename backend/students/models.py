from django.db import models
from config.api.models import Helpers
from school.models import Classe, Seance
from teachers.models import Matiere, Teacher


class Student(Helpers):
    student_name = models.CharField(max_length=100)
    info_contact = models.CharField(max_length=100)
    birthday = models.DateField()


class Absence(Helpers):
    status = models.CharField(max_length=20)
    reason = models.CharField(max_length=200)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='absences')
    seance = models.ForeignKey(
        Seance, on_delete=models.CASCADE, related_name='absences')


class Note(Helpers):
    types = models.CharField(max_length=20)
    note = models.FloatField()
    classe = models.ForeignKey(
        Classe, on_delete=models.CASCADE, related_name='notes')
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name='notes')
    matiere = models.ForeignKey(
        Matiere, on_delete=models.CASCADE, related_name='notes')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='notes')


class StudentMatiere(Helpers):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='student_matieres')
    matiere = models.ForeignKey(
        Matiere, on_delete=models.CASCADE, related_name='student_matieres')

    def __str__(self):
        return f'{self.student.student_name} studies {self.matiere.matiere_name}'


class StudentClasse(Helpers):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='student_classes')
    classe = models.ForeignKey(
        Classe, on_delete=models.CASCADE, related_name='student_classes')
