from datacenter.models import Passcard
from datacenter.models import is_visit_long
from datacenter.models import format_duration
from datacenter.models import get_duration
from datacenter.models import get_visitor_with_passcard
from django.shortcuts import get_object_or_404
from django.shortcuts import render

def render_visit_with_passcard(visitors):
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


def get_passcard_with_passcode(passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    return passcard


def passcard_info_view(request, passcode):
    passcard = get_passcard_with_passcode(passcode)
    all_visited_info = get_visitor_with_passcard(passcard)
    this_passcard_visits = render_visit_with_passcard(all_visited_info)

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
