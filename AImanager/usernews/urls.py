from django.urls import path


from .views import NewsFetchingView

urlpatterns = [

    path('manager', NewsFetchingView.as_view()),


]
