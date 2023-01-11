from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.models import get_duration
from datacenter.models import format_duration
from django.shortcuts import render


def visitor_not_leaved():
    return Visit.objects.filter(leaved_at__isnull=True)

def get_visitors(visitors):
    non_closed_visitors = list()

    for visitor in visitors:
        duration = get_duration(visitor)
        duration_format = format_duration(duration)
        non_closed_visitors.append(
            {
                'who_entered': visitor.passcard,
                'entered_at': visitor.entered_at,
                'duration': duration_format
            }
        )
    return non_closed_visitors

def storage_information_view(request):
    all_visitors = visitor_not_leaved()
    visitors = get_visitors(all_visitors)

    context = {
        'non_closed_visits': visitors,
    }
    return render(request, 'storage_information.html', context)
