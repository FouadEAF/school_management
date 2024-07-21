from django.contrib import admin
from .models import Teacher, Diplome, Matiere, TeacherMatiere

admin.site.register(Teacher)
admin.site.register(Diplome)
admin.site.register(Matiere)
admin.site.register(TeacherMatiere)
