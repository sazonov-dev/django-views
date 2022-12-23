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
    now = localtime(visit.entered_at)
    then = localtime()
    delta = then.replace(tzinfo=None) - now.replace(tzinfo=None)
    return delta.seconds

def get_all_passcards():
    return Passcard.objects.all()

def format_duration(duration):
    d = timedelta(seconds=duration)
    return d

def long_visit_info(visits, minutes=60):
    long_visit = list()
    for visitor in visits:
        if visitor.leaved_at:
            seconds = get_duration(visitor)
            minutes_visit = seconds // 60
            print(minutes)
            if minutes_visit > minutes:
                long_visit.append(visitor)
    return long_visit   

def is_visit_long(visit, minutes=60):
    seconds = get_duration(visit)
    minutes_visit = seconds // 60
    if minutes_visit > minutes:
        return True
    return False

def get_visited_info(visitor):
    return Visit.objects.filter(passcard=visitor)

        

    