from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'sound_reactive_server'

urlpatterns = [
    path(r'', views.led_profiles.LedProfileIndexView.as_view(), name='default'),

    path(r'led_profiles',
         views.led_profiles.LedProfileIndexView.as_view(),
         name='led_profiles'),

    path(r'led_profiles/current',
         views.led_profiles.LedProfileGetCurrentJson.as_view(),
         name='current_led_profile'),

    path(r'led_profiles/get_by_name',
         views.led_profiles.LedProfileGetByNameJson.as_view(),
         name='led_profile_by_name'),

    path(r'led_profiles/set_primary',
         csrf_exempt(views.led_profiles.LedProfileSetPrimarySecondary.as_view()),
         name='led_profile_set_primary'),

    path(r'led_profiles/<int:pk>/update',
         views.led_profiles.LedProfileUpdateView.as_view(),
         name='update_led_profile'),

    path(r'led_profiles/<int:pk>/delete',
         views.led_profiles.LedProfileDeleteView.as_view(),
         name='delete_led_profile'),

    path(r'led_profiles/create',
         views.led_profiles.LedProfileCreateView.as_view(),
         name='create_led_profile'),

    path(r'led_profiles/<int:pk>',
         views.led_profiles.CommonDetailsView.as_view(),
         name='led_profile_details'),

]

