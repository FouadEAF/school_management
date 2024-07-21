# views.py
import json
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from .models import Matiere, Teacher, Diplome, TeacherMatiere
from django.shortcuts import get_object_or_404


@csrf_exempt
def manage_teacher(request, id_teacher=None):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

    if request.method == 'GET':
        """Retrieve teachers"""
        try:
            if id_teacher:
                # Retrieve a specific teacher and their diplomas
                teacher = Teacher.objects.get(pk=id_teacher)
                diplomes = Diplome.objects.filter(teacher=teacher)
                diplomes_list = [
                    {'option': diplome.option, 'annee_obtenu': diplome.annee_obtenu}
                    for diplome in diplomes
                ]
                teacher_dict = model_to_dict(teacher)
                teacher_dict['diplome'] = diplomes_list
                return JsonResponse({'success': True, 'data': teacher_dict}, status=200)
            else:
                # Retrieve all teachers with their diplomas
                teachers = Teacher.objects.all()
                teachers_list = []
                for teacher in teachers:
                    diplomes_list = [
                        {'option': diplome.option,
                            'annee_obtenu': diplome.annee_obtenu}
                        for diplome in Diplome.objects.filter(teacher=teacher)
                    ]
                    teacher_dict = model_to_dict(teacher)
                    teacher_dict['diplome'] = diplomes_list
                    teachers_list.append(teacher_dict)
                return JsonResponse({'success': True, 'data': teachers_list}, status=200)

        except Teacher.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'No Teacher found'}, status=404)

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)

    elif request.method == 'POST':
        """Add new teacher"""
        try:
            data = json.loads(request.body)

            diplom_data = data.pop('diplome', [])
            full_name = data.get('full_name', '')
            cnie = data.get('cnie', '')
            telephone = data.get('telephone', '')
            date_admission = data.get('date_admission', '')
            date_demission = data.get('date_demission', '')
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)

        try:
            # Check if a teacher with the same name or CNIE already exists
            if Teacher.objects.filter(cnie=cnie, full_name=full_name).exists():
                return JsonResponse({'success': False, 'message': 'Teacher with the same name or CNIE already exists'}, status=400)

            # Create the teacher instance
            teacher = Teacher.objects.create(
                full_name=full_name,
                cnie=cnie,
                telephone=telephone,
                date_admission=date_admission,
                date_demission=date_demission,
            )

            # Add diplomes to the teacher
            if diplom_data:
                for diplome_info in diplom_data:
                    option = diplome_info.get('option')
                    annee_obtenu = diplome_info.get('annee_obtenu')

                    # Check if diplome already exists for the teacher
                    diplome, created = Diplome.objects.get_or_create(
                        option=option,
                        annee_obtenu=annee_obtenu,
                        teacher=teacher
                    )
            return JsonResponse({'success': True, 'message': 'Teacher added successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    elif request.method == 'PUT':
        """Update a teacher"""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)

        try:
            teacher_id = data.get('teacher_id')
            if teacher_id is not None:
                # Retrieve the teacher instance
                teacher = Teacher.objects.get(pk=teacher_id)

                # Update teacher fields if provided in the request
                teacher.full_name = data.get('full_name', teacher.full_name)
                teacher.cnie = data.get('cnie', teacher.cnie)
                teacher.telephone = data.get('telephone', teacher.telephone)
                teacher.date_admission = data.get(
                    'date_admission', teacher.date_admission)
                teacher.date_demission = data.get(
                    'date_demission', teacher.date_demission)
                teacher.save()

                # Update or create diplome instances associated with this teacher
                diplome_data = data.get('diplome', [])
                for diplome_info in diplome_data:
                    option = diplome_info.get('option')
                    annee_obtenu = diplome_info.get('annee_obtenu')

                    # Check if diplome already exists for the teacher
                    diplome, created = Diplome.objects.get_or_create(
                        teacher=teacher,
                        option=option,
                        defaults={'annee_obtenu': annee_obtenu}
                    )

                    # Update diplome if it already exists
                    if not created:
                        diplome.annee_obtenu = annee_obtenu
                        diplome.save()

                return JsonResponse({'success': True, 'message': 'Teacher updated successfully'}, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Teacher ID not provided'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    elif request.method == 'DELETE':
        """Delete a Teacher"""
        try:
            deleted_teacher = Teacher.delete(id_teacher)
            if deleted_teacher:
                return JsonResponse({'success': True, 'message': 'Teacher deleted successfully'}, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Teacher not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)


@csrf_exempt
def manage_matiere(request, id_matiere=None):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

    if request.method == 'GET':
        """Retrieve Matieres"""
        try:
            if id_matiere:
                # Retrieve a specific matiere
                matiere = Matiere.objects.get(pk=id_matiere)
                matiere_dict = model_to_dict(matiere)
                return JsonResponse({'success': True, 'data': matiere_dict}, status=200)
            else:
                # Retrieve all matieres
                matieres = Matiere.objects.all()
                matieres_list = [model_to_dict(matiere)
                                 for matiere in matieres]
                return JsonResponse({'success': True, 'data': matieres_list}, status=200)

        except Matiere.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Matiere not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)

    elif request.method == 'POST':
        """Add new Matiere"""
        try:
            data = json.loads(request.body)
            matiere_name = data.get('matiere_name', '')
            duree_program = data.get('duree_program', '')
            teacher_id = data.get('teacher_id', 0)

            if not matiere_name or not duree_program:
                return JsonResponse({'success': False, 'message': 'Missing matiere_name or duree_program'}, status=400)

            # Check if a teacher exists
            try:
                teacher = Teacher.objects.get(pk=teacher_id)
            except Teacher.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'No teacher found'}, status=404)

            # Check if a matiere exists with the same name and duration
            matiere = Matiere.objects.filter(
                matiere_name=matiere_name, duree_program=duree_program).first()

            # Check if a matiere with the same teacher already exists
            if matiere and TeacherMatiere.objects.filter(teacher=teacher, matiere=matiere).exists():
                return JsonResponse({'success': False, 'message': 'Matiere with the same name and duration already exists for this teacher'}, status=400)

            if not matiere:
                # Create the new Matiere if it does not exist
                matiere = Matiere.objects.create(
                    matiere_name=matiere_name,
                    duree_program=duree_program,
                )

            # Create the TeacherMatiere relationship
            TeacherMatiere.objects.create(
                teacher=teacher,
                matiere=matiere,
            )

            return JsonResponse({'success': True, 'message': 'Matiere added successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    elif request.method == 'PUT':
        """Update a Matiere"""
        try:
            data = json.loads(request.body)
            matiere_id = data.get('matiere_id')
            teacher_id = data.get('teacher_id')

            if not matiere_id:
                return JsonResponse({'success': False, 'message': 'Matiere ID not provided'}, status=400)

            if not teacher_id:
                return JsonResponse({'success': False, 'message': 'Teacher ID not provided'}, status=400)

            # Check if a teacher exists
            try:
                teacher = Teacher.objects.get(pk=teacher_id)
            except Teacher.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'No teacher found'}, status=404)

            # Retrieve the matiere instance
            try:
                matiere = Matiere.objects.get(pk=matiere_id)
            except Matiere.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Matiere not found'}, status=404)

            # Update matiere fields if provided in the request
            matiere.matiere_name = data.get(
                'matiere_name', matiere.matiere_name)
            matiere.duree_program = data.get(
                'duree_program', matiere.duree_program)
            matiere.save()

            # Check if the teacher-matiere relationship exists
            teacher_matiere, created = TeacherMatiere.objects.get_or_create(
                teacher=teacher, matiere=matiere)

            if not created:
                teacher_matiere.save()

            return JsonResponse({'success': True, 'message': 'Matiere updated successfully'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    elif request.method == 'DELETE':
        """Delete a Matiere"""
        try:
            matiere = Matiere.delete(id_matiere)
            if matiere:
                return JsonResponse({'success': True, 'message': 'Matiere deleted successfully'}, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Matiere not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)


# ===========================================================================================
# @csrf_exempt
# def manage_diplome(request, id_diplome=None):
#     if request.method == 'GET':
#         """Retrieve Diplomes"""
#         try:
#             if id_diplome:
#                 # Retrieve a specific teacher and their diplomas

#                 diplome = Diplome.objects.filter(pk=id_diplome)

#                 diplome_dict = model_to_dict(diplome)

#                 return JsonResponse({'success': True, 'data': diplome_dict}, status=200)
#             else:
#                 # Retrieve all teachers with their diplomas
#                 diplomes = Diplome.objects.all()
#                 diplomes_dict = model_to_dict(diplomes)
#                 return JsonResponse({'success': True, 'data': diplomes_dict}, status=200)

#         except Diplome.DoesNotExist:
#             return JsonResponse({'success': False, 'message': 'No Diplome found'}, status=404)

#         except Exception as e:
#             return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)

#     elif request.method == 'POST':
#         """Add new Diplome"""
#         try:
#             data = json.loads(request.body)

#             teacher_id = data.get('teacher', '')
#             option = data.get('option', '')
#             annee_obtenu = data.get('annee_obtenu', '')
#         except json.JSONDecodeError:
#             return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)

#         try:
#             # Check if a teacher with the same name or CNIE already exists
#             teacher = Teacher.objects.filter(pk=teacher_id).first()

#             # Check if diplome already exists for the teacher
#             diplome, created = Diplome.objects.get_or_create(
#                 option=option,
#                 annee_obtenu=annee_obtenu,
#                 teacher=teacher
#             )
#             return JsonResponse({'success': True, 'message': 'Diplome added successfully'}, status=201)
#         except Exception as e:
#             return JsonResponse({'success': False, 'message': str(e)}, status=400)

#     elif request.method == 'PUT':
#         """Update a Diplome"""
#         try:
#             data = json.loads(request.body)
#         except json.JSONDecodeError:
#             return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)

#         try:
#             diplome_id = data.get('diplome_id')
#             if diplome_id is not None:
#                 # Retrieve the teacher instance
#                 diplome = Diplome.objects.get(pk=diplome_id)

#                 # Update teacher fields if provided in the request
#                 diplome.option = data.get('option', teacher.option)
#                 diplome.annee_obtenu = data.get(
#                     'annee_obtenu', teacher.annee_obtenu)

#                 diplome.save()

#                 return JsonResponse({'success': True, 'message': 'Diplome updated successfully'}, status=200)
#             else:
#                 return JsonResponse({'success': False, 'message': 'Teacher ID not provided'}, status=400)
#         except Exception as e:
#             return JsonResponse({'success': False, 'message': str(e)}, status=400)

#     elif request.method == 'DELETE':
#         """Delete a Teacher"""
#         try:
#             deleted_diplome = Diplome.delete(id_diplome)
#             if deleted_diplome:
#                 return JsonResponse({'success': True, 'message': 'Diplome deleted successfully'}, status=200)
#             else:
#                 return JsonResponse({'success': False, 'message': 'Diplome not found'}, status=404)
#         except Exception as e:
#             return JsonResponse({'success': False, 'message': str(e)}, status=400)

#     else:
#         return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
