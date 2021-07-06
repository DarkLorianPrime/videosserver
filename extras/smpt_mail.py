import secrets
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth.models import User

from authServer.models import Recent_res
from extras import template_reader


def send_mail(login, password, to_mail):
    message_template = template_reader.parse_template()
    obj = smtplib.SMTP('smtp.mail.ru', 587)
    obj.starttls()
    obj.login(login, password)
    multipart = MIMEMultipart()
    user = User.objects.filter(email=to_mail).first()
    code = secrets.token_urlsafe(8)
    if Recent_res.objects.filter(user=user).exists():
        code = Recent_res.objects.filter(user=user).first().request_token
    else:
        Recent_res.objects.create(user=user, request_token=code)
    message = message_template.substitute(USER_NAME=user, code=code)
    multipart['Subject'] = 'Recent Password'
    multipart.attach(MIMEText(message, 'msg'))
    obj.sendmail(to_addrs=to_mail, from_addr=login,
                 msg=multipart.as_string().encode('utf-8'))