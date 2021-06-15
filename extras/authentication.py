import uuid

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.shortcuts import redirect

from authServer.models import cookie_saves, Role


class BackendAuth(BaseBackend):
    def authenticate(self, request, username=None, password=None, email=None, registration=False):
        if registration:
            if User.objects.filter(username=username).first() is not None:
                return {'error': 'username'}
            if User.objects.filter(email=email).first() is not None:
                return {'error': 'mail'}
            User.objects.create_user(username=username, password=password, email=email).save()
            data_uuid, redirects, obj = uuid.uuid4().hex, redirect('/'), User.objects.filter(username=username).first()
            cookie_saves.objects.create(cookie_user_id=obj.id, cookie_user_token=data_uuid)
            redirects.set_cookie(key='loggined_token', value=data_uuid, max_age=10000000000)
            Role.objects.create(name='User', Users=obj, is_Role=True)
            Role.objects.create(name='Administrator', Users=obj, is_Role=False)
            Role.objects.create(name='Moderator', Users=obj, is_Role=False)
            return redirects
        obj = User.objects.filter(username=username).first()
        if obj is None:
            return {'error': True}
        if obj.check_password(raw_password=password) is not True:
            return {'error': True}
        data_uuid = uuid.uuid4().hex
        redirects = redirect('/')
        if cookie_saves.objects.filter(cookie_user_id=obj.id).first() is None:
            cookie_saves.objects.create(cookie_user_id=obj.id, cookie_user_token=data_uuid)
            redirects.set_cookie(key='loggined_token', value=data_uuid, max_age=100000)
        return redirects

    def get_user(self, token=None):
        user = cookie_saves.objects.filter(cookie_user_token=token).first()
        if user is not None:
            user_returned_id = user.cookie_user_id
        else:
            user_returned_id = None
        return User.objects.filter(id=user_returned_id).first()
