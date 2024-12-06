from django.urls import path
from .views import test_send_mail_view

urlpatterns = [
    # Other URLs
    path('', test_send_mail_view, name='test_send_mail'),
]
