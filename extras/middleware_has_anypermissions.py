from django.utils.deprecation import MiddlewareMixin

from authServer.models import Role


class Is_anypermissions(MiddlewareMixin):

    def process_request(self, request):
        user = request.Auth_user
        if user is not None:
            Selected_Role_administrator = Role.objects.filter(users=user, name=3).exists()
            if not Selected_Role_administrator:
                Selected_Role_moderator = Role.objects.filter(users=user, name=4).exists()
                if not Selected_Role_moderator:
                    request.Is_Anypermissions = False
                    return None
            request.Is_Anypermissions = True
            return None
        request.Is_Anypermissions = False
        return None
