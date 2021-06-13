from django.contrib.auth.models import User

from authServer.models import cookie_saves


class Updater:
    def get_login(self, request):
        d = request.COOKIES.get('loggined_token')
        cookie = cookie_saves.objects.filter(cookie_user_token=d).first()
        Users = User.objects.filter(id=cookie.cookie_user_id).first()
        if cookie is not None:
            return Users
        return False
