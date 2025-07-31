# 文件路径：myapp/middleware/request_interceptor.py
import json

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect

from api.models import Log


class GlobalRequestInterceptor(MiddlewareMixin):
    def process_request(self, request):
        # 获取请求路径和数据
        path = request.path
        if 'upload' not in path and 'login' not in path:
            get_params = request.GET.dict()
            post_data = request.POST.dict()
            raw_body = request.body.decode('utf-8')  # 原始请求体（如JSON）
            print(f"请求路径: {path}")
            print(f"GET参数: {get_params}")
            print(f"POST数据: {post_data}")
            print(f"原始请求体: {raw_body}")
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            paths = path.split('/')
            Log.objects.create(userid=auth_header, tables=paths[2], datas=json.dumps(post_data),
                               action=paths[3] if len(paths) >= 4 else '')

        # 返回None表示放行请求
        return None
