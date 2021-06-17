from django.contrib.auth.models import User
from django.utils.deprecation import MiddlewareMixin

from authServer.models import cookie_saves


class GetUser(MiddlewareMixin):
    def process_request(self, request):
        user = cookie_saves.objects.filter(cookie_user_token=request.COOKIES.get('loggined_token')).first()
        if user is not None:
            user_returned_id = user.cookie_user_id
        else:
            user_returned_id = None
        request.Auth_user = User.objects.filter(id=user_returned_id).first()
        return None
