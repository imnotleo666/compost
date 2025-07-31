from django.urls import path

from api import views

urlpatterns = [
    path('upload', views.upload_file),
    path('user/login', views.login),
    path('user/repassword', views.repassword),
    path('log/getAllData', views.getAllData),

    path('user/list', views.userList),
    path('user/add', views.userAdd),
    path('user/update', views.userUpdate),
    path('user/del', views.userDel),
    path('user/get', views.userById),

    path('log/list', views.logList),
    path('log/add', views.logAdd),
    path('log/update', views.logUpdate),
    path('log/del', views.logDel),
    path('log/get', views.logById),


    path('record/list', views.recordList),
    path('record/add', views.recordAdd),
    path('record/update', views.recordUpdate),
    path('record/del', views.recordDel),
    path('record/get', views.recordById),
]
