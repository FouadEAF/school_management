from django.contrib import admin
from .models import Cohort, Classe, Material, SalleFormation, Seance, MaterialSalleFormation

admin.site.register(Cohort)
admin.site.register(Classe)
admin.site.register(Material)
admin.site.register(SalleFormation)
admin.site.register(Seance)
admin.site.register(MaterialSalleFormation)
