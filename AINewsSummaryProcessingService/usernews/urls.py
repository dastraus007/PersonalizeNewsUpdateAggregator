from django.urls import path
from .views import AINewsSummary

urlpatterns = [
    path(
        'summary',AINewsSummary.as_view()
    ),
]
