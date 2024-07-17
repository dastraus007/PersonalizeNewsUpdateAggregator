from django.urls import path


from .views import NewsEmailView

urlpatterns = [
    path('email/<str:email>', NewsEmailView.as_view()),


]
