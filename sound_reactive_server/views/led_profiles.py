import datetime
import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import BaseUpdateView

from sound_reactive_server.forms.led_profile import LedProfileForm
from sound_reactive_server.helpers.color_helper import ColorHelper
from sound_reactive_server.models.ledprofile import LedProfile
from sound_reactive_server.views.common.common_views import CommonIndexView, CommonUpdateView, CommonCreateView, CommonDeleteView, \
    CommonDetailsView


class LedProfileGetCurrentJson(BaseDetailView):
    def get(self, request, *args, **kwargs):
        current_led_profile = LedProfile.objects.get(is_current=True)
        return JsonResponse(current_led_profile.json())


class LedProfileGetByNameJson(BaseDetailView):
    def get(self, request, *args, **kwargs):
        current_led_profile = LedProfile.objects.get(
            led_profile_name__iexact=request.GET['led_profile_name'].lower())
        return JsonResponse(current_led_profile.json())


class LedProfileSetPrimarySecondary(View):
    def post(self, request, *args, **kwargs):
        request_body = json.loads(request.body.decode())
        current_led_profile = LedProfile.objects.get(
            led_profile_name__iexact=request_body['led_profile_name'].lower())
        if 'primary' in request_body:
            if request_body['primary']:
                current_led_profile.use_secondary = False
            else:
                current_led_profile.use_secondary = True
        if 'percentage' in request_body:
            current_led_profile.percentage = int(request_body['percentage'])
        current_led_profile.save()
        return HttpResponse()


class LedProfileIndexView(CommonIndexView):
    template_name = 'led_profiles/index.html'
    model = LedProfile


class LedProfileUpdateView(CommonUpdateView):
    template_name = 'generics/update.html'
    form_class = LedProfileForm
    context_object_name = 'entity'
    model = LedProfile

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = _('Update LED profile')
        data['entity_name'] = _('led_profile')
        return data

    def form_valid(self, form):
        form.instance.red, form.instance.green, form.instance.blue = \
            ColorHelper.hex_to_rgb(form.cleaned_data['color'])
        if form.cleaned_data['is_current']:
            previous_current = LedProfile.objects.filter(is_current=True).first()
            if previous_current:
                previous_current.is_current = False
                previous_current.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('sound_reactive_server:led_profiles')


class LedProfileCreateView(CommonCreateView):
    template_name = 'generics/create.html'
    form_class = LedProfileForm
    model = LedProfile

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = _('Create LED profile')
        data['entity_name'] = _('LED profile')
        return data

    def form_valid(self, form):
        form.instance.red, form.instance.green, form.instance.blue = \
            ColorHelper.hex_to_rgb(form.cleaned_data['color'])

        if form.cleaned_data['is_current']:
            previous_current = LedProfile.objects.filter(is_current=True).first()
            if previous_current:
                previous_current.is_current = False
                previous_current.save()
        return super().form_valid(form)


class LedProfileDeleteView(CommonDeleteView):
    template_name = 'generics/delete.html'
    context_object_name = 'entity'
    model = LedProfile

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = _('Delete LED profile')
        return data

    def get_success_url(self):
        return reverse('sound_reactive_server:led_profiles')

