from django.urls import path
from api import views


urlpatterns = [
    path('checkSession/', views.checkSession),
    path('sendCodeToPhone/', views.sendCodeToPhone),
    path('checkVerifyCode/', views.checkVerifyCode),
    path('userRegistration/', views.userRegistration),
    path('editUserInfo/', views.editUserInfo),
    path('getInfoProject/', views.getInfoProject),
    path('getWalletUser/', views.getWalletUser),
    path('addRequest/', views.addRequest),
    path('editRequest/', views.editRequest),
    path('cancelRequest/', views.cancelRequest),
    path('getSuggestOfRequest/', views.getSuggestOfRequest),
    path('getRequestUser/', views.getRequestUser),
    path('sendSuggestToRequest/', views.sendSuggestToRequest),
    path('cancelRequest/', views.cancelRequest),
    path('editRequest/', views.editRequest),
    path('addRequest/', views.addRequest),
]
