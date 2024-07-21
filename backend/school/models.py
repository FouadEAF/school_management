from django.db import models
from api.models import Helpers
from teachers.models import Matiere, Teacher


class Cohort(Helpers):
    cohort_name = models.CharField(max_length=50)
    cohort_year = models.CharField(max_length=20)

    def __str__(self):
        return self.cohort_name


class Classe(Helpers):
    cohort = models.ForeignKey(
        Cohort, on_delete=models.CASCADE, related_name='classes')
    class_name = models.CharField(max_length=100)
    level_classe = models.CharField(max_length=50)
    date_start = models.DateField()
    date_end = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.class_name} in cohort {self.cohort.cohort_name}'


class Material(Helpers):
    category = models.CharField(max_length=50)
    item = models.CharField(max_length=50)


class SalleFormation(Helpers):
    salle_name = models.CharField(max_length=40)
    capacity = models.CharField(max_length=10)
    etage = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f'Salle {self.salle_name} in floor {self.etage}'


class MaterialSalleFormation(Helpers):
    salle_formation = models.ForeignKey(
        SalleFormation, on_delete=models.CASCADE, related_name='material_salle_formations')
    material = models.ForeignKey(
        Material, on_delete=models.CASCADE, related_name='material_salle_formations')
    count_item = models.IntegerField()


class Seance(Helpers):
    date_seance = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    titre_module = models.CharField(max_length=100)
    titre_cour = models.CharField(max_length=200)
    effectif_present = models.IntegerField()
    effectif_absent = models.IntegerField()
    is_done = models.BooleanField(default=True)
    observations = models.CharField(max_length=250)
    classe = models.ForeignKey(
        Classe, on_delete=models.CASCADE, related_name='seances')
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name='seances')
    matiere = models.ForeignKey(
        Matiere, on_delete=models.CASCADE, related_name='seances')
    salle_formation = models.ForeignKey(
        SalleFormation, on_delete=models.CASCADE, related_name='seances')
