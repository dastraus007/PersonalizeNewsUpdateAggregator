from django.urls import path
from .views import AINews

urlpatterns = [
    path(
        'users',AINews.as_view()
    ),
]
