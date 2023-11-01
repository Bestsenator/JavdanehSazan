from index.models import User, APIKEY
import re


def checkSession(session):
    userInfo = User.objects.filter(Session=session).first()
    if userInfo:
        context = {
            'Status': 200,
            'Info': userInfo
        }
        return context
    else:
        context = {
            'Status': 901,
            'Message': 'Session invalid'
        }
        return context


def checkApiKey(apikey):
    apiInfo = APIKEY.objects.filter(ApiKey=apikey).first()
    if apiInfo:
        context = {
            'Status': 200,
            'Info': apiInfo
        }
    else:
        context = {
            'Status': 900,
            'Message': 'API-X-KEY invalid'
        }
    return context


def checkPhone(phone):
    if not phone.startswith('09'):
        return False
    if len(phone) != 11:
        return False
    if not phone.isdigit():
        return False
    return True


def checkInput(items):
    for item in items:
        if not item:
            return False
    return True


def checkEmail(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    return True
