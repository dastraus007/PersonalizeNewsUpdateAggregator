from django.urls import path
from .views import AINewsFilter

urlpatterns = [
    path(
        'users/<int:number_of_news_articles>,<str:preference>',AINewsFilter.as_view()
    ),
]
