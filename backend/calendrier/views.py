from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Calendrier, Seance
from django.forms.models import model_to_dict
import json
from django.core.exceptions import ValidationError


@csrf_exempt
def manage_calendrier(request, id_calendrier=None):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

    if request.method == 'GET':
        """Retrieve calendriers"""
        try:
            if id_calendrier:
                # Retrieve calendriers for a specific seance
                seance = Seance.get_one(id_calendrier)
                calendriers = Calendrier.objects.filter(seance=seance)
                calendriers_list = [model_to_dict(
                    calendrier) for calendrier in calendriers]
                return JsonResponse({'success': True, 'data': calendriers_list}, status=200)
            else:
                calendriers = Calendrier.objects.all()
                calendriers_list = [model_to_dict(
                    calendrier) for calendrier in calendriers]
                return JsonResponse({'success': True, 'data': calendriers_list}, status=200)

        except Calendrier.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'No calendrier found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {e}'}, status=500)

    elif request.method == 'POST':
        """Add new calendrier"""
        try:
            data = json.loads(request.body)

            date_event = data.get('date_event', '')
            time_event = data.get('time_event', '')
            seance_id = data.get('seance_id', 0)

            if not date_event or not time_event or not seance_id:
                return JsonResponse({'success': False, 'message': 'Missing required fields'}, status=400)

            # Validate and retrieve related models
            try:
                seance = Seance.objects.get(pk=seance_id)
            except Seance.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'No seance found'}, status=404)

            # Check if a calendrier for this seance already exists
            if Calendrier.objects.filter(time_event=time_event, seance=seance).exists():
                return JsonResponse({'success': False, 'message': 'This seance already program it'}, status=400)

            # Create the new Calendrier instance
            calendrier = Calendrier.objects.create(
                date_event=date_event,
                time_event=time_event,
                seance=seance,
            )

            return JsonResponse({'success': True, 'message': 'Calendrier added successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': f'Validation Error: {e}'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    elif request.method == 'PUT':
        """Update a calendrier"""
        try:
            data = json.loads(request.body)
            calendrier_id = data.get('calendrier_id')

            if not calendrier_id:
                return JsonResponse({'success': False, 'message': 'Calendrier ID not provided'}, status=400)

            # Retrieve the calendrier instance
            calendrier = Calendrier.objects.get(pk=calendrier_id)

            # Update calendrier fields if provided in the request
            calendrier.date_event = data.get(
                'date_event', calendrier.date_event)
            calendrier.time_event = data.get(
                'time_event', calendrier.time_event)
            calendrier.seance_id = data.get('seance_id', calendrier.seance_id)
            calendrier.save()

            return JsonResponse({'success': True, 'message': 'Calendrier updated successfully'}, status=200)
        except Calendrier.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Calendrier not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    elif request.method == 'DELETE':
        """Delete a calendrier"""
        try:
            calendrier = Calendrier.delete(id_calendrier)
            if calendrier:
                return JsonResponse({'success': True, 'message': 'Calendrier deleted successfully'}, status=200)
            else:
                return JsonResponse({'success': False, 'message': 'Calendrier not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
