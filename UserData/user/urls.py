from django.urls import path

from user.views import  UserViewSet


urlpatterns = [
    path('user', UserViewSet.as_view({
        'get': 'list1',
        'post': 'create'
    })),
    path('users/<str:un>,<str:passw>', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
    })),
]