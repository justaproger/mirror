from django.urls import path
from myapp.views import MyProxyView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', MyProxyView.as_view(), name='proxy'),
]
