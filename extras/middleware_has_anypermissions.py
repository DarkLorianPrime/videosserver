from django.utils.deprecation import MiddlewareMixin

from authServer.models import Role, Role_List


class Is_anypermissions(MiddlewareMixin):
    def process_request(self, request):
        user = request.Auth_user
        if user is not None:
            Selected_Role_administrator = Role.objects.filter(users=user, name=Role_List.objects.filter(
                name='Administrator').first()).first()
            if Selected_Role_administrator is None:
                Selected_Role_moderator = Role.objects.filter(users=user, name=Role_List.objects.filter(
                    name='Moderator').first()).first()
                if Selected_Role_moderator is None:
                    request.Is_Anypermissions = False
                    return None
            request.Is_Anypermissions = True
            return None
        request.Is_Anypermissions = False
        return None
