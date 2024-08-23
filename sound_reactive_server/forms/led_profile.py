import django_select2
from django import forms
from django_select2 import forms as s2forms
from django.utils.translation import ugettext_lazy as _

from sound_reactive_server.helpers.color_helper import ColorHelper
from sound_reactive_server.models.ledprofile import LedProfile


class LedProfileForm(forms.ModelForm):
    mode = forms.ChoiceField(
        choices=LedProfile.modes_for_form(),
        label=_('Mode'),
        widget=forms.Select(),
        required=True
    )

    color = forms.CharField(label='Color', widget=forms.TextInput(attrs={'type': 'color'}))
    class Meta:
        model = LedProfile
        fields = [
            'led_profile_name',
            'is_current',
            'brightness',
            'multiplier',
            'mode'
        ]
        labels = {
            'led_profile_name': _('Profile name'),
            'is_current': _('Current'),
            'brightness': _('Brightness'),
            'multiplier': _('Multiplier')
        }
        widgets = {
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        if instance:
            self.fields['color'].initial = ColorHelper.rgb_to_hex(instance.red, instance.green, instance.blue)

        self.visible_fields()[0].field.widget.attrs['autofocus'] = ''
        for visible in self.visible_fields():
            if visible.name in ['is_current', 'enabled']:
                visible.is_check_box = True
                continue
            visible.field.widget.attrs['class'] = 'form-control input-normal'
