from .models import Absence, Student, Note
from teachers.models import Matiere, Teacher
from school.models import Classe
from django.http import JsonResponse
from django.views import View
from django.forms.models import model_to_dict
import json

from .models import Student


class ManageStudentView(View):

    def get(self, request, id_student=None):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

        try:
            if id_student:
                student = Student.objects.get(pk=id_student)
                student_dict = model_to_dict(student)
                return JsonResponse({'success': True, 'data': student_dict}, status=200)
            else:
                students = Student.objects.all()
                students_list = [model_to_dict(student)
                                 for student in students]
                return JsonResponse({'success': True, 'data': students_list}, status=200)
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'No student found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {e}'}, status=500)

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

        try:
            data = json.loads(request.body)
            student_name = data.get('student_name', '')
            info_contact = data.get('info_contact', '')
            birthday = data.get('birthday', '')

            if not student_name or not birthday:
                return JsonResponse({'success': False, 'message': 'Missing student_name or birthday'}, status=400)

            if Student.objects.filter(student_name=student_name, birthday=birthday).exists():
                return JsonResponse({'success': False, 'message': 'Student with the same name and birthday already exists'}, status=400)

            student = Student.objects.create(
                student_name=student_name,
                info_contact=info_contact,
                birthday=birthday,
            )
            return JsonResponse({'success': True, 'message': 'Student added successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def put(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')

            if not student_id:
                return JsonResponse({'success': False, 'message': 'Student ID not provided'}, status=400)

            student = Student.objects.get(pk=student_id)
            student.student_name = data.get(
                'student_name', student.student_name)
            student.info_contact = data.get(
                'info_contact', student.info_contact)
            student.birthday = data.get('birthday', student.birthday)
            student.save()

            return JsonResponse({'success': True, 'message': 'Student updated successfully'}, status=200)
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Student not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def delete(self, request, id_student=None):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

        try:
            student = Student.objects.get(pk=id_student)
            student.delete()
            return JsonResponse({'success': True, 'message': 'Student deleted successfully'}, status=200)
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Student not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)


class ManageNoteView(View):

    def get(self, request, id_note=None):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

        try:
            if id_note:
                note = Note.objects.get(pk=id_note)
                note_dict = model_to_dict(note)
                return JsonResponse({'success': True, 'data': note_dict}, status=200)
            else:
                notes = Note.objects.all()
                notes_list = [model_to_dict(note) for note in notes]
                return JsonResponse({'success': True, 'data': notes_list}, status=200)
        except Note.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'No note found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {e}'}, status=500)

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

        try:
            data = json.loads(request.body)
            types = data.get('types', '')
            note_value = data.get('note', 0)
            classe_id = data.get('classe_id', 0)
            teacher_id = data.get('teacher_id', 0)
            matiere_id = data.get('matiere_id', 0)
            student_id = data.get('student_id', 0)

            if not types or not note_value:
                return JsonResponse({'success': False, 'message': 'Missing types or note'}, status=400)

            try:
                teacher = Teacher.objects.get(pk=teacher_id)
            except Teacher.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'No teacher found'}, status=404)

            try:
                classe = Classe.objects.get(pk=classe_id)
            except Classe.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'No classe found'}, status=404)

            try:
                matiere = Matiere.objects.get(pk=matiere_id)
            except Matiere.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'No matiere found'}, status=404)

            try:
                student = Student.objects.get(pk=student_id)
            except Student.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'No student found'}, status=404)

            if Note.objects.filter(types=types, note=note_value, classe=classe, teacher=teacher, matiere=matiere, student=student).exists():
                return JsonResponse({'success': False, 'message': 'Note with the same details already exists'}, status=400)

            note = Note.objects.create(
                types=types,
                note=note_value,
                classe=classe,
                teacher=teacher,
                matiere=matiere,
                student=student,
            )
            return JsonResponse({'success': True, 'message': 'Note added successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def put(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

        try:
            data = json.loads(request.body)
            note_id = data.get('note_id')

            if not note_id:
                return JsonResponse({'success': False, 'message': 'Note ID not provided'}, status=400)

            note = Note.objects.get(pk=note_id)
            note.types = data.get('types', note.types)
            note.note = data.get('note', note.note)
            note.classe_id = data.get('classe_id', note.classe_id)
            note.teacher_id = data.get('teacher_id', note.teacher_id)
            note.matiere_id = data.get('matiere_id', note.matiere_id)
            note.student_id = data.get('student_id', note.student_id)
            note.save()

            return JsonResponse({'success': True, 'message': 'Note updated successfully'}, status=200)
        except Note.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Note not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def delete(self, request, id_note=None):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

        try:
            note = Note.objects.get(pk=id_note)
            note.delete()
            return JsonResponse({'success': True, 'message': 'Note deleted successfully'}, status=200)
        except Note.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Note not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)


class ManageAbsenceView(View):

    def get(self, request, id_absence=None):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

        try:
            if id_absence:
                absence = Absence.objects.get(pk=id_absence)
                absence_dict = model_to_dict(absence)
                return JsonResponse({'success': True, 'data': absence_dict}, status=200)
            else:
                absences = Absence.objects.all()
                absences_list = [model_to_dict(absence)
                                 for absence in absences]
                return JsonResponse({'success': True, 'data': absences_list}, status=200)
        except Absence.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'No absence found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {e}'}, status=500)

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

        try:
            data = json.loads(request.body)
            student_id = data.get('student_id', 0)
            classe_id = data.get('classe_id', 0)
            absence_date = data.get('absence_date', '')
            reason = data.get('reason', '')

            if not student_id or not absence_date:
                return JsonResponse({'success': False, 'message': 'Missing student_id or absence_date'}, status=400)

            try:
                student = Student.objects.get(pk=student_id)
            except Student.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'No student found'}, status=404)

            try:
                classe = Classe.objects.get(pk=classe_id)
            except Classe.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'No classe found'}, status=404)

            absence = Absence.objects.create(
                student=student,
                classe=classe,
                absence_date=absence_date,
                reason=reason,
            )
            return JsonResponse({'success': True, 'message': 'Absence added successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def put(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

        try:
            data = json.loads(request.body)
            absence_id = data.get('absence_id')

            if not absence_id:
                return JsonResponse({'success': False, 'message': 'Absence ID not provided'}, status=400)

            absence = Absence.objects.get(pk=absence_id)
            absence.student_id = data.get('student_id', absence.student_id)
            absence.classe_id = data.get('classe_id', absence.classe_id)
            absence.absence_date = data.get(
                'absence_date', absence.absence_date)
            absence.reason = data.get('reason', absence.reason)
            absence.save()

            return JsonResponse({'success': True, 'message': 'Absence updated successfully'}, status=200)
        except Absence.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Absence not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def delete(self, request, id_absence=None):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

        try:
            absence = Absence.objects.get(pk=id_absence)
            absence.delete()
            return JsonResponse({'success': True, 'message': 'Absence deleted successfully'}, status=200)
        except Absence.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Absence not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
