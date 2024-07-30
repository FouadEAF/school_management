from django.core.exceptions import ValidationError
from teachers.models import Matiere, Teacher
import json
from django.forms.models import model_to_dict
from .models import Classe, Cohort, Material, SalleFormation, MaterialSalleFormation, Seance
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from django.utils.decorators import method_decorator
from .serializers import CohortSerializer


@method_decorator(csrf_exempt, name='dispatch')
class ManageCohortView(APIView):
    """Manage Cohort in school"""
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id_cohort=None, *args, **kwargs):
        """Call a cohort"""
        try:
            if id_cohort:
                cohort = Cohort.objects.get(pk=id_cohort)
                serializer = CohortSerializer(cohort)
                return Response({'success': True, 'data': serializer.data}, status=200)
            else:
                cohorts = Cohort.objects.all()
                serializer = CohortSerializer(cohorts, many=True)
                return Response({'success': True, 'data': serializer.data}, status=200)
        except Cohort.DoesNotExist:
            return Response({'success': False, 'message': 'No cohort found'}, status=404)
        except Exception as e:
            return Response({'success': False, 'message': f'Error: {e}'}, status=500)

    def post(self, request, *args, **kwargs):
        """Add new cohort"""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({'success': False, 'message': 'Invalid JSON data'}, status=400)

        serializer = CohortSerializer(data=data)
        if serializer.is_valid():
            unique_fields = {
                'cohort_name': data['cohort_name'],
                'cohort_year': data['cohort_year']
            }

            if Cohort.objects.filter(**unique_fields).exists():
                return Response({'success': False, 'message': 'Cohort with the same name and year already exists'}, status=400)

            serializer.save()
            return Response({'success': True, 'message': 'Cohort added successfully'}, status=201)
        return Response({'success': False, 'message': serializer.errors}, status=400)

    def put(self, request, id_cohort, *args, **kwargs):
        """Update a cohort"""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({'success': False, 'message': 'Invalid JSON data'}, status=400)

        if not id_cohort:
            return Response({'success': False, 'message': 'Cohort ID is required'}, status=400)

        try:
            cohort = Cohort.objects.get(pk=id_cohort)
            serializer = CohortSerializer(cohort, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'success': True, 'message': 'Cohort updated successfully'}, status=200)
            return Response({'success': False, 'message': serializer.errors}, status=400)
        except Cohort.DoesNotExist:
            return Response({'success': False, 'message': 'Cohort not found'}, status=404)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)

    def delete(self, request, id_cohort, *args, **kwargs):
        """Delete a cohort"""
        try:
            if not id_cohort:
                return Response({'success': False, 'message': 'Cohort ID is required'}, status=400)

            cohort = Cohort.objects.filter(pk=id_cohort).delete()
            if cohort[0]:
                return Response({'success': True, 'message': 'Cohort deleted successfully'}, status=200)
            else:
                return Response({'success': False, 'message': 'Cohort not found'}, status=404)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)


@ csrf_exempt
def manage_classe(request, id_classe=None):
    if not request.user.is_authenticated:
        return Response({'success': False, 'message': 'User is not authenticated'}, status=401)

    if request.method == 'GET':
        """Call a classe"""
        try:
            if id_classe:
                classe = Classe.objects.get(pk=id_classe)
                classe_dict = model_to_dict(classe)
                return Response({'success': True, 'data': classe_dict}, status=200)
            else:
                classes = Classe.get_all()
                classes_list = [model_to_dict(classe) for classe in classes]
                return Response({'success': True, 'data': classes_list}, status=200)
        except Classe.DoesNotExist:
            return Response({'success': False, 'message': 'No classe found'}, status=404)
        except Exception as e:
            return Response({'success': False, 'message': f'Error: {e}'}, status=500)

    elif request.method == 'POST':
        """Add new classe"""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({'success': False, 'message': 'Invalid JSON data'}, status=400)

        try:
            # Validate the cohort
            cohort_id = data['cohort']
            cohort = Cohort.objects.filter(pk=cohort_id).first()

            if not cohort:
                return Response({'success': False, 'message': 'Invalid cohort'}, status=400)

            # Check if a classe with the same unique fields already exists
            unique_fields = {'class_name': data.get(
                'class_name'), 'cohort': cohort}
            if Classe.objects.filter(**unique_fields).exists():
                return Response({'success': False, 'message': 'Classe with the same name already exists for this cohort'}, status=400)

            # Create the new Classe instance
            data['cohort'] = cohort

            # Handle optional date_end
            date_end = data.get('date_end')
            if date_end == '':
                data['date_end'] = None

            # Create the Classe instance
            # classe_created = Classe.objects.create(**data)
            classe_created = cohort.classes.create(**data)

            if classe_created:
                return Response({'success': True, 'message': 'Classe added successfully'}, status=201)
            else:
                return Response({'success': False, 'message': 'Failed to add classe'}, status=400)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)

    elif request.method == 'PUT':
        """Update a classe"""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({'success': False, 'message': 'Invalid JSON data'}, status=400)

        try:
            classe = Classe.objects.filter(
                pk=data['id'], cohort_id=data['cohort']).update(**data)
            if classe:
                return Response({'success': True, 'message': 'Classe updated successfully'}, status=200)
            else:
                return Response({'success': False, 'message': 'Classe not found'}, status=404)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)

    elif request.method == 'DELETE':
        """Delete a classe"""
        try:
            classe = Classe.objects.filter(
                pk=id_classe).delete()
            if classe[0]:
                return Response({'success': True, 'message': 'Classe deleted successfully'}, status=200)
            else:
                return Response({'success': False, 'message': 'Classe not found'}, status=404)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)

    else:
        return Response({'success': False, 'message': 'Method not allowed'}, status=405)


@ csrf_exempt
def manage_material(request, id_material=None):
    if not request.user.is_authenticated:
        return Response({'success': False, 'message': 'User is not authenticated'}, status=401)

    if request.method == 'GET':
        """Retrieve material"""
        try:
            if id_material:
                material = Material.objects.get(pk=id_material)
                material_dict = model_to_dict(material)
                return Response({'success': True, 'data': material_dict}, status=200)
            else:
                materials = Material.objects.all()
                materials_list = [model_to_dict(material)
                                  for material in materials]
                return Response({'success': True, 'data': materials_list}, status=200)
        except Material.DoesNotExist:
            return Response({'success': False, 'message': 'No material found'}, status=404)
        except Exception as e:
            return Response({'success': False, 'message': f'Error: {e}'}, status=500)

    elif request.method == 'POST':
        """Add new material"""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({'success': False, 'message': 'Invalid JSON data'}, status=400)

        try:

            category = data.get('category')
            item = data.get('item')

            # Check if item already exists in the category
            if Material.objects.filter(category=category, item=item).exists():
                return Response({'success': False, 'message': 'Item already exists in this category'}, status=400)

            material = Material.create(**data)
            if material:
                return Response({'success': True, 'message': 'Material added successfully'}, status=201)
        except json.JSONDecodeError:
            return Response({'success': False, 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)

    elif request.method == 'PUT':
        """Update a material"""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({'success': False, 'message': 'Invalid JSON data'}, status=400)

        try:
            material = Material.update(data['id'], **data)
            if material:
                return Response({'success': True, 'message': 'Material updated successfully'}, status=200)
            else:
                return Response({'success': False, 'message': 'Material not found'}, status=404)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)

    elif request.method == 'DELETE':
        """Delete a material"""
        try:
            material = Material.delete(id_material)
            if material:
                return Response({'success': True, 'message': 'Material deleted successfully'}, status=200)
            else:
                return Response({'success': False, 'message': 'Material not found'}, status=404)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)

    else:
        return Response({'success': False, 'message': 'Method not allowed'}, status=405)


@ csrf_exempt
def manage_salle_formation(request, id_salle=None):
    if not request.user.is_authenticated:
        return Response({'success': False, 'message': 'User is not authenticated'}, status=401)

    if request.method == 'GET':
        """Retrieve salle formation"""
        try:
            if id_salle:
                salle = SalleFormation.objects.get(pk=id_salle)
                material_salle_formations = MaterialSalleFormation.objects.filter(
                    salle_formation=salle)
                materials_list = [{
                    'material': model_to_dict(msf.material),
                    'count_item': msf.count_item
                } for msf in material_salle_formations]
                salle_dict = model_to_dict(salle)
                salle_dict['materials'] = materials_list
                return Response({'success': True, 'data': salle_dict}, status=200)

            else:
                salles = SalleFormation.objects.all()
                salles_list = []
                for salle in salles:
                    materials_list = [{
                        'material': model_to_dict(msf.material),
                        'count_item': msf.count_item
                    } for msf in MaterialSalleFormation.objects.filter(salle_formation=salle)]
                    salle_dict = model_to_dict(salle)
                    salle_dict['materials'] = materials_list
                    salles_list.append(salle_dict)
                return Response({'success': True, 'data': salles_list}, status=200)
        except (SalleFormation.DoesNotExist, MaterialSalleFormation.DoesNotExist):
            return Response({'success': False, 'message': 'No salle or material salle formation found'}, status=404)
        except Exception as e:
            return Response({'success': False, 'message': f'Error: {e}'}, status=500)

    elif request.method == 'POST':
        """Add new salle formation"""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({'success': False, 'message': 'Invalid JSON data'}, status=400)

        try:
            # Validate and retrieve related models
            salle_name = data.get('salle_name')
            etage = data.get('etage')
            capacity = data.get('capacity')
            material_data = data.get('material', [])

            # Check if salle with same name and floor already exists
            if SalleFormation.objects.filter(salle_name=salle_name, etage=etage).exists():
                return Response({'success': False, 'message': 'Salle with the same name and floor already exists'}, status=400)

            # Create the new SalleFormation instance
            salle_formation = SalleFormation.objects.create(
                salle_name=salle_name,
                capacity=capacity,
                etage=etage
            )

            # Add materials to the salle_formation
            for material_info in material_data:
                material_id = material_info.get('material_id')
                count_item = material_info.get('count_item')

                material = Material.objects.filter(pk=material_id).first()
                if material:
                    MaterialSalleFormation.objects.create(
                        salle_formation=salle_formation,
                        material=material,
                        count_item=count_item
                    )

            # Return success response
            return Response({'success': True, 'message': 'Salle formation added successfully'}, status=201)

        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)

    elif request.method == 'PUT':
        """Update a salle formation"""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({'success': False, 'message': 'Invalid JSON data'}, status=400)

        try:
            salle_id = data.get('salle_id', 0)
            if salle_id:
                # Retrieve the SalleFormation instance
                salle = SalleFormation.objects.get(pk=salle_id)

                # Update SalleFormation fields if provided in the request
                salle.salle_name = data.get('salle_name', salle.salle_name)
                salle.etage = data.get('etage', salle.etage)
                salle.capacity = data.get('capacity', salle.capacity)
                salle.save()

                # Update or create MaterialSalleFormation instances associated with this SalleFormation
                material_data = data.get('material', [])
                for material_info in material_data:
                    material_id = material_info.get('material_id')
                    count_item = material_info.get('count_item')

                    material = Material.objects.filter(pk=material_id).first()
                    if material:
                        # Update or create MaterialSalleFormation instance
                        material_salle, created = MaterialSalleFormation.objects.update_or_create(
                            salle_formation=salle,
                            material=material,
                            defaults={'count_item': count_item}
                        )

                return Response({'success': True, 'message': 'Salle formation updated successfully'}, status=200)
            else:
                return Response({'success': False, 'message': 'Salle ID not provided'}, status=400)

        except SalleFormation.DoesNotExist:
            return Response({'success': False, 'message': 'Salle formation not found'}, status=404)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=500)

    elif request.method == 'DELETE':
        """Delete a salle formation"""
        try:
            salle = SalleFormation.delete(id_salle)
            if salle:
                return Response({'success': True, 'message': 'Salle formation deleted successfully'}, status=200)
            else:
                return Response({'success': False, 'message': 'Salle formation not found'}, status=404)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)

    else:
        return Response({'success': False, 'message': 'Method not allowed'}, status=405)


@ csrf_exempt
def manage_seance(request, id_seance=None):
    if not request.user.is_authenticated:
        return Response({'success': False, 'message': 'User is not authenticated'}, status=401)

    if request.method == 'GET':
        """Retrieve seance(s)"""
        try:
            if id_seance:
                seance = Seance.objects.get(pk=id_seance)
                seance_dict = model_to_dict(seance)
                return Response({'success': True, 'data': seance_dict}, status=200)
            else:
                seances = Seance.objects.all()
                seances_list = [model_to_dict(seance) for seance in seances]
                return Response({'success': True, 'data': seances_list}, status=200)
        except Seance.DoesNotExist:
            return Response({'success': False, 'message': 'No seance found'}, status=404)
        except Exception as e:
            return Response({'success': False, 'message': f'Error: {e}'}, status=500)

    elif request.method == 'POST':
        """Add new seance"""
        try:
            data = json.loads(request.body)

            # Validate and retrieve related models
            classe_id = data.get('classe_id')
            teacher_id = data.get('teacher_id')
            matiere_id = data.get('matiere_id')
            salle_formation_id = data.get('salle_formation_id')
        except json.JSONDecodeError:
            return Response({'success': False, 'message': 'Invalid JSON data'}, status=400)

        try:
            # Check if a teacher exists
            try:
                teacher = Teacher.objects.get(pk=teacher_id)
            except Teacher.DoesNotExist:
                return Response({'success': False, 'message': 'No teacher found'}, status=404)

            # Check if a classe exists
            try:
                classe = Classe.objects.get(pk=classe_id)
            except Classe.DoesNotExist:
                return Response({'success': False, 'message': 'No classe found'}, status=404)

            # Check if a matiere exists
            try:
                matiere = Matiere.objects.get(pk=matiere_id)
            except Matiere.DoesNotExist:
                return Response({'success': False, 'message': 'No matiere found'}, status=404)

            # Check if a salle_formation exists
            try:
                salle_formation = SalleFormation.objects.get(
                    pk=salle_formation_id)
            except SalleFormation.DoesNotExist:
                return Response({'success': False, 'message': 'No salle_formation found'}, status=404)

            # Check if a seance with the same details already exists
            if Seance.objects.filter(
                date_seance=data['date_seance'],
                time_start=data['time_start'],
                time_end=data['time_end'],
                teacher=teacher,
                classe=classe,
                matiere=matiere,
                salle_formation=salle_formation
            ).exists():
                return Response({'success': False, 'message': 'Seance with the same details already exists'}, status=400)

            # Create the new Seance instance
            seance = Seance.objects.create(
                date_seance=data['date_seance'],
                time_start=data['time_start'],
                time_end=data['time_end'],
                titre_module=data['titre_module'],
                titre_cour=data['titre_cour'],
                effectif_present=data['effectif_present'],
                effectif_absent=data['effectif_absent'],
                is_done=data['is_done'],
                observations=data['observations'],
                classe=classe,
                teacher=teacher,
                matiere=matiere,
                salle_formation=salle_formation
            )

            if seance:
                return Response({'success': True, 'message': 'Seance added successfully'}, status=201)
            else:
                return Response({'success': False, 'message': 'Failed to add seance'}, status=400)

        except KeyError as e:
            missing_field = e.args[0]
            return Response({'success': False, 'message': f'Missing field: {missing_field}'}, status=400)

        except ValidationError as e:
            return Response({'success': False, 'message': f'Validation Error: {e}'}, status=400)

        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)

    elif request.method == 'PUT':
        """Update a seance"""
        try:
            data = json.loads(request.body)
            # Validate and retrieve related models
            seance_id = data.get('seance_id')
            classe_id = data.get('classe_id')
            teacher_id = data.get('teacher_id')
            matiere_id = data.get('matiere_id')
            salle_formation_id = data.get('salle_formation_id')
        except json.JSONDecodeError:
            return Response({'success': False, 'message': 'Invalid JSON data'}, status=400)

        try:

            classe = Classe.objects.get(pk=classe_id)
            teacher = Teacher.objects.get(pk=teacher_id)
            matiere = Matiere.objects.get(pk=matiere_id)
            salle_formation = SalleFormation.objects.get(pk=salle_formation_id)

            # Update the Seance instance
            seance = Seance.objects.get(pk=seance_id)
            seance.date_seance = data.get('date_seance', seance.date_seance)
            seance.time_start = data.get('time_start', seance.time_start)
            seance.time_end = data.get('time_end', seance.time_end)
            seance.titre_module = data.get('titre_module', seance.titre_module)
            seance.titre_cour = data.get('titre_cour', seance.titre_cour)
            seance.effectif_present = data.get(
                'effectif_present', seance.effectif_present)
            seance.effectif_absent = data.get(
                'effectif_absent', seance.effectif_absent)
            seance.is_done = data.get('is_done', seance.is_done)
            seance.observations = data.get('observations', seance.observations)
            seance.classe = classe
            seance.teacher = teacher
            seance.matiere = matiere
            seance.salle_formation = salle_formation

            seance.save()

            return Response({'success': True, 'message': 'Seance updated successfully'}, status=200)

        except Seance.DoesNotExist:
            return Response({'success': False, 'message': 'Seance not found'}, status=404)

        except (Classe.DoesNotExist, Teacher.DoesNotExist, Matiere.DoesNotExist, SalleFormation.DoesNotExist) as e:
            return Response({'success': False, 'message': 'Related object not found'}, status=404)

        except ValidationError as e:
            return Response({'success': False, 'message': f'Validation Error: {e}'}, status=400)

        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)

    elif request.method == 'DELETE':
        """Delete a seance"""
        try:
            seance = Seance.objects.filter(pk=id_seance).delete()
            if seance[0]:
                return Response({'success': True, 'message': 'Seance deleted successfully'}, status=200)
            else:
                return Response({'success': False, 'message': 'Seance not found'}, status=404)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)

    else:
        return Response({'success': False, 'message': 'Method not allowed'}, status=405)


# ============================No neeed manage==================================

# @csrf_exempt
# def manage_material_salle_formation(request, id_material_salle=None):
#     if request.method == 'GET':
#         """Retrieve material salle formation"""
#         try:
#             if id_material_salle:
#                 material_salle = MaterialSalleFormation.objects.get(
#                     pk=id_material_salle)
#                 material_salle_dict = model_to_dict(material_salle)
#                 return Response({'success': True, 'data': material_salle_dict}, status=200)
#             else:
#                 material_salles = MaterialSalleFormation.objects.all()
#                 material_salles_list = [model_to_dict(
#                     msf) for msf in material_salles]
#                 return Response({'success': True, 'data': material_salles_list}, status=200)
#         except MaterialSalleFormation.DoesNotExist:
#             return Response({'success': False, 'message': 'No material salle formation found'}, status=404)
#         except Exception as e:
#             return Response({'success': False, 'message': f'Error: {e}'}, status=500)

#     elif request.method == 'POST':
#         """Add new material salle formation"""
#         try:
#             data = json.loads(request.body)
#         except json.JSONDecodeError:
#             return Response({'success': False, 'message': 'Invalid JSON data'}, status=400)

#         try:

#             # Validate and retrieve related models
#             salle_formation_id = data.get('salle_formation')
#             material_id = data.get('material')

#             salle_formation = SalleFormation.objects.filter(
#                 pk=salle_formation_id).first()
#             material = Material.objects.filter(pk=material_id).first()

#             if not salle_formation or not material:
#                 return Response({'success': False, 'message': 'Invalid salle formation or material'}, status=400)

#             # Create the new MaterialSalleFormation instance
#             material_salle_created = MaterialSalleFormation.create(
#                 salle_formation=salle_formation,
#                 material=material,
#                 # Default to 1 if count_item is not provided
#                 count_item=data.get('count_item', 1)
#             )
#             if material_salle_created:
#                 return Response({'success': True, 'message': 'Material salle formation added successfully'}, status=201)
#             else:
#                 return Response({'success': False, 'message': 'Failed to add material salle formation'}, status=400)
#         except json.JSONDecodeError:
#             return Response({'success': False, 'message': 'Invalid JSON data'}, status=400)
#         except Exception as e:
#             return Response({'success': False, 'message': str(e)}, status=400)

#     elif request.method == 'PUT':
#         """Update a material salle formation"""
#         try:
#             data = json.loads(request.body)
#         except json.JSONDecodeError:
#             return Response({'success': False, 'message': 'Invalid JSON data'}, status=400)

#         try:
#             material_salle = MaterialSalleFormation.update(
#                 id_material_salle, **data)
#             if material_salle:
#                 return Response({'success': True, 'message': 'Material salle formation updated successfully'}, status=200)
#             else:
#                 return Response({'success': False, 'message': 'Material salle formation not found'}, status=404)
#         except Exception as e:
#             return Response({'success': False, 'message': str(e)}, status=400)

#     elif request.method == 'DELETE':
#         """Delete a material salle formation"""
#         try:
#             material_salle = MaterialSalleFormation.delete(id_material_salle)
#             if material_salle:
#                 return Response({'success': True, 'message': 'Material salle formation deleted successfully'}, status=200)
#             else:
#                 return Response({'success': False, 'message': 'Material salle formation not found'}, status=404)
#         except Exception as e:
#             return Response({'success': False, 'message': str(e)}, status=400)

#     else:
#         return Response({'success': False, 'message': 'Method not allowed'}, status=405)
