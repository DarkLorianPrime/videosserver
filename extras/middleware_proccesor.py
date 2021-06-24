from django.utils.deprecation import MiddlewareMixin

from authServer.models import cookie_saves

list_of_restrictible = ['login', 'registration', 'recent']


class GetUser(MiddlewareMixin):
    def process_request(self, request):
        request.Auth_user = None
        user = cookie_saves.objects.filter(cookie_user_token=request.COOKIES.get('loggined_token')).first()
        if user is not None:
            request.Auth_user = user.cookie_user_data
