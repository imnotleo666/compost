import hashlib
import json
import os
import time
from datetime import datetime

from django.conf import settings
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

from api.models import *


class DateEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, o)


def object_to_json(o):
    return dict([(kk, o.__dict__[kk]) for kk in o.__dict__.keys() if kk != "_state"])


# 文件上传代码
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        fileNameSuffix = str(request.FILES['file']).rsplit('.', 1)[-1]
        fileName = '{}.{}'.format(time.time(), fileNameSuffix)
        path = '{}/{}'.format(settings.MEDIA_ROOT, fileName)
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(path)
        with open(path, 'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
                print('保存成功')
        resp = {'data': 'http://localhost{}{}'.format(settings.MEDIA_URL, fileName), }
        return HttpResponse(json.dumps(resp), content_type='application/json')


@csrf_exempt
def download_file(request):
    fileurl = request.POST.get('fileurl')
    fileName = fileurl.split('/')[-1]
    file_path = settings.MEDIA_ROOT + '/' + fileName

    def file_iterator(file_path, chunk_size=1024 * 1024):
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                yield chunk

    response = StreamingHttpResponse(file_iterator(file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename*=UTF-8''{escape_uri_path("机密文档.txt")}'
    return response


@csrf_exempt
def repassword(request):
    request_dict = request.POST
    user_id = request_dict.get("id")
    newPassword = request_dict.get("newPassword")
    oldPassword = request_dict.get("oldPassword")
    # 创建 MD5 哈希对象
    md5_hash = hashlib.md5()
    # 更新哈希对象的内容，需要将字符串编码为字节类型
    md5_hash.update(oldPassword.encode('utf-8'))
    # 获取加密后的十六进制字符串
    oldPassword = md5_hash.hexdigest()
    print(oldPassword, user_id)
    obj = User.objects.filter(id=user_id).filter(password=oldPassword).first()
    print(obj)
    if not obj:
        return JsonResponse({"message": "旧密码错误"})
    # 创建 MD5 哈希对象
    md5_hash = hashlib.md5()
    # 更新哈希对象的内容，需要将字符串编码为字节类型
    md5_hash.update(newPassword.encode('utf-8'))
    # 获取加密后的十六进制字符串
    newPassword = md5_hash.hexdigest()
    obj.password = newPassword
    obj.save()
    response = {"message": "success"}
    return JsonResponse(response)


@csrf_exempt
def login(request):
    request_dict = request.POST
    username = request_dict.get("username")
    password = request_dict.get("password")
    role = request_dict.get("role")
    # 创建 MD5 哈希对象
    md5_hash = hashlib.md5()
    # 更新哈希对象的内容，需要将字符串编码为字节类型
    md5_hash.update(password.encode('utf-8'))
    # 获取加密后的十六进制字符串
    password = md5_hash.hexdigest()
    print(password)
    try:
        obj = User.objects.get(username=username, password=password,role=role)
        object_json = {
            "id": obj.id,
            "username": obj.username,
            "role": obj.role,
            "avatar": obj.avatar,
            "phone": obj.phone,
            "email": obj.email,
            "gender": obj.gender,
            "createtime": obj.createtime,
            "name": obj.name,
            "password": obj.password,
        }
        return JsonResponse({'data': object_json}, safe=False)
    except Exception as e:
        print("error-----------")
        print(e)
        obj = None
        return JsonResponse(obj, safe=False)


@csrf_exempt
def getAllData(request):
    daily_counts = (
        Log.objects
        .annotate(date=TruncDate('createtime'))  # 按日期截断
        .values('date')  # 按日期分组
        .annotate(count=Count('id'))  # 统计每日数量
        .order_by('date')  # 按日期排序
    )
    user_counts = (
        Log.objects
        .values('userid')  # 按用户ID分组
        .annotate(total=Count('id'))  # 统计每个用户的记录总数
        .order_by('-total')  # 按数量降序
    )

    action_counts = (
        Log.objects
        .values('action')  # 按动作类型分组
        .annotate(count=Count('id'))  # 统计每个Action的数量
        .order_by('-count')  # 按数量降序
    )

    table_counts = (
        Log.objects
        .values('tables')  # 按表名分组
        .annotate(count=Count('id'))  # 统计每个表的记录数
        .order_by('-count')  # 按数量降序
    )
    for item in user_counts:
        item['name'] = User.objects.get(id=item['userid']).name
    response = {
        'action_counts': [item for item in action_counts],
        'table_counts': [item for item in table_counts],
        'daily_counts': [item for item in daily_counts],
        'user_count': [item for item in user_counts]
    }
    print(response)
    return JsonResponse(response)


@csrf_exempt
def userAdd(request):
    request_dict = request.POST
    username = request_dict.get("username")
    phone = request_dict.get("phone")
    email = request_dict.get("email")
    avatar = request_dict.get("avatar")
    name = request_dict.get("name")
    gender = request_dict.get("gender")
    password = request_dict.get("password")
    # 创建 MD5 哈希对象
    md5_hash = hashlib.md5()
    # 更新哈希对象的内容，需要将字符串编码为字节类型
    md5_hash.update(password.encode('utf-8'))
    # 获取加密后的十六进制字符串
    password = md5_hash.hexdigest()
    role = request_dict.get("role")
    User.objects.create(username=username, phone=phone, email=email, avatar=avatar, name=name, gender=gender,
                        password=password, role=role)
    response = {
        "message": "success"
    }
    return JsonResponse(response)


@csrf_exempt
def userUpdate(request):
    request_dict = request.POST
    id = request_dict.get("id")
    username = request_dict.get("username")
    phone = request_dict.get("phone")
    email = request_dict.get("email")
    avatar = request_dict.get("avatar")
    name = request_dict.get("name")
    gender = request_dict.get("gender")
    password = request_dict.get("password")
    role = request_dict.get("role")
    obj = User.objects.get(id=id)
    if username:
        obj.username = username
    if phone:
        obj.phone = phone
    if email:
        obj.email = email
    if avatar:
        obj.avatar = avatar
    if name:
        obj.name = name
    if gender:
        obj.gender = gender
    if password:
        # 创建 MD5 哈希对象
        md5_hash = hashlib.md5()
        # 更新哈希对象的内容，需要将字符串编码为字节类型
        md5_hash.update(password.encode('utf-8'))
        # 获取加密后的十六进制字符串
        password = md5_hash.hexdigest()
        obj.password = password
    if role:
        obj.role = role
    obj.save()
    response = {
        "message": "success"
    }
    return JsonResponse(response)


@csrf_exempt
def userById(request):
    request_dict = request.POST
    id = request_dict.get("id")
    obj = User.objects.get(id=id)
    dic_obj = object_to_json(obj)
    return JsonResponse(dic_obj, safe=False)


@csrf_exempt
def userDel(request):
    request_dict = request.POST
    id = request_dict.get("id")
    User.objects.filter(id=id).delete()
    response = {
        "message": "success"
    }
    return JsonResponse(response)


@csrf_exempt
def userList(request):
    request_dict = request.POST
    page = request_dict.get("pageIndex")
    pageSizes = request_dict.get("pageSize")
    username = request_dict.get("username")

    phone = request_dict.get("phone")
    email = request_dict.get("email")
    avatar = request_dict.get("avatar")
    name = request_dict.get("name")
    gender = request_dict.get("gender")
    password = request_dict.get("password")
    role = request_dict.get("role")
    pageSize = 5
    if pageSizes != None and pageSizes != '':
        pageSize = int(pageSizes)
    if page == None or page == '':
        page = 1
    response = {}
    objList = User.objects.all().order_by('-id')
    if username:
        objList = objList.filter(username__contains=username)
    if phone:
        objList = objList.filter(phone__contains=phone)
    if email:
        objList = objList.filter(email__contains=email)
    if avatar:
        objList = objList.filter(avatar__contains=avatar)
    if name:
        objList = objList.filter(name__contains=name)
    if gender:
        objList = objList.filter(gender__contains=gender)
    if password:
        objList = objList.filter(password__contains=password)
    if role:
        objList = objList.filter(role__contains=role)
    paginator = Paginator(objList, pageSize)
    response['total'] = paginator.count
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)
    list = []
    for obj in objs:
        list.append({
            'id': obj.id,
            'username': obj.username,
            'phone': obj.phone,
            'email': obj.email,
            'avatar': obj.avatar,
            'name': obj.name,
            'password': obj.password,
            'role': obj.role,
            'createtime': obj.createtime,
        })
    response['list'] = list
    return JsonResponse(response)


@csrf_exempt
def logAdd(request):
    request_dict = request.POST
    userid = request_dict.get("userid")

    tables = request_dict.get("tables")
    action = request_dict.get("action")
    datas = request_dict.get("datas")
    Log.objects.create(userid=userid, tables=tables, action=action, datas=datas, )
    response = {
        "message": "success"
    }
    return JsonResponse(response)


@csrf_exempt
def logUpdate(request):
    request_dict = request.POST
    id = request_dict.get("id")
    userid = request_dict.get("userid")
    tables = request_dict.get("tables")
    action = request_dict.get("action")
    datas = request_dict.get("datas")
    obj = Log.objects.get(id=id)
    if userid:
        obj.userid = userid
    if tables:
        obj.tables = tables
    if action:
        obj.action = action
    if datas:
        obj.datas = datas
    obj.save()
    response = {
        "message": "success"
    }
    return JsonResponse(response)


@csrf_exempt
def logById(request):
    request_dict = request.POST
    id = request_dict.get("id")
    obj = Log.objects.get(id=id)
    dic_obj = object_to_json(obj)
    return JsonResponse(dic_obj, safe=False)


@csrf_exempt
def logDel(request):
    request_dict = request.POST
    id = request_dict.get("id")
    Log.objects.filter(id=id).delete()
    response = {
        "message": "success"
    }
    return JsonResponse(response)


@csrf_exempt
def logList(request):
    request_dict = request.POST
    page = request_dict.get("pageIndex")
    pageSizes = request_dict.get("pageSize")
    userid = request_dict.get("userid")

    tables = request_dict.get("tables")
    action = request_dict.get("action")
    datas = request_dict.get("datas")
    pageSize = 5
    if pageSizes != None and pageSizes != '':
        pageSize = int(pageSizes)
    if page == None or page == '':
        page = 1
    response = {}
    objList = Log.objects.all().order_by('-id')
    if userid:
        objList = objList.filter(userid__contains=userid)
    if tables:
        objList = objList.filter(tables__contains=tables)
    if action:
        objList = objList.filter(action__contains=action)
    if datas:
        objList = objList.filter(datas__contains=datas)
    paginator = Paginator(objList, pageSize)
    response['total'] = paginator.count
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)
    list = []
    for obj in objs:
        user = User.objects.get(id=obj.userid)
        list.append({
            'id': obj.id,
            'userid': obj.userid,
            'tables': obj.tables,
            'action': obj.action,
            'datas': obj.datas,
            'createtime': obj.createtime,
            'name': user.name if user else '',
        })
    response['list'] = list
    return JsonResponse(response)

from utils import train
@csrf_exempt
def recordAdd(request):
    request_dict = request.POST
    userid = request_dict.get("userid")
    imageurl = request_dict.get("imageurl")
    starttime = time.time()
    classifier = train.classifier
    result, confidence, probabilities = classifier.predict(f'upload/{imageurl.split("/")[-1]}')
    endtime = time.time()
    timeconsuming = endtime - starttime

    Record.objects.create(userid=userid, imageurl=imageurl, result=result, confidence=confidence,
                          timeconsuming=timeconsuming, )
    response = {
        "message": "success"
    }
    return JsonResponse(response)


@csrf_exempt
def recordUpdate(request):
    request_dict = request.POST
    id = request_dict.get("id")
    userid = request_dict.get("userid")
    imageurl = request_dict.get("imageurl")
    result = request_dict.get("result")
    confidence = request_dict.get("confidence")
    timeconsuming = request_dict.get("timeconsuming")
    obj = Record.objects.get(id=id)
    if userid:


        obj.userid = userid
    if imageurl:
        obj.imageurl = imageurl
    if result:
        obj.result = result
    if confidence:
        obj.confidence = confidence
    if timeconsuming:
        obj.timeconsuming = timeconsuming
    obj.save()
    response = {
        "message": "success"
    }
    return JsonResponse(response)


@csrf_exempt
def recordById(request):
    request_dict = request.POST
    id = request_dict.get("id")
    obj = Record.objects.get(id=id)
    dic_obj = object_to_json(obj)
    return JsonResponse(dic_obj, safe=False)


@csrf_exempt
def recordDel(request):
    request_dict = request.POST
    id = request_dict.get("id")
    Record.objects.filter(id=id).delete()
    response = {
        "message": "success"
    }
    return JsonResponse(response)


@csrf_exempt
def recordList(request):
    request_dict = request.POST
    page = request_dict.get("pageIndex")
    pageSizes = request_dict.get("pageSize")
    userid = request_dict.get("userid")


    imageurl = request_dict.get("imageurl")
    result = request_dict.get("result")
    confidence = request_dict.get("confidence")
    timeconsuming = request_dict.get("timeconsuming")
    pageSize = 5
    if pageSizes != None and pageSizes != '':
        pageSize = int(pageSizes)
    if page == None or page == '':
        page = 1
    response = {}
    objList = Record.objects.all().order_by('-id')
    if userid:
        objList = objList.filter(userid__contains=userid)
    if imageurl:
        objList = objList.filter(imageurl__contains=imageurl)
    if result:
        objList = objList.filter(result__contains=result)
    if confidence:
        objList = objList.filter(confidence__contains=confidence)
    if timeconsuming:
        objList = objList.filter(timeconsuming__contains=timeconsuming)
    paginator = Paginator(objList, pageSize)
    response['total'] = paginator.count
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)
    list = []
    for obj in objs:
        if obj.userid:
            user = User.objects.get(id=obj.userid)
            name = user.name if user else '--'
        else:
            name = ''
        list.append({
            'id': obj.id,
            'userid': obj.userid,
            'imageurl': obj.imageurl,
            'result': obj.result,
            'confidence': obj.confidence,
            'timeconsuming': obj.timeconsuming,
            'createtime': obj.createtime,
            'name': name,
        })
    response['list'] = list
    return JsonResponse(response)