from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.views import generic

from sound_reactive_server.helpers.view_helper import ViewHelper
from sound_reactive_server.views.common.common_constants import ViewsConstants


class CommonIndexView(generic.TemplateView):

    model = None

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['enabled_cookies'] = ViewsConstants.ENABLED_TABLE_CACHE
        return ViewHelper.process_common_data(data=data, request=self.request)

    def get(self, request, *args, **kwargs):

        if 'json' in self.request.GET:
            content = self.model.return_json(
                request_parameters=self.request.GET
            )
            if request.GET.get('debug'):
                return HttpResponse(u'<html><body><pre>{}</pre></body></html>'.format(content))
            return JsonResponse(content)

        cookie_url, cookies_name, cookies_to_save = ViewHelper.get_cookies_values(request, self.__class__.__name__)
        if cookie_url:
            return HttpResponseRedirect(cookie_url)

        response = super().get(request, *args, **kwargs)
        if request.user.is_authenticated:
            response.set_cookie(key=cookies_name, value=cookies_to_save, expires=ViewHelper.get_cookies_expire_time())
        return response


class CommonCreateView(generic.CreateView):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return ViewHelper.process_return_address_in_url(data=data, request=self.request)

    def get_success_url(self):
        if ViewHelper.RETURN_URL_PARAMETER_NAME in self.request.GET:
            return self.request.GET[ViewHelper.RETURN_URL_PARAMETER_NAME].replace('&', '?', 1)
        return reverse('sound_reactive_server:default')


class CommonUpdateView(generic.UpdateView):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return ViewHelper.process_return_address_in_url(data=data, request=self.request)

    def get_success_url(self):
        if ViewHelper.RETURN_URL_PARAMETER_NAME in self.request.GET:
            return self.request.GET[ViewHelper.RETURN_URL_PARAMETER_NAME].replace('&', '?', 1)
        return reverse('sound_reactive_server:default')


class CommonDeleteView(generic.DeleteView):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return ViewHelper.process_return_address_in_url(data=data, request=self.request)

    def get_success_url(self):
        if ViewHelper.RETURN_URL_PARAMETER_NAME in self.request.GET:
            return self.request.GET[ViewHelper.RETURN_URL_PARAMETER_NAME].replace('&', '?', 1)
        return reverse('sound_reactive_server:default')


class CommonDetailsView(generic.DetailView):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['enabled_cookies'] = ViewsConstants.ENABLED_TABLE_CACHE
        return ViewHelper.process_common_data(data=data, request=self.request, model_instance=self.object)

    def get(self, request, *args, **kwargs):

        cookie_url, cookies_name, cookies_to_save = ViewHelper.get_cookies_values(request, self.__class__.__name__)
        if cookie_url:
            return HttpResponseRedirect(cookie_url)

        response = super().get(request, *args, **kwargs)
        if request.user.is_authenticated:
            response.set_cookie(key=cookies_name, value=cookies_to_save, expires=ViewHelper.get_cookies_expire_time())
        return response
