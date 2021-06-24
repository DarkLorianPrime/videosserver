import uuid

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.shortcuts import redirect

from authServer.models import cookie_saves, Role, Role_List


class BackendAuth(BaseBackend):
    def authenticate(self, request, username=None, password=None, email=None, registration=False):
        if registration:
            if User.objects.filter(username=username).first() is not None:
                return {'error': 'Login'}
            if User.objects.filter(email=email).first() is not None:
                return {'error': 'Email'}
            User.objects.create_user(username=username, password=password, email=email).save()
            data_uuid, redirects, obj = uuid.uuid4().hex, redirect('/'), User.objects.filter(username=username).first()
            cookie_saves.objects.create(cookie_user_data_id=obj.id, cookie_user_token=data_uuid)
            redirects.set_cookie(key='loggined_token', value=data_uuid, max_age=1000000)
            Role.objects.create(name=Role_List.objects.filter(name='User').first(), users=obj)
            return redirects
        obj = User.objects.filter(username=username).first()
        if obj is None:
            return {'error': True}
        if obj.check_password(raw_password=password) is not True:
            return {'error': True}
        data_uuid = uuid.uuid4().hex
        cookie_saves.objects.create(cookie_user_data=obj, cookie_user_token=data_uuid)
        returned = redirect('/')
        returned.set_cookie(key='loggined_token', value=data_uuid, max_age=10000000)
        return returned
