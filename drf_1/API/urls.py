from django.urls import path

from API import views

urlpatterns = [
    path("user/", views.user),
    # 为类视图定义url
    path("users/", views.UserView.as_view()),

    path("student/", views.StudentView.as_view()),
    path("student/<str:user_id>/", views.StudentView.as_view()),

    # DRF的类视图  调用的as_view与Django的不是同一个方法
    path("user_api/", views.UserAPIView.as_view()),
]