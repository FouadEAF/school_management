from django.urls import path, include, re_path
from . import views

app_name = 'api'

urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('school/', include('school.urls')),
    path('teacher/', include('teachers.urls')),
    path('student/', include('students.urls')),
    path('calendrier/', include('calendrier.urls')),

    # Catch-all route for invalid paths within api/v1/
    re_path(r'^(?P<invalid_path>.*)$', views.invalid_route),
]
