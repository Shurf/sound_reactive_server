from html import escape

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class LedProfile(models.Model):

    led_profile_name = models.CharField(max_length=128, null=False)
    is_current = models.BooleanField(null=False, default=False)
    red = models.IntegerField(null=False, validators=[MaxValueValidator(255), MinValueValidator(0)])
    green = models.IntegerField(null=False, validators=[MaxValueValidator(255), MinValueValidator(0)])
    blue = models.IntegerField(null=False, validators=[MaxValueValidator(255), MinValueValidator(0)])
    brightness = models.IntegerField(null=False, validators=[MaxValueValidator(255), MinValueValidator(0)], default=80)
    multiplier = models.FloatField(null=False, default=1)
    mode = models.IntegerField(null=False, default=0)

    MODE_SINGLE_COLOR = 0
    MODE_GROW_FROM_CENTER = 1

    MODE_SINGLE_COLOR_TEXT = _('Single Color')
    GROW_FROM_CENTER_TEXT = _('Grow from Center')

    __MODES = {
        MODE_SINGLE_COLOR: MODE_SINGLE_COLOR_TEXT,
        MODE_GROW_FROM_CENTER: GROW_FROM_CENTER_TEXT
    }

    @staticmethod
    def modes_for_form():
        return [(x, LedProfile.__MODES[x]) for x in LedProfile.__MODES]

    def __str__(self):
        return self.led_profile_name

    def json(self):
        return {
            'id': self.id,
            'led_profile_name': escape(self.led_profile_name),
            'is_current': self.is_current,
            'red': self.red,
            'green': self.green,
            'blue': self.blue,
            'brightness': self.brightness,
            'multiplier': self.multiplier,
            'mode': self.mode,
            'mode_printable': LedProfile.__MODES[self.mode]
        }

    @staticmethod
    def return_json(
            request_parameters
    ):
        query = LedProfile.objects
        unfiltered_query = query
        if 'search' in request_parameters:
            query = query.filter(led_profile_name__icontains=request_parameters['search'])
            query = query.distinct()

        if 'sort' in request_parameters:
            query = query.order_by(request_parameters['sort'])
            if 'order' in request_parameters and request_parameters['order'] == 'desc':
                query = query.reverse()

        total_filtered_rows = len(query)

        # noinspection PyBroadException
        try:
            offset = int(request_parameters['offset'])
            limit = int(request_parameters['limit'])
            query = query[offset:offset + limit]
        except Exception:
            pass

        result = []
        for chronicle in query:

            result.append(chronicle.json())

        return {
            'total': total_filtered_rows,
            'totalNotFiltered': len(unfiltered_query.all()),
            'rows': result
        }

