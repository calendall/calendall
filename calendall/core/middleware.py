import pytz

from django.utils import timezone


class TimezoneMiddleware(object):
    def process_request(self, request):
        tzname = request.session.get('user-tz')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            try:
                user_tz = request.user.timezone
                request.session['user-tz'] = user_tz
                timezone.activate(pytz.timezone(user_tz))
            except AttributeError:
                timezone.deactivate()
