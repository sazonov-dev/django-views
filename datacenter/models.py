from django.db import models
from django.utils.timezone import localtime
from datetime import timedelta

class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

def get_duration(visit):
    entered_at_time = localtime(visit.entered_at)
    if not visit.leaved_at:
        levead_at_time = localtime()
    else:
        levead_at_time = localtime(visit.leaved_at)
        
    delta = levead_at_time.replace(tzinfo=None) - entered_at_time.replace(tzinfo=None)
    return delta.total_seconds()

def get_all_passcards():
    return Passcard.objects.all()

def format_duration(duration):
    d = timedelta(seconds=duration)
    format_duration = str(d).split('.')[0]
    return format_duration

def check_minutes_visit(minutes_visit, minutes_limit):
    result = minutes_visit > minutes_limit
    return result

def is_visit_long(visit, minutes=60):
    seconds = get_duration(visit)
    minutes_visit = seconds // 60
    is_long = check_minutes_visit(minutes_visit, minutes)
    return is_long

def get_visitor_with_passcard(visitor):
    return Visit.objects.filter(passcard=visitor)
        

    