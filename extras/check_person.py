from django.contrib.auth.models import User

from authServer.models import cookie_saves, Admin


def get_login(request):
    d = request.COOKIES.get('loggined_token')
    cookie = cookie_saves.objects.filter(cookie_user_token=d).first()
    if cookie is not None:
        Users = User.objects.filter(id=cookie.cookie_user_id).first()
        is_admin = False
        is_admin_or_not = Admin.objects.filter(name=Users).first()
        if is_admin_or_not is not None:
            is_admin = True
        print(User, is_admin)
        print('==========================================')
        return Users, is_admin
    return False, False
