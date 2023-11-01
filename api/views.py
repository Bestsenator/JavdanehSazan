from rest_framework.response import Response
from rest_framework.decorators import api_view
from funcs import check, sms
from index.models import VerifyCode
from api.serializers import User, UserSer, InfoProject, InfoProjectSer, Developers, DevelopersSer, Wallet, WalletSer, \
                            Request, RequestSer, SuggestForRequest, SuggestForRequestSer, MiniBook, MiniBookSer
import jdatetime
import random

# Create your views here.


@api_view(['POST'])
def checkSession(request):
    apiKey = request.headers.get('API-X-KEY')
    resAuth = check.checkApiKey(apiKey)
    if resAuth.get('Status') == 900:
        return Response(resAuth)
    session = request.data.get('Session')
    resInfo = check.checkSession(session)
    return Response(resInfo)


@api_view(['POST'])
def getMiniBook(request):
    apiKey = request.headers.get('API-X-KEY')
    resAuth = check.checkApiKey(apiKey)
    if resAuth.get('Status') == 900:
        return Response(resAuth)
    miniBookInfo = MiniBook.objects.all()
    writerInfoSer = MiniBookSer(miniBookInfo[:5], many=True).data
    speakerInfoSer = MiniBookSer(miniBookInfo[5:], many=True).data
    context = {
        'Status': 200,
        'Writer': writerInfoSer,
        'Speaker': speakerInfoSer
    }
    return Response(context)


@api_view(['POST'])
def sendCodeToPhone(request):
    apiKey = request.headers.get('API-X-KEY')
    resAuth = check.checkApiKey(apiKey)
    if resAuth.get('Status') == 900:
        return Response(resAuth)
    phone = request.data.get('Phone')
    if not phone:
        context = {
            'Status': 400,
            'Message': 'Input Incomplete'
        }
        return Response(context)
    if check.checkPhone(phone) is False:
        context = {
            'Status': 401,
            'Message': 'Phone format invalid'
        }
        return Response(context)
    verifyInfo = VerifyCode.objects.filter(Phone=phone).first()
    if verifyInfo:
        if verifyInfo.isVerify is False:
            timeNow = jdatetime.datetime.today().replace(tzinfo=None)
            timeSent = verifyInfo.RegisterTime.replace(tzinfo=None)
            between = (timeNow - timeSent).total_seconds()
            if between >= 120:  # time expire
                verifyInfo.Code = random.randint(123456, 999999)
                verifyInfo.RegisterTime = timeNow
                verifyInfo.save()
                context = {
                    'Status': 200,
                    'Phone': verifyInfo.Phone
                }
                return Response(context)
            else:  # time has not expire
                context = {
                    'Status': 402,
                    'Message': 'The previous code has not yet expired'
                }
                return Response(context)
        else:
            context = {
                'Status': 403,
                'Message': 'The mobile number has been verified for another account'
            }
            return Response(context)
    else:
        randCode = random.randint(123456, 999999)
        # resSms = sms.send(phone, randCode)
        # if resSms != 200:
        #     context = {
        #         'Status': 407,
        #         'Message': 'Wrong to send sms'
        #     }
        #     return Response(context)
        VerifyCode.objects.create(Phone=phone, Code=randCode)
        context = {
            'Status': 200,
            'Phone': phone,
            'Code': randCode
        }
        return Response(context)


@api_view(['POST'])
def checkVerifyCode(request):
    apiKey = request.headers.get('API-X-KEY')
    resAuth = check.checkApiKey(apiKey)
    if resAuth.get('Status') == 900:
        return Response(resAuth)
    phone = request.data.get('Phone')
    code = request.data.get('Code')
    resInput = check.checkInput([phone, code])
    if resInput is False:
        context = {
            'Status': 400,
            'Message': 'Input incomplete'
        }
        return Response(context)
    verifyInfo = VerifyCode.objects.filter(Phone=phone, Code=code).first()
    if verifyInfo:
        if verifyInfo.isVerify is True:
            context = {
                'Status': 401,
                'Message': 'this phone with this code has been verified'
            }
            return Response(context)
        timeNow = jdatetime.datetime.today().replace(tzinfo=None)
        timeSent = verifyInfo.RegisterTime.replace(tzinfo=None)
        between = (timeNow - timeSent).total_seconds()
        if between >= 120:  # time expire
            context = {
                'Status': 402,
                'Message': 'Code has Expire'
            }
            return Response(context)
        else:
            userInfo = User.objects.filter(Phone=phone).first()
            if userInfo:
                userInfoSer = UserSer(userInfo).data
                context = {
                    'Status': 200,  # exist account
                    'Info': userInfoSer
                }
                verifyInfo.delete()
            else:
                verifyInfo.isVerify = True
                verifyInfo.save()
                context = {
                    'Status': 201,  # not exist account
                    'Phone': phone
                }
            return Response(context)
    else:
        context = {
            'Status': 403,
            'Message': 'Code or Phone is Wrong'
        }
        return Response(context)


@api_view(['POST'])
def userRegistration(request):
    apiKey = request.headers.get('API-X-KEY')
    resAuth = check.checkApiKey(apiKey)
    if resAuth.get('Status') == 900:
        return Response(resAuth)
    name = request.data.get('Name')
    family = request.data.get('Family')
    phone = request.data.get('Phone')
    gender = request.data.get('Gender')
    resInput = check.checkInput([name, family, phone, gender])
    if resInput is False:
        context = {
            'Status': 400,
            'Message': 'Input Incomplete'
        }
        return Response(context)
    if not check.checkPhone(phone):
        context = {
            'Status': 401,
            'Message': 'Phone format invalid'
        }
        return Response(context)
    listGender = [1, 2]
    if not gender.isdigit():
        context = {
            'Status': 405,
            'Message': 'gender value wrong'
        }
        return Response(context)
    if int(gender) not in listGender:
        context = {
            'Status': 405,
            'Message': 'gender value wrong'
        }
        return Response(context)
    verifyInfo = VerifyCode.objects.filter(Phone=phone, isVerify=True).first()
    if not verifyInfo:
        context = {
            'Status': 406,
            'Message': 'Phone is not verified'
        }
        return Response(context)
    userInfo = User.objects.create(Name=name, Family=family, Phone=phone)
    Wallet.objects.create(User=userInfo, PricePerCoin=100)
    context = {
        'Status': 200,
        'Session': userInfo.Session
    }
    return Response(context)


@api_view(['GET'])
def getInfoProject(request):
    apiKey = request.headers.get('API-X-KEY')
    resAuth = check.checkApiKey(apiKey)
    if resAuth.get('Status') == 900:
        return Response(resAuth)
    infoSite = InfoProject.objects.first()
    if infoSite:
        infoSiteSer = InfoProjectSer(infoSite).data
        developerInfo = Developers.objects.first()
        developerInfoSer = DevelopersSer(developerInfo).data
        context = {
            'Status': 200,
            'Info': infoSiteSer,
            'Developer': developerInfoSer
        }
    else:
        context = {
            'Status': 400,
            'Message': 'Empty List'
        }
    return Response(context)


@api_view(['POST'])
def editUserInfo(request):
    apiKey = request.headers.get('API-X-KEY')
    resAuth = check.checkApiKey(apiKey)
    if resAuth.get('Status') == 900:
        return Response(resAuth)
    session = request.headers.get('Session')
    resInfo = check.checkSession(session)
    if resInfo.get('Status') == 901:
        return Response(resInfo)
    name = request.data.get('Name')
    family = request.data.get('Family')
    email = request.data.get('Email')
    nationalCode = request.data.get('NationalCode')
    resInput = check.checkInput([name, family, email, nationalCode])
    if resInput is False:
        context = {
            'Status': 400,
            'Message': 'Input Incomplete'
        }
        return Response(context)
    if check.checkEmail(email) is False:
        context = {
            'Status': 401,
            'Message': 'Email format invalid'
        }
        return Response(context)
    if len(nationalCode) != 10 or not nationalCode.isdigit():
        context = {
            'Status': 402,
            'Message': 'NationalCode format invalid'
        }
        return Response(context)
    resInfo.get('Info').Name = name
    resInfo.get('Info').Family = family
    resInfo.get('Info').Email = email
    resInfo.get('Info').NationalCode = nationalCode
    resInfo.get('Info').save()
    context = {
        'Status': 200
    }
    return Response(context)


@api_view(['GET'])
def getWalletUser(request):
    apiKey = request.headers.get('API-X-KEY')
    resAuth = check.checkApiKey(apiKey)
    if resAuth.get('Status') == 900:
        return Response(resAuth)
    session = request.headers.get('Session')
    resInfo = check.checkSession(session)
    if resInfo.get('Status') == 901:
        return Response(resInfo)
    walletInfo = Wallet.objects.filter(User=resInfo.get('Info')).first()
    if walletInfo:
        walletInfoSer = WalletSer(Wallet).data
        context = {
            'Status': 200,
            'Wallet': walletInfoSer
        }
        return Response(context)
    else:
        context = {
            'Status': 400,
            'Message': 'Wallet not found'
        }
        return Response(context)


@api_view(['POST'])
def addRequest(request):
    apiKey = request.headers.get('API-X-KEY')
    resAuth = check.checkApiKey(apiKey)
    if resAuth.get('Status') == 900:
        return Response(resAuth)
    session = request.headers.get('Session')
    resInfo = check.checkSession(session)
    if resInfo.get('Status') == 901:
        return Response(resInfo)
    title = request.data.get('Title')
    content = request.data.get('Content')
    deadLine = request.data.get('DeadLine')
    resInput = check.checkInput([title, content, deadLine])
    if resInput is False:
        context = {
            'Status': 400,
            'Message': 'Input Incomplete'
        }
        return Response(context)
    try:
        deadLine = jdatetime.datetime.strptime(deadLine, '%Y/%m/%d')
    except Exception as e:
        context = {
            'Status': 401,
            'Message': 'DeadLine format invalid',
            'Error': e.__class__.__name__
        }
        return Response(context)
    walletInfo = Wallet.objects.filter(User=resInfo.get('Info')).first()
    if (walletInfo.Inventory - 15000) >= 0:
        Request.objects.create(User=resInfo.get('Info'), Title=title, Content=content, DeadLine=deadLine)
        walletInfo.Inventory = walletInfo - 15000
        walletInfo.save()
        context = {
            'Status': 200
        }
        return Response(context)
    else:
        context = {
            'Status': 402,
            'Message': 'Insufficient inventory'
        }
        return Response(context)


@api_view(['POST'])
def editRequest(request):
    apiKey = request.headers.get('API-X-KEY')
    resAuth = check.checkApiKey(apiKey)
    if resAuth.get('Status') == 900:
        return Response(resAuth)
    session = request.headers.get('Session')
    resInfo = check.checkSession(session)
    if resInfo.get('Status') == 901:
        return Response(resInfo)
    code = request.data.get('Code')
    title = request.data.get('Title')
    content = request.data.get('Content')
    deadLine = request.data.get('DeadLine')
    resInput = check.checkInput([code, title, content, deadLine])
    if resInput is False:
        context = {
            'Status': 400,
            'Message': 'Input Incomplete'
        }
        return Response(context)
    try:
        deadLine = jdatetime.datetime.strptime(deadLine, '%Y/%m/%d')
    except Exception as e:
        context = {
            'Status': 401,
            'Message': 'DeadLine format invalid',
            'Error': e.__class__.__name__
        }
        return Response(context)
    requestInfo = Request.objects.filter(id=code).first()
    if requestInfo:
        if requestInfo.Status == 0:
            pass
        elif requestInfo.Status == 1:
            requestInfo.Status = 0
        else:
            context = {
                'Status': 402,
                'Message': 'Cannot edit this status'
            }
            return Response(context)
        requestInfo.Title = title
        requestInfo.Content = content
        requestInfo.DeadLine = deadLine
        requestInfo.save()
        context = {
            'Status': 200
        }
        return Response(context)
    else:
        context = {
            'Status': 403,
            'Message': 'Request not found'
        }
        return Response(context)


@api_view(['POST'])
def cancelRequest(request):
    apiKey = request.headers.get('API-X-KEY')
    resAuth = check.checkApiKey(apiKey)
    if resAuth.get('Status') == 900:
        return Response(resAuth)
    session = request.headers.get('Session')
    resInfo = check.checkSession(session)
    if resInfo.get('Status') == 901:
        return Response(resInfo)
    code = request.data.get('Code')
    if not code:
        context = {
            'Status': 400,
            'Message': 'Input Incomplete'
        }
        return Request(context)
    requestInfo = Request.objects.filter(id=code).first()
    if requestInfo:
        stInput = [0, 1, 2]
        if requestInfo.Status not in stInput:
            context = {
                'Status': 401,
                'Message': 'Cannot Cancel this status'
            }
            return Request(context)
        requestInfo.Status = -1
        requestInfo.save()
        context = {
            'Status': 200
        }
        return Response(context)
    else:
        context = {
            'Status': 402,
            'Message': 'Request not found'
        }
        return Response(context)


@api_view(['POST'])
def sendSuggestToRequest(request):
    apiKey = request.headers.get('API-X-KEY')
    resAuth = check.checkApiKey(apiKey)
    if resAuth.get('Status') == 900:
        return Response(resAuth)
    session = request.headers.get('Session')
    resInfo = check.checkSession(session)
    if resInfo.get('Status') == 901:
        return Response(resInfo)
    code = request.data.get('Code')
    content = request.data.get('Content')
    price = request.data.get('Price')
    resInput = check.checkInput([code, content, price])
    if resInput is False:
        context = {
            'Status': 400,
            'Message': 'Input Incomplete'
        }
        return Response(context)
    if price.isdigit():
        context = {
            'Status': 401,
            'Message': 'Price is not integer'
        }
        return Response(context)
    stList = [1, 2]
    requestInfo = Request.objects.filter(id=code, Status__in=stList).first()
    if requestInfo:
        suggestInfo = SuggestForRequest.objects.filter(User=resInfo.get('Info')).first()
        if suggestInfo:
            context = {
                'Status': 402,
                'Message': 'you submit a suggest for this request at a time ago'
            }
            return Response(context)
        SuggestForRequest.objects.create(User=resInfo.get('Info'), Request=requestInfo, Content=content, Price=price)
        context = {
            'Status': 200
        }
        return Response(context)
    else:
        context = {
            'Status': 403,
            'Message': 'Request not found'
        }
        return Response(context)


@api_view(['GET'])
def getRequestUser(request):
    apiKey = request.headers.get('API-X-KEY')
    resAuth = check.checkApiKey(apiKey)
    if resAuth.get('Status') == 900:
        return Response(resAuth)
    session = request.headers.get('Session')
    resInfo = check.checkSession(session)
    if resInfo.get('Status') == 901:
        return Response(resInfo)
    requestInfo = Request.objects.filter(User=resInfo.get('Info'))
    if requestInfo:
        resInfoSer = RequestSer(requestInfo, many=True).data
        context = {
            'Status': 200,
            'Request': resInfoSer
        }
        return Response(context)
    else:
        context = {
            'Status': 400,
            'Message': 'Empty List'
        }
        return Response(context)


@api_view(['POST'])
def getSuggestOfRequest(request):
    apiKey = request.headers.get('API-X-KEY')
    resAuth = check.checkApiKey(apiKey)
    if resAuth.get('Status') == 900:
        return Response(resAuth)
    session = request.headers.get('Session')
    resInfo = check.checkSession(session)
    if resInfo.get('Status') == 901:
        return Response(resInfo)
    code = request.data.get('Code')
    if not code:
        context = {
            'Status': 400,
            'Message': 'Input Incomplete'
        }
        return Response(context)
    requestInfo = Request.objects.filter(id=code, User=resInfo.get('Info')).first()
    if requestInfo:
        suggestInfo = SuggestForRequest.objects.filter(Request=requestInfo)
        if suggestInfo:
            suggestInfoSer = SuggestForRequestSer(suggestInfo, many=True).data
            context = {
                'Status': 200,
                'Suggest': suggestInfoSer
            }
            return Response(context)
        else:
            context = {
                'Status': 201,
                'Message': 'Empty List'
            }
            return Response(context)
    else:
        context = {
            'Status': 401,
            'Message': 'request not found'
        }
        return Response(context)
