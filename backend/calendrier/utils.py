from django.http import JsonResponse
from .models import Calendrier


def add_seance(date, time, seance):
    try:
        added = Calendrier.create(
            date_event=date,
            time_event=time,
            seance=seance,
        )
        if added:
            return JsonResponse({'success': True, 'message': 'Seance added successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'error is {e}'})
