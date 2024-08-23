import datetime

from django.utils import http


class ViewHelper:

    RETURN_URL_PARAMETER_NAME = 'return_url'

    @staticmethod
    def make_return_url(request):
        return '?' + http.urlencode({ViewHelper.RETURN_URL_PARAMETER_NAME: request.path})


    @staticmethod
    def process_return_address_in_url(data, request):

        data['url'] = request.path
        if ViewHelper.RETURN_URL_PARAMETER_NAME in request.GET:
            data['url'] += '?' + \
            http.urlencode(
                {ViewHelper.RETURN_URL_PARAMETER_NAME: request.GET[ViewHelper.RETURN_URL_PARAMETER_NAME]}
            )
        return data

    @staticmethod
    def process_common_data(data, request, model_instance=None, department_categories=None):
        return data

    @staticmethod
    def get_cookies_name(view_name):
        return f'{view_name.lower()}_filters'

    @staticmethod
    def get_cookies_values(request, view_name):
        request_url = request.get_full_path()
        previous_page = request.META.get("HTTP_REFERER") or ''
        cookies_name = ViewHelper.get_cookies_name(view_name)
        cookies_to_save = request.META.get("QUERY_STRING") or ''

        if not request.GET and f'{request_url}?' not in previous_page:
            cookie_value = request.COOKIES[cookies_name] if cookies_name in request.COOKIES else ''
            if cookie_value:
                cookie_url = f'{request_url}?{cookie_value}'
                return cookie_url, cookies_name, cookies_to_save
        return '', cookies_name, cookies_to_save

    @staticmethod
    def get_cookies_expire_time():
        return datetime.datetime.today() + datetime.timedelta(days=365)
