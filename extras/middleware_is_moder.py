from django.utils.deprecation import MiddlewareMixin

from authServer.models import Role, Role_List


class Is_Moder(MiddlewareMixin):
    def process_request(self, request):
        user = request.Auth_user
        if user is not None:
            Selected_Role = Role.objects.filter(users=user, name=Role_List.objects.filter(name='Moderator').first()).first()
            if Selected_Role is not None:
                request.is_moderator = True
                return None
            request.is_moderator = False
            return None
        request.is_moderator = False
        return None