from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
import json
from .models import Calendrier, Seance
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from authentication.utils import APIAccessMixin


class CalendrierView(APIAccessMixin, APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id_calendrier=None):
        # if not request.user.is_authenticated:
        #     return Response({'success': False, 'message': 'User is not authenticated'}, status=401)

        try:
            if id_calendrier:
                # Retrieve calendriers for a specific seance
                seance = Seance.get_one(id_calendrier)
                calendriers = Calendrier.objects.filter(seance=seance)
            else:
                calendriers = Calendrier.objects.all()

            calendriers_list = [model_to_dict(
                calendrier) for calendrier in calendriers]
            return Response({'success': True, 'data': calendriers_list}, status=200)
        except Calendrier.DoesNotExist:
            return Response({'success': False, 'message': 'No calendrier found'}, status=404)
        except Exception as e:
            return Response({'success': False, 'message': f'Error: {e}'}, status=500)

    def post(self, request):

        try:
            data = json.loads(request.body)

            date_event = data.get('date_event', '')
            time_event = data.get('time_event', '')
            seance_id = data.get('seance_id', 0)
        except json.JSONDecodeError:
            return Response({'success': False, 'message': 'Invalid JSON data'}, status=400)

        try:

            if not date_event or not time_event or not seance_id:
                return Response({'success': False, 'message': 'Missing required fields'}, status=400)

            # Validate and retrieve related models
            try:
                seance = Seance.objects.get(pk=seance_id)
            except Seance.DoesNotExist:
                return Response({'success': False, 'message': 'No seance found'}, status=404)

            # Check if a calendrier for this seance already exists
            if Calendrier.objects.filter(time_event=time_event, seance=seance).exists():
                return Response({'success': False, 'message': 'This seance already program it'}, status=400)

            # Create the new Calendrier instance
            calendrier = Calendrier.objects.create(
                date_event=date_event,
                time_event=time_event,
                seance=seance,
            )

            return Response({'success': True, 'message': 'Calendrier added successfully'}, status=201)

        except ValidationError as e:
            return Response({'success': False, 'message': f'Validation Error: {e}'}, status=400)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=500)

    def put(self, request, id_calendrier=None):

        try:
            data = json.loads(request.body)
            # calendrier_id = data.get('calendrier_id')

            if not id_calendrier:
                return Response({'success': False, 'message': 'Calendrier ID not provided'}, status=400)

            # Retrieve the calendrier instance
            calendrier = Calendrier.objects.get(pk=id_calendrier)

            # Update calendrier fields if provided in the request
            calendrier.date_event = data.get(
                'date_event', calendrier.date_event)
            calendrier.time_event = data.get(
                'time_event', calendrier.time_event)
            calendrier.seance_id = data.get('seance_id', calendrier.seance_id)
            calendrier.save()

            return Response({'success': True, 'message': 'Calendrier updated successfully'}, status=200)
        except Calendrier.DoesNotExist:
            return Response({'success': False, 'message': 'Calendrier not found'}, status=404)
        except json.JSONDecodeError:
            return Response({'success': False, 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=500)

    def delete(self, request, id_calendrier=None):
        try:
            calendrier = Calendrier.delete(id_calendrier)
            if calendrier:
                return Response({'success': True, 'message': 'Calendrier deleted successfully'}, status=200)
            else:
                return Response({'success': False, 'message': 'Calendrier not found'}, status=404)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)
