from datacenter.models import Passcard
from datacenter.models import is_visit_long
from datacenter.models import format_duration
from datacenter.models import get_duration
from datacenter.models import get_visited_info
from django.shortcuts import get_object_or_404
from django.shortcuts import render

def passcard_visits_render(visitors):
    this_passcard_visits = list()
    for visitor in visitors:
        duration_seconds = get_duration(visitor)
        duration_format = format_duration(duration_seconds)
        is_strange = is_visit_long(visitor)
        this_passcard_visits.append(
            {
                'entered_at': visitor.entered_at,
                'duration': duration_format,
                'is_strange': is_strange
            }
        )
    return this_passcard_visits


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    all_visited_info = get_visited_info(passcard)
    this_passcard_visits = passcard_visits_render(all_visited_info)

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
