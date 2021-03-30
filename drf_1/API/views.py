from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.response import Response
from rest_framework.views import APIView

from API.models import User


def user(request):
    if request.method == "GET":
        print("查询  GET")
        # TODO 查询用户的相关逻辑
        return HttpResponse("GET SUCCESS")

    if request.method == "POST":
        print("添加  POST")
        # TODO 添加用户的相关逻辑
        return HttpResponse("POST SUCCESS")

    if request.method == "PUT":
        print("修改  PUT")
        # TODO 修改用户的相关逻辑
        return HttpResponse("PUT SUCCESS")

    if request.method == "DELETE":
        print("删除  DELETE")
        # TODO 删除用户的相关逻辑
        return HttpResponse("DELETE SUCCESS")


"""
django视图模式有两种：
FBV: function base view  基于函数的视图
CBV：class base view     基于类的视图  更符合面向对象思想
"""


# @method_decorator(csrf_protect, name="dispatch")  # 为类视图添加csrf认证
@method_decorator(csrf_exempt, name="dispatch")  # 让类视图免除csrf认证
class UserView(View):
    """
    类视图内部通过请求的http方法来匹配到内部的函数，从而进行对应的处理
    """

    def dispatch(self, request, *args, **kwargs):
        print("先于所有的http函数执行")
        # 调用父类的dispatch方法
        obj = super(UserView, self).dispatch(request, *args, **kwargs)
        return obj

    def get(self, request, *args, **kwargs):
        print("查询  GET")
        return HttpResponse("DRF GET SUCCESS")

    def post(self, request, *args, **kwargs):
        print("查询  POST")
        return HttpResponse("DRF POST SUCCESS")

    def put(self, request, *args, **kwargs):
        print("查询  PUT")
        return HttpResponse("DRF PUT SUCCESS")

    def delete(self, request, *args, **kwargs):
        print("查询  DELETE")
        return HttpResponse("DRF DELETE SUCCESS")


"""
查询单个  查询所有  新增单个  新增多个  删除单个  删除多个
修改单个  修改多个  局部修改单个  局部修改多个
"""


@method_decorator(csrf_exempt, name="dispatch")
class StudentView(View):
    """
    提供对用户操作的常见API
    """

    def get(self, request, *args, **kwargs):
        """
        提供查询单个用户 以及所有用户的操作
        :param request: 请求参数 用户id
        :param kwargs:
        :return:    查询出的用户信息
        """

        # 接收前端路径中包含的参数  可变长参数
        user_id = kwargs.get("user_id")

        # 路径中包含参数则代表查询单个
        if user_id:
            user_obj = User.objects.filter(pk=user_id).values("username", "password", "gender").first()
            # 将查询出的单个对象的数据返回到前端
            if user_obj:
                # 如果查询出对应的用户信息，则将用户信息返回  返回的数据需要有一定的格式
                return JsonResponse({
                    "status": 200,
                    "message": "查询单个用户成功",
                    "results": user_obj})
        # 如果路径中不包含参数 则代表查询所有
        else:
            user_list = User.objects.all().values("username", "password", "gender")
            # 将数据转换成json返回到前端
            if user_list:
                return JsonResponse({
                    "status": 200,
                    "message": "查询所有用户成功",
                    "results": list(user_list),
                })

        return JsonResponse({
            "status": 500,
            "message": "查询的用户不存在",
        })

    def post(self, request, *args, **kwargs):
        """
        新增单个用户
        """
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.create(username=username, password=password)
            return JsonResponse({
                "status": 201,
                "message": "创建单个用户成功",
                "results": {"username": user_obj.username, "gender": user_obj.gender}
            })

        except:
            return JsonResponse({
                "status": 500,
                "message": "新增单个用户失败"
            })


class UserAPIView(APIView):
    """
    DRF的第一个类视图
    """

    def get(self, request, *args, **kwargs):
        print("DRF GET VIEW")
        return Response("DRF GET SUCCESS")

    def post(self, request, *args, **kwargs):
        print("DRF POST VIEW")
        return Response("DRF POST SUCCESS")
