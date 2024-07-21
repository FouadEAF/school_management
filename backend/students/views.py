from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json

from school.models import Classe, Seance
from teachers.models import Matiere, Teacher
from .models import Absence, Note, Student


@csrf_exempt
def manage_student(request, id_student=None):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

    if request.method == 'GET':
        """Retrieve students"""
        try:
            if id_student:
                # Retrieve a specific student
                student = Student.objects.get(pk=id_student)
                student_dict = model_to_dict(student)
                return JsonResponse({'success': True, 'data': student_dict}, status=200)
            else:
                # Retrieve all students
                students = Student.objects.all()
                students_list = [model_to_dict(student)
                                 for student in students]
                return JsonResponse({'success': True, 'data': students_list}, status=200)
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'No student found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {e}'}, status=500)

    elif request.method == 'POST':
        """Add new student"""
        try:
            data = json.loads(request.body)

            student_name = data.get('student_name', '')
            info_contact = data.get('info_contact', '')
            birthday = data.get('birthday', '')

            if not student_name or not birthday:
                return JsonResponse({'success': False, 'message': 'Missing student_name or birthday'}, status=400)

            # Check if a student with the same name and birthday already exists
            if Student.objects.filter(student_name=student_name, birthday=birthday).exists():
                return JsonResponse({'success': False, 'message': 'Student with the same name and birthday already exists'}, status=400)

            # Create the new student
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

    elif request.method == 'PUT':
        """Update a student"""
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')

            if not student_id:
                return JsonResponse({'success': False, 'message': 'Student ID not provided'}, status=400)

            # Retrieve the student instance
            student = Student.objects.get(pk=student_id)

            # Update student fields if provided in the request
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

    elif request.method == 'DELETE':
        """Delete a student"""
        try:
            student = Student.delete(id_student)
            if student:
                return JsonResponse({'success': True, 'message': 'Student deleted successfully'}, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Student not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)


@csrf_exempt
def manage_note(request, id_note=None):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

    if request.method == 'GET':
        # Retrieve notes for a specific student

        """Retrieve notes"""
        try:
            if id_note:
                try:
                    student = Student.objects.get(pk=id_note)
                except Student.DoesNotExist:
                    return JsonResponse({'success': False, 'message': 'No student found'}, status=404)

                notes = Note.objects.filter(student=student)
                notes_list = [model_to_dict(note) for note in notes]
                return JsonResponse({'success': True, 'data': notes_list}, status=200)

            else:
                # Retrieve all notes
                notes = Note.objects.all()
                notes_list = [model_to_dict(note) for note in notes]
                return JsonResponse({'success': True, 'data': notes_list}, status=200)
        except Note.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'No note found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {e}'}, status=500)

    elif request.method == 'POST':
        """Add new note"""
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

            # Validate and retrieve related models
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

            # Check if a note with the same student, classe, teacher, and matiere already exists
            if Note.objects.filter(types=types, note=note_value, classe=classe, teacher=teacher, matiere=matiere, student=student).exists():
                return JsonResponse({'success': False, 'message': 'Note with the same details already exists'}, status=400)

            # Create the new note
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

    elif request.method == 'PUT':
        """Update a note"""
        try:
            data = json.loads(request.body)
            note_id = data.get('note_id')

            if not note_id:
                return JsonResponse({'success': False, 'message': 'Note ID not provided'}, status=400)

            # Retrieve the note instance
            note = Note.objects.get(pk=note_id)

            # Update note fields if provided in the request
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

    elif request.method == 'DELETE':
        """Delete a note"""
        try:
            note = Note.delete(id_note)
            if note:
                return JsonResponse({'success': True, 'message': 'Note deleted successfully'}, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Note not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)


@csrf_exempt
def manage_absence(request, id_absence=None):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

    if request.method == 'GET':
        """Retrieve absences"""
        try:
            if id_absence:
                # Retrieve a specific absence
                absence = Absence.objects.get(pk=id_absence)
                absence_dict = model_to_dict(absence)
                return JsonResponse({'success': True, 'data': absence_dict}, status=200)
            else:
                # Retrieve all absences
                absences = Absence.objects.all()
                absences_list = [model_to_dict(absence)
                                 for absence in absences]
                return JsonResponse({'success': True, 'data': absences_list}, status=200)
        except Absence.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'No absence found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {e}'}, status=500)

    elif request.method == 'POST':
        """Add new absence"""
        try:
            data = json.loads(request.body)

            status = data.get('status', '')
            student_id = data.get('student_id', 0)
            seance_id = data.get('seance_id', 0)

            if not status or not student_id or not seance_id:
                return JsonResponse({'success': False, 'message': 'Missing status, student_id, or seance_id'}, status=400)

            # Validate and retrieve related models
            try:
                student = Student.objects.get(pk=student_id)
            except Student.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'No student found'}, status=404)

            try:
                seance = Seance.objects.get(pk=seance_id)
            except Seance.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'No seance found'}, status=404)

            # Check if an absence with the same student and seance already exists
            if Absence.objects.filter(student=student, seance=seance).exists():
                return JsonResponse({'success': False, 'message': 'Absence with the same student and seance already exists'}, status=400)

            # Create the new absence
            absence = Absence.objects.create(
                status=status,
                student=student,
                seance=seance,
            )
            return JsonResponse({'success': True, 'message': 'Absence added successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    elif request.method == 'PUT':
        """Update an absence"""
        try:
            data = json.loads(request.body)
            absence_id = data.get('absence_id')

            if not absence_id:
                return JsonResponse({'success': False, 'message': 'Absence ID not provided'}, status=400)

            # Retrieve the absence instance
            absence = Absence.objects.get(pk=absence_id)

            # Update absence fields if provided in the request
            absence.status = data.get('status', absence.status)
            absence.student_id = data.get('student_id', absence.student_id)
            absence.seance_id = data.get('seance_id', absence.seance_id)
            absence.save()

            return JsonResponse({'success': True, 'message': 'Absence updated successfully'}, status=200)
        except Absence.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Absence not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    elif request.method == 'DELETE':
        """Delete an absence"""
        try:
            absence = Absence.delete(id_absence)
            if absence:
                return JsonResponse({'success': True, 'message': 'Absence deleted successfully'}, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Absence not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
