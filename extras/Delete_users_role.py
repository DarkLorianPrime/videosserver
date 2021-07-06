from django.contrib.auth.models import User

from authServer.models import Role
from extras import logger_mini


def deleter(form_data, request, id_old, id_new):
    User_Model = User.objects.filter(username=form_data['name']).first()
    Role_selected = Role.objects.filter(name_id=id_old, users=User_Model).first()
    if Role_selected is not None:
        Role_selected.delete()
        Role.objects.create(name_id=id_new, users=User_Model)
        logger_mini.logger(request.Auth_user, 'Remove role', form_data['name'])