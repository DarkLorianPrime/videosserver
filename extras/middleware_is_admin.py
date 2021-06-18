from django.utils.deprecation import MiddlewareMixin

from authServer.models import Role


class Is_Admin(MiddlewareMixin):
    def process_request(self, request):
        user = request.Auth_user
        if user is not None:
            Selected_Role = Role.objects.filter(Users=user, name='Administrator', is_Role=True).first()
            if Selected_Role is not None:
                request.is_administrator = True
                return None
            request.is_administrator = False
            return None
        request.is_administrator = False
        return None
