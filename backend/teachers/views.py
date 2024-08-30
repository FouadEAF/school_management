# views.py
from .models import Matiere, Teacher, TeacherMatiere
from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Matiere, Teacher, Diplome, TeacherMatiere
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from authentication.utils import APIAccessMixin


class ManageTeacherView(APIAccessMixin, APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id_teacher=None):
        """Retrieve teachers"""
        # if not request.user.is_authenticated:
        #     return Response({'success': False, 'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

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
                return Response({'success': True, 'data': teacher_dict}, status=status.HTTP_200_OK)
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
                return Response({'success': True, 'data': teachers_list}, status=status.HTTP_200_OK)

        except Teacher.DoesNotExist:
            return Response({'success': False, 'message': 'No Teacher found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'message': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """Add new teacher"""
        # if not request.user.is_authenticated:
        #     return Response({'success': False, 'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            data = request.data

            diplom_data = data.pop('diplome', [])
            full_name = data.get('full_name', '')
            cnie = data.get('cnie', '')
            telephone = data.get('telephone', '')
            date_admission = data.get('date_admission', '')
            date_demission = data.get('date_demission', '')

            # Check if a teacher with the same name or CNIE already exists
            if Teacher.objects.filter(cnie=cnie, full_name=full_name).exists():
                return Response({'success': False, 'message': 'Teacher with the same name or CNIE already exists'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the teacher instance
            teacher = Teacher.objects.create(
                full_name=full_name,
                cnie=cnie,
                telephone=telephone,
                date_admission=date_admission,
                date_demission=date_demission,
            )

            # Add diplomes to the teacher
            for diplome_info in diplom_data:
                option = diplome_info.get('option')
                annee_obtenu = diplome_info.get('annee_obtenu')
                Diplome.objects.get_or_create(
                    option=option,
                    annee_obtenu=annee_obtenu,
                    teacher=teacher
                )
            return Response({'success': True, 'message': 'Teacher added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id_teacher=None):
        """Update a teacher"""
        # if not request.user.is_authenticated:
        #     return Response({'success': False, 'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            data = request.data
            # teacher_id = data.get('teacher_id')
            if id_teacher is None:
                return Response({'success': False, 'message': 'Teacher ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the teacher instance
            teacher = Teacher.objects.get(pk=id_teacher)

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

            return Response({'success': True, 'message': 'Teacher updated successfully'}, status=status.HTTP_200_OK)
        except Teacher.DoesNotExist:
            return Response({'success': False, 'message': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_teacher):
        """Delete a Teacher"""
        # if not request.user.is_authenticated:
        #     return Response({'success': False, 'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            teacher = Teacher.objects.get(pk=id_teacher)
            teacher.delete()
            return Response({'success': True, 'message': 'Teacher deleted successfully'}, status=status.HTTP_200_OK)
        except Teacher.DoesNotExist:
            return Response({'success': False, 'message': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ManageMatiereView(APIView):
    def get(self, request, id_matiere=None):
        """Retrieve Matieres"""
        # if not request.user.is_authenticated:
        #     return Response({'success': False, 'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            if id_matiere:
                # Retrieve a specific matiere
                matiere = Matiere.objects.get(pk=id_matiere)
                matiere_dict = model_to_dict(matiere)
                return Response({'success': True, 'data': matiere_dict}, status=status.HTTP_200_OK)
            else:
                # Retrieve all matieres
                matieres = Matiere.objects.all()
                matieres_list = [model_to_dict(matiere)
                                 for matiere in matieres]
                return Response({'success': True, 'data': matieres_list}, status=status.HTTP_200_OK)

        except Matiere.DoesNotExist:
            return Response({'success': False, 'message': 'Matiere not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'message': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """Add new Matiere"""
        # if not request.user.is_authenticated:
        #     return Response({'success': False, 'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            data = request.data
            matiere_name = data.get('matiere_name', '')
            duree_program = data.get('duree_program', '')
            teacher_id = data.get('teacher_id', 0)

            if not matiere_name or not duree_program:
                return Response({'success': False, 'message': 'Missing matiere_name or duree_program'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if a teacher exists
            teacher = Teacher.objects.get(pk=teacher_id)

            # Check if a matiere exists with the same name and duration
            matiere = Matiere.objects.filter(
                matiere_name=matiere_name, duree_program=duree_program).first()

            # Check if a matiere with the same teacher already exists
            if matiere and TeacherMatiere.objects.filter(teacher=teacher, matiere=matiere).exists():
                return Response({'success': False, 'message': 'Matiere with the same name and duration already exists for this teacher'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the matiere instance
            if not matiere:
                matiere = Matiere.objects.create(
                    matiere_name=matiere_name, duree_program=duree_program)

            # Create TeacherMatiere association
            TeacherMatiere.objects.create(teacher=teacher, matiere=matiere)

            return Response({'success': True, 'message': 'Matiere added successfully'}, status=status.HTTP_201_CREATED)
        except Teacher.DoesNotExist:
            return Response({'success': False, 'message': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id_matiere=None):
        """Update a Matiere"""
        if not request.user.is_authenticated:
            return Response({'success': False, 'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            data = request.data
            # matiere_id = data.get('matiere_id')
            if not id_matiere:
                return Response({'success': False, 'message': 'Matiere ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the matiere instance
            matiere = Matiere.objects.get(pk=id_matiere)

            # Update matiere fields if provided in the request
            matiere.matiere_name = data.get(
                'matiere_name', matiere.matiere_name)
            matiere.duree_program = data.get(
                'duree_program', matiere.duree_program)
            matiere.save()

            # Update or create TeacherMatiere association if teacher_id is provided
            teacher_id = data.get('teacher_id')
            if teacher_id:
                teacher = Teacher.objects.get(pk=teacher_id)
                # Update or create the teacher-matiere relationship
                TeacherMatiere.objects.update_or_create(
                    teacher=teacher,
                    matiere=matiere,
                    defaults={'teacher': teacher, 'matiere': matiere}
                )

            return Response({'success': True, 'message': 'Matiere updated successfully'}, status=status.HTTP_200_OK)
        except Matiere.DoesNotExist:
            return Response({'success': False, 'message': 'Matiere not found'}, status=status.HTTP_404_NOT_FOUND)
        except Teacher.DoesNotExist:
            return Response({'success': False, 'message': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_matiere=None):
        """Delete a Matiere"""
        # if not request.user.is_authenticated:
        #     return Response({'success': False, 'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            matiere = Matiere.objects.get(pk=id_matiere)
            matiere.delete()
            return Response({'success': True, 'message': 'Matiere deleted successfully'}, status=status.HTTP_200_OK)
        except Matiere.DoesNotExist:
            return Response({'success': False, 'message': 'Matiere not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
