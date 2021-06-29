from django.utils import timezone


def logger(user, method, data):
    with open('logger.log', 'a+') as logger_data:
        logger_data.write(f'\n[{timezone.now()}] {user} {method}: {data}')